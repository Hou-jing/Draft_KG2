
'''
将文件内容，以封面、前言、范围和内容形式存储
'''


import json
import os
import re

import docx
from docx import Document
#word2text（纯文本）
class Word2Txt:
    def __init__(self,dir,resdir):
        self.dir=dir
        self.resdir=resdir#存放转换后的文件
    def File2text(self,fpath,respath):
        doc = Document(fpath)
        newfpath = open(respath, mode='w+', encoding='utf_8')
        for paragraph in doc.paragraphs:
            # print(paragraph.text)
            newfpath.write(paragraph.text)
            newfpath.write('\n')
        print('{}转换成功'.format(fpath.split('\\')[-1]))
    def Dir2text(self):
        for file in os.listdir(self.dir):
            if 'docx' in file:
                self.File2text(self.dir+ '\\' + file,self.resdir+'\\'+file.replace('.docx','.txt'))
#
# 正则：
#封面：^(.*)前\s{0,6}言
#前言：前\s{0,6}言(.*?)1 范围
# 假设标准中最多含有20章。从前言向后，抽取每个章节的内容。
#单个章节的正则抽取表达式：(\d+)\s{1,}.*?\n(\d{1,2})\s
#文件内容分块
def ReExtract(fpath):
    fdic={'封面':[],'前言':[],'范围':[],'内容':{}}
    f=open(fpath,encoding='utf-8',mode='r').read()
    coverp='^(.*?)前\s{0,6}言|'
    prefacep='前\s{0,6}言(.*?)1\s{0,}范围'
    rangep='\d+\s{1,}范围.*?\n\d{1,2}\s'
    conver=re.findall(coverp,f,re.I|re.S|re.M)#封面
    preface = re.findall(prefacep, f, re.I | re.S | re.M)#前言
    rangec=re.findall(rangep,f,re.M|re.I|re.S)#范围
    cover=list(set(conver))
    cover= [i for i in cover if i!='']
    if len(cover)>0:
            fdic['封面'].append(conver[0])
    else:
        cov=re.findall('^.*\n1\s{0,}[\u4e00-\u9fa5]{2,15}',f,re.M|re.S|re.I)
        if cov:
            fdic['封面'].append(cov[0])
    if preface:
        fdic['前言'].append(preface)
    if rangec:
        fdic['范围'].append(rangec)
    #正文内容解析，正则，(\d+)\s{1,}.*?\n(\d{1,2})\s
    #先删除前言部分，在对内容做解析
    body_contp='^.*前\s{0,}言'
    body_cont=re.sub(body_contp,'',f,re.M|re.S|re.I)

    for i in range(2,20):
        bcontp='\n%s\s{1,}.*?\n\d{1,2}\s'%(i)
        cont=re.findall(bcontp,body_cont,re.M|re.I|re.S)
        if cont:
            fdic['内容'][i]=cont
    return fdic

#抽取整个文件夹下的文件
def Extract_event(dir):
    flist=os.listdir(dir)
    dir_dic={}
    for fname in flist:
        if '.txt' in fname:
            fdic=ReExtract(dir+'\\'+fname)
            dir_dic[fname]=fdic
            print(f'{fname}内容已抽取')
    return dir_dic

#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)


# ReExtract(fpath='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\zhdraft\\G1035.txt')




if __name__=='__main__':
    dir = 'E:\\python project\\pythonProject_draftKG\\标准文件\\转换文件'
    resultdir = 'E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\zhdraft'
    wtinp=input('是否需要Word2txt操作(True or False):')
    if wtinp=='True':
        os.makedirs(resultdir,exist_ok=True)
        wt = Word2Txt(dir,resdir=resultdir)
        wt.Dir2text()
        print('完成word2TXT，开始文件内容抽取')

    conbool=input('是否需要进行文件内容块提取（True or False):')
    if conbool=='True':
        dir_dic=Extract_event(dir=resultdir)
        savedir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件内容'
        os.makedirs(savedir,exist_ok=True)
        Savedic(fname=savedir+'\\'+'cont.json',dir_dic=dir_dic)


