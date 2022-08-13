#参考博客：https://blog.csdn.net/weixin_41168304/article/details/122389948


from __future__ import print_function

import os
import re
from multiprocessing import freeze_support

import jieba
from jieba._compat import xrange
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

fdir='E:\python project\pythonProject_draftKG\文件信息结构化\文件文本2\zhdraft'
print('文件总数量为{}'.format(len(os.listdir(fdir))))
stoppath='E:\python project\pythonProject_draftKG\主题聚类\chinese'

#加载数据，数据为[[],[]],二元列表，每个子列表存放每个文件分词后得到的列表
class DataLoad:
    def __init__(self):
        pass
    #将文件内容存储在dataset列表中，每个元素是一篇文件
    def loadDataset(self):
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

    #建立停用词文件
    def buildSW(self):
        '''停用词的过滤'''
        typetxt = open(stoppath,encoding='utf_8')  # 停用词文档地址
        stoptexts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
        '''停用词库的建立'''
        for word in typetxt:
            word = word.strip()
            stoptexts.append(word)
        return stoptexts

    #文件分词，存储在二元列表中，每个子列表是一篇文档
    def buildWB(self,dataset,stoptexts):
        '''语料库的建立'''
        corpus=[]
        for i in range(0, len(dataset)):
            data = jieba.cut(dataset[i])  # 文本分词
            data_adj =[]
            delete_word = []
            for item in data:
                if item not in stoptexts:  # 停用词过滤
                    # value=re.compile(r'^[0-9]+$')#去除数字
                    value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
                    if value.match(item):
                        data_adj.append(item)
                else:
                    delete_word.append(item)
            corpus.append(data_adj)  # 语料库建立完成
        # print(corpus)
        return corpus

Data=DataLoad()
dataset = Data.loadDataset()
stoptexts=Data.buildSW()
data_set=Data.buildWB(dataset,stoptexts)
print('data_set',data_set[:3])
print('data_set的长度是',len(data_set))



#----------------LDA模型-------------------------

import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings

warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

#   构建词典，语料向量化表示
dictionary = corpora.Dictionary(data_set)  # 构建词典
corpus = [dictionary.doc2bow(text) for text in data_set]  #表示为第几个单词出现了几次

num_topics=10
passes=3

ldamodel = LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes,random_state = 1)   #分为10个主题
print('每个主题输出15个单词')
print(ldamodel.print_topics(num_topics=num_topics, num_words=15))  #每个主题输出15个单词
#计算困惑度
def perplexity(num_topics):
    ldamodel = LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=15))
    print(ldamodel.log_perplexity(corpus))
    return ldamodel.log_perplexity(corpus)
#计算coherence
def coherence(num_topics):
    ldamodel = LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes,random_state = 1)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=10))
    ldacm = CoherenceModel(model=ldamodel, texts=data_set, dictionary=dictionary, coherence='u_mass')
    print(ldacm.get_coherence())
    return ldacm.get_coherence()

if __name__ == '__main__':
    freeze_support()
    #绘制主题-coherence曲线，选择最佳主题数
    x = range(1,15)
    # z = [perplexity(i) for i in x]  #如果想用困惑度就选这个
    y = [coherence(i) for i in x]
    plt.plot(x, y)
    plt.xlabel('主题数目')
    plt.ylabel('coherence大小')
    plt.rcParams['font.sans-serif']=['SimHei']
    matplotlib.rcParams['axes.unicode_minus']=False
    plt.title('主题-coherence变化情况')
    plt.show()


    import pyLDAvis.gensim
    # pyLDAvis.enable_notebook()
    data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.save_html(data, '3topic.html')
