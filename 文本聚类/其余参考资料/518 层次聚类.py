# 层次聚类（Hierarchical Clustering）
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

sp500_px = pd.read_csv('data29.csv.gz', index_col=0)

df = sp500_px.loc[sp500_px.index >= '2011-01-01', ['XOM', 'CVX']]
#################################################################
syms1 = ['AAPL', 'AMZN', 'AXP', 'COP', 'COST', 'CSCO', 'CVX', 'GOOGL', 'HD', 
         'INTC', 'JPM', 'MSFT', 'SLB', 'TGT', 'USB', 'WFC', 'WMT', 'XOM']
df = sp500_px.loc[sp500_px.index >= '2011-01-01', syms1].transpose()

Z = linkage(df, method='complete')
print(Z.shape)
