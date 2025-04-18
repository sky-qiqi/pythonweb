import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import numpy as np

# 加载您的数据集 (与之前相同)
file_path = r'C:\Users\qiqi\OneDrive\Desktop\code\pythonweb\t2\Groceries_dataset.csv'
df = pd.read_csv(file_path)
transactions = df.groupby('Member_number')['itemDescription'].apply(list).tolist()
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)
min_support = 0.01
min_confidence = 0.2
frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

# 为了使图表更易读，我们选择置信度最高的 10 条规则进行可视化
top_n = 10
rules_top = rules.sort_values(by='confidence', ascending=False).head(top_n)

# 准备数据 для平行坐标图
data_for_plot = []
for index, row in rules_top.iterrows():
    antecedents = ", ".join(list(row['antecedents']))
    consequents = ", ".join(list(row['consequents']))
    data_for_plot.append({
        'rule': f"{antecedents} -> {consequents}",
        'support': row['support'],
        'confidence': row['confidence'],
        'lift': row['lift']
    })
df_plot = pd.DataFrame(data_for_plot)

# 绘制平行坐标图
plt.figure(figsize=(10, 8))
parallel_coordinates(df_plot, 'rule', color=('#556270', '#4ECDC4', '#C7F464'))
plt.title(f'Top {top_n} Association Rules (Parallel Coordinates)')
plt.xlabel('Rule Metrics')
plt.ylabel('Value')
plt.xticks(range(3), ['Support', 'Confidence', 'Lift'])
plt.grid(True)
plt.legend(loc='best')
plt.show()