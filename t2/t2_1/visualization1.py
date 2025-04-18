import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
import networkx as nx

# 加载您的数据集
file_path = r'C:\Users\qiqi\OneDrive\Desktop\code\pythonweb\t2\Groceries_dataset.csv'
df = pd.read_csv(file_path)

# 将数据按 Member_number 分组，获取每个用户的购物篮
transactions = df.groupby('Member_number')['itemDescription'].apply(list).tolist()

# 数据预处理
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# 设置最小支持度和最小置信度
min_support = 0.01
min_confidence = 0.2

# 应用 Apriori 算法挖掘频繁项集
frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

# 生成关联规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

# 创建网络图
G = nx.DiGraph()

# 添加节点 (商品)
for item in df_encoded.columns:
    G.add_node(item)

# 添加边 (关联规则)
for index, row in rules.iterrows():
    antecedents = tuple(row['antecedents'])
    consequents = tuple(row['consequents'])
    confidence = row['confidence']
    lift = row['lift']

    # 为了简化图，我们只添加前件和后件都只有一个商品的规则
    if len(antecedents) == 1 and len(consequents) == 1:
        u = antecedents[0]
        v = consequents[0]
        G.add_edge(u, v, confidence=confidence, lift=lift)

# 设置节点大小和颜色
node_size = [len(list(G.neighbors(node))) * 50 for node in G.nodes()]
node_color = 'lightblue'

# 设置边宽度和颜色
edge_width = [d['confidence'] * 5 for u, v, d in G.edges(data=True)]
edge_alpha = 0.5
edge_color = 'gray'

# 绘制网络图
pos = nx.spring_layout(G, k=0.5, iterations=50)  # 可以尝试不同的布局算法
plt.figure(figsize=(15, 15))
nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_color,
        width=edge_width, edge_color=edge_color, alpha=edge_alpha,
        font_size=10, font_weight='bold', arrowsize=20)
plt.title("Association Rules Network Graph (Confidence as Edge Width)")
plt.show()

# 可以创建另一个网络图，边的颜色表示 Lift
G_lift = nx.DiGraph()
for item in df_encoded.columns:
    G_lift.add_node(item)
for index, row in rules.iterrows():
    antecedents = tuple(row['antecedents'])
    consequents = tuple(row['consequents'])
    confidence = row['confidence']
    lift = row['lift']
    if len(antecedents) == 1 and len(consequents) == 1:
        u = antecedents[0]
        v = consequents[0]
        G_lift.add_edge(u, v, confidence=confidence, lift=lift)

edge_colors = [d['lift'] for u, v, d in G_lift.edges(data=True)]
pos_lift = nx.spring_layout(G_lift, k=0.5, iterations=50)
plt.figure(figsize=(15, 15))
nx.draw(G_lift, pos_lift, with_labels=True, node_size=node_size, node_color=node_color,
        width=edge_width, edge_color=edge_colors, edge_cmap=plt.cm.viridis, alpha=0.5,
        font_size=10, font_weight='bold', arrowsize=20)
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(edge_colors), vmax=max(edge_colors)))
sm.set_array([])
cbar = plt.colorbar(sm, label='Lift')
plt.title("Association Rules Network Graph (Lift as Edge Color)")
plt.show()