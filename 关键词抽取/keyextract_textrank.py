#!/usr/bin/python
# coding=utf-8
# 采用TextRank方法提取文本关键词
import os
import sys
import pandas as pd
import jieba.analyse
"""
       TextRank权重：

            1、将待抽取关键词的文本进行分词、去停用词、筛选词性
            2、以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
            3、计算图中节点的PageRank，注意是无向带权图
"""

# 处理标题和摘要，提取关键词
def getKeywords_textrank(dir,topK):
    fdir = os.listdir(dir)
    ids,keys=[],[]
    for fname in fdir:
        fp = open(dir + '\\' + fname, encoding='utf_8', mode='r').read()
        jieba.analyse.set_stop_words('E:\python project\pythonProject_draftKG\关键词抽取\stopWord.txt')  # 加载自定义停用词表
        text = fp
        keywords = jieba.analyse.textrank(text, topK=topK)  # TextRank关键词提取，词性筛选
        word_split = " ".join(keywords)
        print(word_split)
        keys.append(word_split)
        ids.append(fname)
    result = pd.DataFrame({"fname": ids,"key": keys}, columns=['fname', 'key'])
    return result

def main():
    dir = 'E:\python project\pythonProject_draftKG\文件信息结构化\文件文本2\zhdraft'

    result = getKeywords_textrank(dir,10)
    result.to_csv("keys_TextRank.csv",index=False)

if __name__ == '__main__':
    main()
