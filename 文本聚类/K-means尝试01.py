#!--encoding=utf-8
#参考博文：https://www.cnblogs.com/fengfenggirl/p/k-means.html

from __future__ import print_function

import os
import re

import jieba
from jieba._compat import xrange
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

fdir='E:\python project\pythonProject_draftKG\文件信息结构化\文件文本2\zhdraft'
print('文件总数量为{}'.format(len(os.listdir(fdir))))
stoppath='E:\python project\pythonProject_draftKG\主题聚类\chinese'
def loadDataset():
    '''导入文本数据集'''
    flist=os.listdir(fdir)
    dataset = []
    for fname in flist:
        f = open(fdir+'\\'+fname, 'r',encoding='utf_8')
        d=''
        for line in f.readlines():
            if line!='\n' and line!='':
                d+=line
        dataset.append(d)
        f.close()
    return dataset

#停用词建立
def buildSW():
    '''停用词的过滤'''
    typetxt = open(stoppath,encoding='utf_8')  # 停用词文档地址
    stoptexts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
    '''停用词库的建立'''
    for word in typetxt:
        word = word.strip()
        stoptexts.append(word)
    return stoptexts

#语料建立data_set=[doc1,doc2,...]
def buildWB(dataset,stoptexts):
    '''语料库的建立'''
    corpus=[]
    for i in range(0, len(dataset)):
        data = jieba.cut(dataset[i])  # 文本分词
        data_adj = ''
        delete_word = []
        for item in data:
            if item not in stoptexts:  # 停用词过滤
                # value=re.compile(r'^[0-9]+$')#去除数字
                value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
                if value.match(item):
                    data_adj += item + ' '
            else:
                delete_word.append(item)
        corpus.append(data_adj)  # 语料库建立完成
    # print(corpus)
    return corpus

def transform(dataset, n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer


def train(X, vectorizer, true_k=10, minibatch=False, showLable=False):
    # 使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X))
    print('Cluster distribution:')
    print(dict([(i, result.count(i)) for i in result]))
    return -km.score(X)

#测试在不同的聚类数设置下，可达到的效果
def test():
    '''测试选择最优参数'''
    dataset = loadDataset()
    print("%d documents" % len(dataset))
    X, vectorizer = transform(dataset, n_features=500)
    true_ks = []
    scores = []
    for i in xrange(3, 80, 1):
        score = train(X, vectorizer, true_k=i) / len(dataset)
        print(i, score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def out():
    '''在最优参数下输出聚类结果'''
    dataset = loadDataset()
    stoptexts=buildSW()
    corpus=buildWB(dataset,stoptexts)

    X, vectorizer = transform(corpus, n_features=500)
    score = train(X, vectorizer, true_k=5,minibatch=True, showLable=True) / len(dataset)
    print(score)


# test()
out()
