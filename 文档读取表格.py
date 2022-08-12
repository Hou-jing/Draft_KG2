import json

import docx
import os, re
from docx import Document
from collections import Counter   #引入Counter


# filename='E:\\python project\\pythonProject_draftKG\\文件内容抽取\\GBT 1.1-2020  标准化工作导则 第1部分：标准化文件的结构和起草规则.docx'


#获取单张表格的内容
def Get_tablecont(tables,tabel_index):
    #单个table的内容
    tabel_cont = []
    tb = tables[tabel_index]
    # 获取表格的行
    tb_rows = tb.rows
    # 读取每一行内容
    for i in range(len(tb_rows)):
        row_data = []
        row_cells = tb_rows[i].cells
        # 读取每一行单元格内容
        for cell in row_cells:
            # 单元格内容
            row_data.append(cell.text)
        tabel_cont.append(row_data)

    thead=tabel_cont[0]#获取表头信息
    b = dict(Counter(thead))#统计表头的重复元素
    repeat_ele=[key for key,value in b.items()if value > 1] #只展示重复元素

    #以字典形式存储表格信息，key=表头，value=表内容
    tdic={}
    i=0
    for item in thead:
        if item in repeat_ele:
            tdic[item+str(i)]=[]#对重复元素通过，添加序号，区别名称
            i+=1
        else:
            tdic[item]=[]
    dkeys=list(tdic.keys())

    for row in tabel_cont[1:]:
        if len(dkeys)>=len(row):
            for cindex in range(len(dkeys)):
                tdic[dkeys[cindex]].append(row[cindex])
        else:
            for cindex in range(len(dkeys)-1,len(row)):#如果，表内容长于表头，则将其存储在表头的最后一个key中。
                tdic[dkeys[len(dkeys)-1]].append(row[cindex])
    return tdic

#获取一个文件里所有的表格内容
def Get_doctable(tables,table_nums):
    nums=[i for i in range(table_nums)]
    doc_cont={}
    for num in nums:
        doc_cont[num]=Get_tablecont(tables,num)
    return doc_cont

#将存放表格内容的字典存储
def Savedict(base_dir,doc_cont,filename):
    fp=open(base_dir+'\\'+filename,'w+',encoding='utf_8')
    json.dump(doc_cont,fp=fp,ensure_ascii=False,indent=1)

#对整个文件夹内的word表格内容提取
def Get_all_tables(base_dir,dir):
    tabelddic={}
    spam=os.listdir(dir)
    for i in spam:
        wordpath=dir+'\\'+i
        doc = Document(wordpath)
        tables = doc.tables
        table_nums = len(tables)
        doc_cont = Get_doctable(tables,table_nums)
        tabelddic[i]=doc_cont

    return tabelddic


if __name__=='__main__':
    base_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件表格'#表格信息存放地址
    dir = 'E:\\python project\\pythonProject_draftKG\\标准文件\\转换文件'#word存放地址
    os.makedirs(base_dir,exist_ok=True)
    tabelddic=Get_all_tables(base_dir,dir)
    Savedict(base_dir,tabelddic,filename='table.json')