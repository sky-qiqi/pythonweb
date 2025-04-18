import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 加载您的数据集
file_path = r'C:\Users\qiqi\OneDrive\Desktop\code\pythonweb\t2\Groceries_dataset.csv'
df = pd.read_csv(file_path)

# 将数据按 Member_number 分组，获取每个用户的购物篮
transactions = df.groupby('Member_number')['itemDescription'].apply(list).tolist()

print("原始交易数据示例:")
print(transactions[:5])

# 数据预处理
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)
print("\nOne-hot 编码后的数据示例:")
print(df_encoded.head())

# 设置最小支持度和最小置信度
min_support = 0.01  # 您可以根据需要调整这个值
min_confidence = 0.2  # 您可以根据需要调整这个值

# 应用 Apriori 算法挖掘频繁项集
frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
print(f"\n频繁项集 (最小支持度: {min_support}):")
print(frequent_itemsets)

# 生成关联规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
print(f"\n关联规则 (最小置信度: {min_confidence}):")
print(rules)

# 展示关联规则结果 (按置信度排序)
sorted_rules = rules.sort_values(by='confidence', ascending=False)
print("\n按置信度排序后的关联规则:")
print(sorted_rules)

# 基于规则的简单推荐
def recommend_items(basket, rules, top_n=5):
    """
    根据关联规则为给定的购物篮推荐商品。

    Args:
        basket (list): 用户购物篮中的商品列表。
        rules (pd.DataFrame): 包含关联规则的 DataFrame。
        top_n (int): 返回推荐的商品数量上限。

    Returns:
        list: 推荐的商品列表。
    """
    recommendations = set()
    for index, rule in rules.iterrows():
        antecedents = set(rule['antecedents'])
        consequents = set(rule['consequents'])

        if antecedents.issubset(basket):
            for item in consequents:
                if item not in basket:
                    recommendations.add(item)

    return list(recommendations)[:top_n]

# 示例用户购物篮
user_basket = ['whole milk', 'rolls/buns']
recommended_items = recommend_items(user_basket, sorted_rules)
print(f"\n当用户购买了 '{user_basket}' 时，推荐商品: {recommended_items}")

user_basket_2 = ['tropical fruit', 'citrus fruit']
recommended_items_2 = recommend_items(user_basket_2, sorted_rules)
print(f"\n当用户购买了 '{user_basket_2}' 时，推荐商品: {recommended_items_2}")