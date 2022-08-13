# K均值算法（K-Means Algorithm）
# 包scikit-learn的算法默认重复10次（n_init），而参数max_iter用于控制迭代次数。

import pandas as pd
from sklearn.cluster import KMeans

sp500_px = pd.read_csv('data29.csv.gz', index_col=0)

syms = sorted(['AAPL', 'MSFT', 'CSCO', 'INTC', 'CVX', 'XOM', 'SLB', 'COP', 
               'JPM', 'WFC', 'USB', 'AXP', 'WMT', 'TGT', 'HD', 'COST'])
top_sp = sp500_px.loc[sp500_px.index >= '2011-01-01', syms]
kmeans = KMeans(n_clusters=5).fit(top_sp)

print(top_sp)
print(kmeans)
