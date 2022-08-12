#对标准前言内容做规范化处理
import json
import re


#单个文件的前言部分解析
def Prefice(fname):
    Preficedic={
        '提出单位':[],
        '归口单位':[],
        '起草单位':[],
        '起草人':[],
        '其余内容':[]
    }
    prefice=''
    for i in fdict[fname]['前言']:
        prefice='。'.join(i)
    # print(prefice)
    prefice=prefice.split('。')
    for item in prefice:
        if '提出' in item:
            Preficedic['提出单位'].append(item)
        elif '归口' in item:
            Preficedic['归口单位'].append(item)
        elif '起草单位' in item:
            Preficedic['起草单位'].append(item)
        elif '起草人' in item:
            Preficedic['起草人'].append(item)
        else:
            Preficedic['其余内容'].append(item)

    return Preficedic


#整个文件夹下的前言部分解析
def Dirprefice(flist):
    predic={}
    for fname in flist:
        Preficedic=Prefice(fname)
        predic[fname]=Preficedic
    return predic

#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)


#对单个标准的范围部分解析
def Range(fname):
    frange={
        '范围表述':[],
        '范围适用':[],
        '范围不适用':[],
        '其余内容':[]
    }
    srange=[]
    if len(fdict[fname]['范围'])>0:
        for item in fdict[fname]['范围'][0]:

            con=re.findall('^1.*$',item,re.M|re.S|re.I)
            if con:
                srange.append(con[0])


    rangecont=''
    for item in srange:
            rangecont=item+'。'
    rangecont=rangecont.split('。')
    # print(rangecont)
    for sent in rangecont:
        if '确立了' in sent or '规定了' in sent or '给出了' in sent or '界定了' in sent:
            frange['范围表述'].append(sent)
        elif '适用于' in sent:
            frange['范围适用'].append(sent)
        elif '不适用于' in sent:
            frange['范围不适用'].append(sent)
        else:
            frange['其余内容'].append(sent)

    return frange

#对整个文件夹下的范围部分解析
def Dirrange(flist):
    drange={}
    for fname in flist:
        frange=Range(fname)
        # print(frange)
        drange[fname]=frange
    return drange



if __name__=='__main__':
    base_dir = 'E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
    fname = 'cont.json'
    fpath = base_dir + '\\' + fname
    fdict = json.load(open(fpath, encoding='utf_8'))
    flist = list(fdict.keys())  # json文件中存放的文件名称

    predic=Dirprefice(flist)#前言部分
    drange=Dirrange(flist)#范围部分

    Savedic(base_dir+'\\'+'prefice.json',predic)
    Savedic(base_dir+'\\'+'Range.json',drange)
