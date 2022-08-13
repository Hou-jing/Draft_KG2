#参考博客：https://blog.csdn.net/szfhy/article/details/82696030

import re
from os import listdir

import jieba
import matplotlib.pyplot as plt
import numpy as np

from time import time
from sklearn.datasets import load_files

print("loading documents ...")
t = time()
fdir='E:\python project\pythonProject_draftKG\文件信息结构化\文件文本2\zhdraft'
odir='E:\python project\pythonProject_draftKG\主题聚类'
stoppath='E:\python project\pythonProject_draftKG\主题聚类\chinese'
all_file = listdir(fdir)  # 获取文件夹中所有文件名#数据集地址
outputDir = odir  # 结果输出地址
labels = []  # 用以存储名称
corpus = []  # 空语料库
def buildSW():
    '''停用词的过滤'''
    typetxt = open(stoppath,encoding='utf_8')  # 停用词文档地址
    texts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
    '''停用词库的建立'''
    for word in typetxt:
        word = word.strip()
        texts.append(word)
    return texts


def buildWB(texts):
    '''语料库的建立'''
    for i in range(0, len(all_file)):
        filename = all_file[i]
        filelabel = filename.split('.')[0]
        labels.append(filelabel)  # 名称列表
        file_add = fdir +'\\' +filename  # 数据集地址
        doc = open(file_add, encoding='utf-8').read()
        data = jieba.cut(doc)  # 文本分词
        data_adj = ''
        delete_word = []
        for item in data:
            if item not in texts:  # 停用词过滤
                # value=re.compile(r'^[0-9]+$')#去除数字
                value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
                if value.match(item):
                    data_adj += item + ' '
            else:
                delete_word.append(item)
        corpus.append(data_adj)  # 语料库建立完成
    # print(corpus)
    return corpus


print("done in {0} seconds".format(time() - t))

from sklearn.feature_extraction.text import TfidfVectorizer

max_features = 20000
print("vectorizing documents ...")
t = time()
vectorizer = TfidfVectorizer(max_df=0.4,
                             min_df=2,
                             max_features=max_features,
                             encoding='latin-1')

texts = buildSW()
corpus = buildWB(texts)


X = vectorizer.fit_transform((d for d in corpus))
print("n_samples: %d, n_features: %d" % X.shape)

print("done in {0} seconds".format(time() - t))

from sklearn.cluster import KMeans

print("clustering documents ...")
t = time()
n_clusters = 10
kmean = KMeans(n_clusters=n_clusters,
               max_iter=100,
               tol=0.01,
               verbose=1,
               n_init=3)
kmean.fit(X)
print("kmean: k={}, cost={}".format(n_clusters, int(kmean.inertia_)))
print("done in {0} seconds".format(time() - t))



print("Top terms per cluster:")

order_centroids = kmean.cluster_centers_.argsort()[:, ::-1]

terms = vectorizer.get_feature_names()
for i in range(n_clusters):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()


## 这是两种评价手段，和上述数据无关
from sklearn import metrics

label_true = np.random.randint(1, 4, 6)
label_pred = np.random.randint(1, 4, 6)
print("Adjusted Rand-Index for random sample: %.3f"
      % metrics.adjusted_rand_score(label_true, label_pred))
label_true = [1, 1, 3, 3, 2, 2]
label_pred = [3, 3, 2, 2, 1, 1]
print("Adjusted Rand-Index for same structure sample: %.3f"
      % metrics.adjusted_rand_score(label_true, label_pred))
