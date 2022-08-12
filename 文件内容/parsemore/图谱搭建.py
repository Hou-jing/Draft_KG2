import ast
import json
import time

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph(
        "http://localhost:7474",
        auth=('neo4j', '123456')
    )
graph.delete_all()#根据标准名去除重复行

base_dir='E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
def Savecsv(fpath):
    fp = json.load(open(base_dir + '\\' + 'newcont.json', encoding='utf_8'))
    flist = list(fp.keys())
    Imgurl = json.load(open(base_dir + '\\' + 'imgurl.json', encoding='utf_8'))
    fnames,zhnames,ennames,prounit,guikouunit,draftunit=[],[],[],[],[],[]
    draftper,prefacecon,range_1,range_2,range_3,range_4=[],[],[],[],[],[]
    term_1,term_2,term_3=[],[],[]
    cover_daiti,cover_type,cover_zhcls,cover_encls,cover_bianh=[],[],[],[],[]
    cover_piz,cover_fab,cover_beian=[],[],[]
    date_fabu,date_shish=[],[]
    contpart,tablepart=[],[]
    imgurl=[]
    for fname in flist:
        fnames.append(fname)
        zhnames.append(fp[fname]['名称']['中文名'])
        ennames.append(fp[fname]['名称']['英文名'])
        prounit.append(fp[fname]['前言部分']['提出单位'])
        guikouunit.append(fp[fname]['前言部分']['归口单位'])
        draftunit.append(fp[fname]['前言部分']['起草单位'])
        draftper.append(fp[fname]['前言部分']['起草人'])
        prefacecon.append(fp[fname]['前言部分']['其余内容'])
        range_1.append(fp[fname]['范围部分']['范围表述'])
        range_2.append(fp[fname]['范围部分']['范围适用'])
        range_3.append(fp[fname]['范围部分']['范围不适用'])
        range_4.append(fp[fname]['范围部分']['其余内容'])
        term_1.append(fp[fname]['术语部分']['引用'])
        term_2.append(fp[fname]['术语部分']['术语'])
        term_3.append(fp[fname]['术语部分']['缩略语'])
        cover_daiti.append(fp[fname]['封面部分']['代替标准'])
        cover_type.append(fp[fname]['封面部分']['标准类型'])
        cover_zhcls.append(fp[fname]['封面部分']['中文分类号'])
        cover_encls.append(fp[fname]['封面部分']['国际分类号'])
        cover_bianh.append(fp[fname]['封面部分']['标准编号'])
        cover_piz.append(fp[fname]['封面部分']['批准单位'])
        cover_fab.append(fp[fname]['封面部分']['发布单位'])
        cover_beian.append(fp[fname]['封面部分']['备案号'])
        date_fabu.append(fp[fname]['日期部分']['发布时间'])
        date_shish.append(fp[fname]['日期部分']['实施时间'])
        contpart.append(fp[fname]['内容部分'])
        tablepart.append(fp[fname]['表格部分'])
        if fname.replace('.txt','.docx') in list(Imgurl.keys()):
            imgurl.append(Imgurl[fname.replace('.txt','.docx')])
        else:
            imgurl.append([])

    df=pd.DataFrame(
        [fnames,zhnames,ennames,prounit,guikouunit,draftunit,
         draftper,prefacecon,range_1,range_2,range_3,range_4,
         term_1,term_2,term_3,
         cover_daiti,cover_type,cover_zhcls,cover_encls,cover_bianh,
         cover_piz, cover_fab, cover_beian,
         date_fabu,date_shish,
         contpart,tablepart,
         imgurl
         ],
        index=['存储文件名称','中文名','英文名', '提出单位','归口单位','起草单位',
               '起草人','其余内容', '范围表述','范围适用','范围不适用','其余内容',
                 '引用','术语','缩略语',
               '代替标准','标准类型','中文分类号','国际分类号','标准编号',
               '批准单位', '发布单位', '备案号', '发布时间', '实施时间', '内容部分', '表格部分',
               '图片链接'
                 ]
    )
    df=df.T
    df.to_csv(fpath,encoding='utf_8',index=False)



matcher=NodeMatcher(graph)

#判断起草人和起草单位，避免重复设立节点
def Judge_Exist(value,relname):
    if value != None and value!='[]' and value!="['']":
        if type(value) != float:
            try:
                dunit_ = ast.literal_eval(value)
                for j in range(len(dunit_)):
                    nodelist = list(matcher.match(relname, name=dunit_[j]))
                    if len(nodelist) > 0:  # 判断这个节点是否建立过
                        rel_dunit = Relationship(draft, relname, nodelist[0])
                        graph.create(rel_dunit)
                    else:
                        unit = Node(relname, name=dunit_[j])
                        graph.create(unit)
                        rel_dunit = Relationship(draft, relname, unit)
                        graph.create(rel_dunit)
            except Exception as e:
                pass

def Judge_Exist_list(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            # dunit_ = ast.literal_eval(value)
            dunit_=value
            for j in range(len(dunit_)):
                nodelist = list(matcher.match(relname, name=dunit_[j]))
                if len(nodelist) > 0:  # 判断这个节点是否建立过
                    rel_dunit = Relationship(draft, relname, nodelist[0])
                    graph.create(rel_dunit)
                else:
                    unit = Node(relname, name=dunit_[j])
                    graph.create(unit)
                    rel_dunit = Relationship(draft, relname, unit)
                    graph.create(rel_dunit)

def Judge_Exist_str(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            # dunit_ = ast.literal_eval(value)
            dunit_=value

            nodelist = list(matcher.match(relname, name=dunit_))
            if len(nodelist) > 0:  # 判断这个节点是否建立过
                rel_dunit = Relationship(draft, relname, nodelist[0])
                graph.create(rel_dunit)
            else:
                unit = Node(relname, name=dunit_)
                graph.create(unit)
                rel_dunit = Relationship(draft, relname, unit)
                graph.create(rel_dunit)

def Judge_Existjson(value,relname):
    if value != None:
        if type(value) != float:
            ditems = ast.literal_eval(value)
            item_nums=list(ditems.keys())
            if len(list(ditems.keys()))>0:#匹配相关内容
                for itemkey in list(ditems.keys()):
                    # print(int(itemkey))
                    # print(ditems[itemkey][0])
                    contnd=Node('内容',name='第{}章内容'.format(int(itemkey)),cont=str(ditems[itemkey]))
                    graph.create(contnd)
                    rel_dunit = Relationship(draft,'第{}章内容'.format(int(itemkey)) ,contnd)
                    graph.create(rel_dunit)


if __name__ == '__main__':
    Savecsv(fpath='newcont.csv')
    con_dir = 'E:\python project\pythonProject_draftKG\文件信息结构化\文件内容\parsermore'
    df = pd.read_csv(con_dir + '\\' + 'newcont.csv', encoding='utf_8', header=0)
    # df.fillna(value="未知",inplace=True)
    # df=df.replace('[]','空值').replace('['']','空值').replace('{}','空值')
    # print(df.head(5))
    fnames, zhnames, ennames, prounit, guikouunit, draftunit = df['存储文件名称'], df['中文名'], df['英文名'], df['提出单位'], df[
        '归口单位'], df['起草单位']
    draftper, prefacecon, range_1, range_2, range_3, range_4 = df['起草人'], df['其余内容'], df['范围表述'], df['范围适用'], df[
        '范围不适用'], df['其余内容']
    term_1, term_2, term_3 = df['引用'], df['术语'], df['缩略语']
    cover_daiti, cover_type, cover_zhcls, cover_encls, cover_bianh = df['代替标准'], df['标准类型'], df['中文分类号'], df['国际分类号'], \
                                                                     df['标准编号']

    cover_piz, cover_fab, cover_beian = df['批准单位'], df['发布单位'], df['备案号']

    date_fabu, date_shish = df['发布时间'], df['实施时间']

    contpart, tablepart = df['内容部分'], df['表格部分']
    imgpart = df['图片链接']

    zhnames.fillna(value='空值', inplace=True)
    ennames.fillna(value='空值', inplace=True)


    #图谱构建
    #起草单位关系创建
    for i in range(0,len(fnames)):
        nodelist=list(matcher.match('标准名',name=fnames[i],zhname=zhnames[i],enname=ennames[i],bianhao=cover_bianh[i][0],type=cover_type[i][0],
                                    zhclas=cover_zhcls[i][0],enclas=cover_encls[i][0],beian=cover_beian[i][0]))
        if len(nodelist)>0:
            draft=nodelist[0]
            matcher=NodeMatcher(graph)
            Judge_Exist(draftunit[i],'起草单位')
            Judge_Exist(draftper[i],'起草人')
            Judge_Exist(guikouunit[i], '归口单位')
            Judge_Exist(prounit[i],'提出单位')
            Judge_Exist(cover_piz[i],'批准单位')
            Judge_Exist(cover_fab[i],'发布单位')
            Judge_Exist(prefacecon[i],'前言其余内容')
            Judge_Exist(range_1[i],'范围表述')
            Judge_Exist(range_2[i],'范围适用')
            Judge_Exist(range_3[i],'范围不适用')
            Judge_Exist(range_4[i],'范围其余内容')
            Judge_Exist(term_1[i],'引用')
            Judge_Exist(term_2[i],'术语')
            Judge_Exist(term_3[i],'缩略语')
            Judge_Exist(cover_daiti[i],'代替标准')
            Judge_Exist(date_fabu[i],'发布时间')
            Judge_Exist(date_shish[i],'实施时间')
            Judge_Existjson(contpart[i],'内容部分')
            Judge_Existjson(tablepart[i],'表格部分')
            Judge_Exist(imgpart[i],'图片链接')
        else:
            draftname=Node('标准名',name=fnames[i],zhname=zhnames[i],enname=ennames[i],bianhao=cover_bianh[i][0],type=cover_type[i][0],
                                    zhclas=cover_zhcls[i][0],enclas=cover_encls[i][0],beian=cover_beian[i][0])
            graph.create(draftname)
            draft=draftname
            time.sleep(0.2)
            print('创建名为{}的节点'.format(fnames[i]))
            Judge_Exist(draftunit[i], '起草单位')
            Judge_Exist(draftper[i], '起草人')
            Judge_Exist(guikouunit[i], '归口单位')
            Judge_Exist(prounit[i], '提出单位')
            Judge_Exist(cover_piz[i], '批准单位')
            Judge_Exist(cover_fab[i], '发布单位')
            Judge_Exist(prefacecon[i], '前言其余内容')
            Judge_Exist(range_1[i], '范围表述')
            Judge_Exist(range_2[i], '范围适用')
            Judge_Exist(range_3[i], '范围不适用')
            Judge_Exist(range_4[i], '范围其余内容')
            Judge_Exist(term_1[i], '引用')
            Judge_Exist(term_2[i], '术语')
            Judge_Exist(term_3[i], '缩略语')
            Judge_Exist(cover_daiti[i], '代替标准')
            Judge_Exist(date_fabu[i], '发布时间')
            Judge_Exist(date_shish[i], '实施时间')
            Judge_Existjson(contpart[i], '内容部分')
            Judge_Existjson(tablepart[i], '表格部分')
            Judge_Exist(imgpart[i], '图片链接')
