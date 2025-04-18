import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# from models import Rating, Movie  <- Remove this line
# from app import db              <- Remove this line
from extensions import db # <- Add this line

# 缓存用户-物品评分矩阵和用户相似度矩阵，避免重复计算
user_item_matrix_cache = None
user_similarity_cache = None

def get_user_item_matrix():
    """获取用户-物品评分矩阵."""
    # Move imports inside the function
    from models import Rating # <- Keep this import local if needed only here
    global user_item_matrix_cache
    if user_item_matrix_cache is not None:
        return user_item_matrix_cache

    print("Loading ratings data for user-item matrix...")
    # 从数据库加载评分数据
    ratings_query = db.session.query(Rating.user_id, Rating.movie_id, Rating.rating)
    ratings_df = pd.read_sql(ratings_query.statement, db.session.bind)

    if ratings_df.empty:
        print("No ratings data found in the database.")
        return None

    print(f"Loaded {len(ratings_df)} ratings.")
    print("Creating user-item matrix...")
    # 创建用户-物品评分矩阵
    user_item_matrix = ratings_df.pivot_table(index='user_id', columns='movie_id', values='rating')
    # 填充 NaN 值为 0 (或者可以使用均值填充等策略)
    user_item_matrix = user_item_matrix.fillna(0)
    print("User-item matrix created.")
    user_item_matrix_cache = user_item_matrix
    return user_item_matrix

def get_user_similarity():
    """计算用户之间的相似度 (基于余弦相似度)."""
    global user_similarity_cache
    if user_similarity_cache is not None:
        return user_similarity_cache

    user_item_matrix = get_user_item_matrix()
    if user_item_matrix is None:
        return None

    print("Calculating user similarity...")
    # 计算用户相似度矩阵
    user_similarity = cosine_similarity(user_item_matrix)
    # 转换为 DataFrame，方便索引
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
    print("User similarity calculated.")
    user_similarity_cache = user_similarity_df
    return user_similarity_df

def recommend_movies_for_user(user_id, num_recommendations=10):
    """为指定用户推荐电影 (基于用户的协同过滤)."""
    # Move imports inside the function
    from models import Rating, Movie
    # from app import db <- Remove this line
    print(f"Generating recommendations for user {user_id}...")
    user_item_matrix = get_user_item_matrix()
    user_similarity = get_user_similarity()

    if user_item_matrix is None or user_similarity is None:
        print("Error: Could not get user-item matrix or user similarity.")
        return []

    if user_id not in user_similarity.index:
        print(f"User {user_id} not found in the similarity matrix.")
        return []

    # 获取与该用户最相似的用户 (排除自己)
    similar_users = user_similarity[user_id].sort_values(ascending=False)[1:]

    # 获取该用户已评分的电影
    user_rated_movies = user_item_matrix.loc[user_id]
    movies_rated_by_user = user_rated_movies[user_rated_movies > 0].index.tolist()
    print(f"User {user_id} has rated {len(movies_rated_by_user)} movies.")

    # 计算推荐电影的得分
    recommendation_scores = {}

    # 遍历相似用户
    for similar_user_id, similarity_score in similar_users.items():
        if similarity_score <= 0: # 忽略不相似或负相关的用户
            continue

        # 获取相似用户评分过，但目标用户未评分的电影
        similar_user_ratings = user_item_matrix.loc[similar_user_id]
        movies_to_recommend = similar_user_ratings[similar_user_ratings > 0].index

        for movie_id in movies_to_recommend:
            if movie_id not in movies_rated_by_user:
                # 加权评分：相似度 * 相似用户的评分
                weighted_rating = similarity_score * similar_user_ratings[movie_id]
                recommendation_scores[movie_id] = recommendation_scores.get(movie_id, 0) + weighted_rating

    # 按得分排序
    sorted_recommendations = sorted(recommendation_scores.items(), key=lambda item: item[1], reverse=True)

    # 获取推荐电影的详细信息
    recommended_movie_ids = [movie_id for movie_id, score in sorted_recommendations[:num_recommendations]]

    if not recommended_movie_ids:
        print(f"No recommendations generated for user {user_id}.")
        return []

    print(f"Retrieving details for {len(recommended_movie_ids)} recommended movies...")
    # 从数据库查询电影信息
    recommended_movies = db.session.query(Movie.id, Movie.title, Movie.genres)\
                                     .filter(Movie.id.in_(recommended_movie_ids)).all()

    # 构建结果列表，保持推荐顺序
    movie_details_map = {movie.id: movie for movie in recommended_movies}
    final_recommendations = []
    for movie_id in recommended_movie_ids:
        if movie_id in movie_details_map:
            movie = movie_details_map[movie_id]
            final_recommendations.append({
                'movie_id': movie.id,
                'title': movie.title,
                'genres': movie.genres,
                'score': recommendation_scores[movie_id] # 可以选择性返回预测得分
            })

    print(f"Generated {len(final_recommendations)} recommendations for user {user_id}.")
    return final_recommendations

# 可以在这里添加其他推荐算法，如基于物品的协同过滤、矩阵分解等