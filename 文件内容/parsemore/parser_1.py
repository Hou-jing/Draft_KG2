#对prefice.json做解析
#将标准文件的所有内容，做结构化存储
import json
import re

from ast import literal_eval

base_dir='E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
res_dir='E:\python project\pythonProject_draftKG\文件信息结构化\文件内容\parsermore'
dprefice=json.load(open(base_dir+'\\'+'prefice.json',encoding='utf_8'))#前言部分
drange=json.load(open(base_dir+'\\'+'Range.json',encoding='utf_8'))
trdic=json.load(open(base_dir+'\\'+'detailterm&refer.json',encoding='utf_8'))
cover=json.load(open(base_dir+'\\'+'basic_cov.json',encoding='utf_8'))
Timed=json.load(open(base_dir+'\\'+'time_cov.json',encoding='utf_8'))
cont=json.load(open(base_dir+'\\'+'cont.json',encoding='utf_8'))
Table=json.load(open(base_dir+'\\'+'table.json',encoding='utf_8'))

#前言
def Prefice(fname):
    fd = {
        '提出单位': [],
        '归口单位': [],
        '起草单位': [],
        '起草人': [],
        '其余内容': []
    }
    protunit = dprefice[fname]['提出单位']
    if len(protunit)>0:
        punit = re.findall('由(.*)提出', protunit[0])
        if punit:
            fd['提出单位'].append(punit[0])
    guiunit = dprefice[fname]['归口单位']
    if len(guiunit)>0:
        gunit = re.findall('由(.*)归口', guiunit[0])
        if gunit:
            fd['归口单位'].append(gunit[0])
    qicunit = dprefice[fname]['起草单位']
    if len(qicunit)>0:
        qiunit = re.findall('起草单位:(.*)|起草单位：(.*)', qicunit[0])
        if qiunit:
            qiunit=''.join(i for i in list(qiunit[0]))
            fd['起草单位'].extend(qiunit.split('、'))
    qicper = dprefice[fname]['起草人']
    if len(qicper)>0:
        qiper = re.findall('起草人：(.*)|起草人:(.*)', qicper[0])
        if qiper:
            qiper = ''.join(i for i in list(qiper[0]))
            fd['起草人'].extend(qiper.split('、'))
    fd['其余内容'] = dprefice[fname]['其余内容']
    return fd
#范围
def Range(fname):
    dr = {
        '范围表述': [],
        '范围适用': [],
        '范围不适用': [],
        '其余内容': []
    }
    if len(drange[fname]['范围表述'])>0:
        biaoshu = re.findall('\\n(.*)', drange[fname]['范围表述'][0], re.M | re.S | re.I)
        if biaoshu:
            dr['范围表述'].append(biaoshu[0])
    if len(drange[fname]['范围适用'])>0:
        shiyong = re.findall('适用.*', drange[fname]['范围适用'][0], re.M | re.I | re.S)
        if shiyong:
            dr['范围适用'].append(shiyong[0])
    if len(drange[fname]['范围不适用'])>0:
        bushiyong = re.findall('不适用.*', drange[fname]['范围不适用'][0], re.M | re.S | re.I)
        if bushiyong:
            dr['范围不适用'].append(bushiyong)
    qiyucont = []
    if len(drange[fname]['其余内容'])>0:
        for item in drange[fname]['其余内容']:
            if re.findall('[\u4e00-\u9fa5]{1,}', item):
                qiyucont.append(item)
        dr['其余内容'] = qiyucont
    return dr
#术语和引用
def TermRefer(fname):
    refter = {}
    refre = trdic[fname]['引用']
    term = ''.join(i for i in trdic[fname]['术语'])
    suoc = trdic[fname]['缩略语']
    refs, tems, suo = [], [], []
    for file in refre:
        if re.findall('[A-Z]{2,5}.*', file):
            refs.append(re.findall('[A-Z]{2,5}.*', file)[0])
    # 术语
    terms = re.findall('[\u4e00-\u9fa5]{2,}\s{0,}[a-z]{2,}.*?。', term, re.M | re.S | re.I)
    if terms:
        tems = terms
    # 缩略语
    for item in suoc:
        item_ = re.findall('\\n(.*[\u4e00-\u9fa5]{2,})', item)
        if item_:
            suo.append(item_)

    refter['引用'] = refs
    refter['术语'] = tems
    refter['缩略语'] = suo
    return refter

#封面
def Cover(fname):
    fcovdic = {
        '代替标准': [],
        '标准类型': [],
        '中文分类号': [],
        '国际分类号': [],
        '标准编号': [],
        '批准单位': [],
        '发布单位': [],
        '备案号': []
    }
    fcover = cover[fname]
    if len(fcover['代替标准']) > 0:
        fcovdic['代替标准'].append(re.findall('代替(.*)', fcover['代替标准'][0])[0])
    if len(fcover['标准类型']) > 0:
        for i in fcover['标准类型']:
            if '行业标准' in i:
                fcovdic['标准类型'].append('行业标准')
                break
            elif '军用标准' in i:
                fcovdic['标准类型'].append('军用标准')
                break
            elif '专项标准' in i:
                fcovdic['标准类型'].append('专项标准')
                break
            elif '国家标准' in i:
                fcovdic['标准类型'].append('国家标准')
                break

    if len(fcover['中文标准分类号']) > 0:
        fcovdic['中文分类号'].append(fcover['中文标准分类号'][0][0].replace('\n', ''))
    if len(fcover['国际标准分类号']) > 0:
        if len(fcover['国际标准分类号'][0])>0:
            fcovdic['国际分类号'].append(fcover['国际标准分类号'][0][0].replace('\n', ''))
    if len(fcover['标准编号']) > 0:
        for con in fcover['标准编号'][0]:
            conord = con.replace('\n', '')
            if re.findall('[\u4e00-\u9fa5]{2,}', conord):
                pass
            else:
                fcovdic['标准编号'].append(conord)



    return fcovdic

#封面中的中英文名称
base_dir = 'E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
titledic = {}
titles = open('new_title.txt', encoding='utf_8', mode='r').readlines()
itemli = []
itemli2 = []  # 存name
pre2 = []  # 存类别
for item in titles:
    item_ = literal_eval(item)
    t = item_[0]
    if '\n' in t or '\t' in t:
        t_ = t.replace('\n', '').replace('\t', '')
    else:
        t_ = t
    c = item_[1]
    titledic[t] = c
    itemli.append(item_)
    itemli2.append(t_)
    pre2.append(str(c))

def Name(fname):

    zh_name = cover[fname]['标准中文名']
    zh = []
    if len(zh_name) > 0:
        for name in zh_name[0]:
            if name.replace('\n', '').replace('\t', '') in itemli2:
                ind = itemli2.index(name.replace('\n', '').replace('\t', ''))
                if pre2[ind] == '1':
                    zh.append(name.replace('\n', '').replace('\t', ''))
    zname = ''.join(i for i in zh)

    en_name = cover[fname]['标准英文名']
    en = []
    if len(en_name) > 0:
        for name in en_name[0]:
            if name.replace('\n', '').replace('\t', '') in itemli2:
                ind = itemli2.index(name.replace('\n', '').replace('\t', ''))
                if pre2[ind] == '1':
                    en.append(name.replace('\n', '').replace('\t', ''))
    ename = ''.join(i for i in en)
    fnamed = {
        '中文名': zname,
        '英文名': ename
    }
    return fnamed

#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)
flist=list(dprefice.keys())
newprefice={}
for fname in flist:
    fnamed=Name(fname)
    pre=Prefice(fname)
    ran=Range(fname)
    ter=TermRefer(fname)
    cov=Cover(fname)
    timed=Timed[fname]
    contd=cont[fname]['内容']
    table=Table[fname.replace('.txt','.docx')]
    # print(timed)
    fd={
        '名称':fnamed,
        '前言部分':pre,
        '范围部分':ran,
        '术语部分':ter,
        '封面部分':cov,
        '日期部分':timed,
        '内容部分':contd,
        '表格部分':table
    }
    newprefice[fname]=fd
Savedic(base_dir+'\\'+'newcont.json',newprefice)



