import os
import pprint
import tempfile
from typing import Dict, Text

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs

# --- 1. 数据加载与准备 ---

# 加载 MovieLens 100k 数据集
print("Loading dataset...")
# 在这里，我们保留 movie_genres 的原始整数格式
ratings = tfds.load("movielens/100k-ratings", split="train")
movies = tfds.load("movielens/100k-movies", split="train")

# 提取用户ID和电影特征。注意这里 movie_genres 保持不变。
ratings = ratings.map(lambda x: {
    "movie_title": x["movie_title"],
    "user_id": x["user_id"],
    "movie_genres": x["movie_genres"]
})

movies = movies.map(lambda x: {
    "movie_title": x["movie_title"],
    "movie_genres": x["movie_genres"]
})

# 构建用户ID和电影标题的词汇表 (它们是字符串/bytes)
print("Building vocabularies for user_id and movie_title...")
user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
user_ids_vocabulary.adapt(ratings.map(lambda x: x["user_id"]))

movie_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
movie_titles_vocabulary.adapt(movies.map(lambda x: x["movie_title"]))

# --- 找出电影类型的最大 ID ---
# 因为 movie_genres 已经是整数 ID，我们需要找到最大的 ID 来设置 Embedding 层的大小
print("Finding maximum movie genre ID...")
all_movie_genres_ids = []
for movie in movies.map(lambda x: x["movie_genres"]):
    # movie["movie_genres"] 是一个张量，可能包含多个 genre ID
    # 在这里直接处理原始 movies 数据集，它里面的 movie_genres 仍然是标准的tf.Tensor
    all_movie_genres_ids.extend(movie.numpy().tolist()) # 将张量转换为列表并添加到总列表

max_movie_genre_id = max(all_movie_genres_ids)
num_movie_genres = max_movie_genre_id + 1 # Embedding 层维度需要包含所有可能的 ID，从 0 到 max_id

print(f"Maximum movie genre ID found: {max_movie_genre_id}")
print(f"Number of unique movie genres (for embedding layer): {num_movie_genres}")


# 数据划分
print("Splitting data into train and test sets...")
tf.random.set_seed(42)
shuffled_ratings = ratings.shuffle(100_000, seed=42, reshuffle_each_iteration=False)

train = shuffled_ratings.take(80_000)
test = shuffled_ratings.skip(80_000).take(20_000)

# 批量处理和缓存数据
print("Batching and caching data...")
# 修改：使用 ragged_batch 来处理训练/测试数据中 movie_genres 的可变长度
cached_train = train.ragged_batch(4096).cache()
cached_test = test.ragged_batch(4096).cache()

# --- 2. 模型构建 (双塔模型) ---

embedding_dimension = 64  # 嵌入维度，可以调整

# 定义用户模型 (Query tower)
user_model = tf.keras.Sequential([
    user_ids_vocabulary,
    # 修正：使用 vocabulary_size()
    tf.keras.layers.Embedding(user_ids_vocabulary.vocabulary_size(), embedding_dimension)
])

# 定义电影模型 (Candidate tower)
class MovieCandidateModel(tf.keras.Model):
    def __init__(self, movie_titles_vocabulary, num_movie_genres, embedding_dimension):
        super().__init__()
        # 处理电影标题 (字符串 -> 嵌入)
        self.movie_titles_embedding = tf.keras.Sequential([
            movie_titles_vocabulary,
            # 修正：使用 vocabulary_size()
            tf.keras.layers.Embedding(movie_titles_vocabulary.vocabulary_size(), embedding_dimension)
        ])
        # 处理电影类型 (整数 ID -> 嵌入)
        # Embedding 层能够处理 RaggedTensor 输入
        self.movie_genres_embedding = tf.keras.layers.Embedding(
            input_dim=num_movie_genres,
            output_dim=embedding_dimension
        )
        # 组合不同特征的 embeddings
        self.combination_layer = tf.keras.layers.Dense(embedding_dimension, activation="relu")

    def call(self, inputs):
        # inputs["movie_title"] 是一个 Tensor 或 RaggedTensor (来自 ragged_batch)
        # inputs["movie_genres"] 是一个 RaggedTensor (来自 ragged_batch)
        title_embedding = self.movie_titles_embedding(inputs["movie_title"])
        genres_embedding = self.movie_genres_embedding(inputs["movie_genres"]) # Output is RaggedTensor

        # 对 RaggedTensor 进行求和，axis=1 会在每个样本内部的第二个维度（嵌入维度）求和
        # 结果 shape 是 [batch_size, embedding_dimension]
        genres_embedding_aggregated = tf.reduce_sum(genres_embedding, axis=1)

        # 确保 title_embedding 是密集张量以便拼接
        # 理论上 movie_title 应该是密集张量，但为了保险，这里检查并转换
        if isinstance(title_embedding, tf.RaggedTensor):
            title_embedding = title_embedding.to_tensor()


        combined_embedding = tf.concat([title_embedding, genres_embedding_aggregated], axis=1)
        return self.combination_layer(combined_embedding)


# 定义完整的 TFRS 模型
class MovieLensModel(tfrs.Model):
    def __init__(self, user_model, movie_model, movies_dataset):
        super().__init__()
        self.user_model = user_model
        self.movie_model = movie_model
        # 定义检索任务和评估指标
        # 注意：这里的 candidates 应该是经过 movie_model 处理后的电影 embeddings
        # 这里需要将 movies_dataset 的每个元素（字典）传递给 movie_model
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                # 修改：对用于 candidates 的数据集也使用 ragged_batch
                candidates=movies_dataset.ragged_batch(128).map(self.movie_model)
            )
        )

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        # features["user_id"] 是一个 Tensor (通常来自原始数据集或 map)
        # features["movie_title"] 是一个 Tensor 或 RaggedTensor (来自 ragged_batch)
        # features["movie_genres"] 是一个 RaggedTensor (来自 ragged_batch)

        # 计算用户和电影的 embeddings
        user_embeddings = self.user_model(features["user_id"])
        # 将完整的电影特征字典传递给 movie_model
        movie_embeddings = self.movie_model({
            "movie_title": features["movie_title"],
            "movie_genres": features["movie_genres"]
        })

        # 将 embeddings 传递给任务计算损失
        return self.task(user_embeddings, movie_embeddings)

# 创建电影候选模型实例
movie_candidate_model = MovieCandidateModel(movie_titles_vocabulary, num_movie_genres, embedding_dimension)

# 创建完整的 TFRS 模型实例
# 注意：这里的 movies 数据集需要保留 movie_genres 特征以便传递给 movie_model
model = MovieLensModel(user_model, movie_candidate_model, movies)


# --- 3. 模型编译与训练 ---

print("Compiling and training the model...")
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.5))

# 训练模型
model.fit(cached_train, epochs=3) # 可以调整训练轮数


# --- 4. 模型评估 ---

print("Evaluating the model...")
model.evaluate(cached_test, return_dict=True)


# --- 5. 生成推荐 ---

print("Generating recommendations...")
# 构建检索索引。索引是基于电影 embeddings 构建的。
# 注意：这里需要使用 movie_candidate_model 来处理电影数据以获取 embeddings
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
# 在 index_from_dataset 中，需要传递电影的特征字典给 movie_model
# 修改：对用于构建索引的 movies 数据集也使用 ragged_batch
index.index_from_dataset(
    movies.ragged_batch(100).map(lambda movie_features: (
        movie_features["movie_title"], # 使用电影标题作为标识符
        model.movie_model(movie_features) # 将电影特征字典传递给 movie_model
    ))
)

# 为特定用户生成 Top-K 推荐
user_id_to_recommend = "33"
# 获取用户 embedding
# user_embedding = model.user_model(tf.constant([user_id_to_recommend])) # 这行不再需要了

# 使用索引查找最相似的电影
# index 返回两个张量：第一个是相似度得分，第二个是电影标题（或其他你用于索引的标识符）
# 修改：直接将原始用户 ID 张量传递给 index 层，它会内部调用 user_model
scores, titles = index(tf.constant([user_id_to_recommend])) # 修改为这行

print(f"Top recommendations for user {user_id_to_recommend}:")
# 解码 byte string 并打印电影标题
for title in titles[0, :10].numpy():
    print(title.decode("utf-8"))