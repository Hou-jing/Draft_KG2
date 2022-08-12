import json
import re



def Covs_extrac(flist):
    # print(flist)
    # print('-' * 30)
    # print('共有{}篇标准'.format(len(flist)))
    #封面内容提取
    covs={}
    for draftf in flist:
        fcover_=fdict[draftf]['封面'][0]
        print(type(fcover_))
        if type(fcover_)==str:
            if re.findall('\d+\.\d+\\n\\n.*$', fcover_, re.M | re.S | re.I):
                con = re.findall('\d+\.\d+\\n\\n.*$', fcover_, re.M | re.S | re.I)  # 剔除杂信息
                fcover_ = fcover_.replace(con[0], '')
                fcover=re.sub('\d+\.\d+\\n\\n\\n.*','',fcover_)
            else:
                fcover=fcover_
        else:
            fcover=''

        fcon=list(set(fcover.split('\n')))
        fcon = [i for i in fcon if i != '']#去除空值
        covs[draftf]=fcon
    json.dump(covs, fp=open(base_dir+'\\'+'covs.json', 'w+', encoding='utf_8'), ensure_ascii=False, indent=1)#写入封面信息

#中文标准时间信息提取
def Timeexct(covfile):
    fp=json.load(open(covfile,encoding='utf_8',mode='r'))
    timedict={}
    for draftf in flist:
        draftd={
        '发布时间':[],
        '实施时间':[],
        }
        draft='\n'.join(i for i in fp[draftf])
        ppubdate='(\d{4}-\d{2}-\d+)\s{0,}发布'#发布日期，正则匹配：\d{4}-\d{2}-\d+\s?发布
        pimpdate='(\d{4}-\d{2}-\d+)\s{0,}实施' #实施日期，正则匹配：
        pubdate=re.findall(ppubdate,draft,re.M|re.I|re.S)
        if pubdate:
            draftd['发布时间'].append(pubdate[0])
        impdate=re.findall(pimpdate,draft,re.M|re.I|re.S)
        if impdate:
            draftd['实施时间'].append(impdate[0])

        timedict[draftf]=draftd
    return timedict

#中文标准其他信息提取
def Chinese_draftextra(covfile):
    fp = json.load(open(covfile, encoding='utf_8', mode='r'))
    draft_dict = {}
    for draftf in flist:
        draftd = {
            '代替标准': [],
            '标准类型': [],
            '中文标准分类号':[],#http://www.qdifst.org.cn/fuwu/peixun/165.html
            '国际标准分类号':[],#https://www.docin.com/p-1343581846.html#:~:text=InternationalClassificationStandards%20%28ICS%29%E7%BC%96%E7%A0%81%E8%8B%B1%E6%96%87%E5%90%8D%E7%A7%B0%E4%B8%AD%E6%96%87%E5%90%8D%E7%A7%B0%EF%BC%90%EF%BC%91GENERALITIES.TERMINOLOGY.STANDARDIZATION.DOCUMENTATION%E7%BB%BC%E5%90%88%E3%80%81%E6%9C%AF%E8%AF%AD%E5%AD%A6%E3%80%81%E6%A0%87%E5%87%86%E5%8C%96%E3%80%81%E6%96%87%E7%8C%AE%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%92%EF%BC%90Terminology%20%28principlescoordination%29%E6%9C%AF%E8%AF%AD%E5%AD%A6%EF%BC%88%E5%8E%9F%E5%88%99%E5%92%8C%E5%8D%8F%E8%B0%83%E9%85%8D%E5%90%88%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90Vocabularies%E8%AF%8D%E6%B1%87%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%90%EF%BC%91Generalities.Terminology.Standardization.Documentation%20%28Vocabularies%29%E7%BB%BC%E5%90%88%E3%80%81%E6%9C%AF%E8%AF%AD%E5%AD%A6%E3%80%81%E6%A0%87%E5%87%86%E5%8C%96%E3%80%81%E6%96%87%E7%8C%AE%E3%80%80%EF%BC%88%E8%AF%8D%E6%B1%87%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%90%EF%BC%93Sociology.Services.Companyorganizationmanagement.Administration.Transport%20%28Vocabularies%29%E7%A4%BE%E4%BC%9A%E5%AD%A6%E3%80%81%E6%9C%8D%E5%8A%A1%E3%80%81%E5%85%AC%E5%8F%B8%EF%BC%88%E4%BC%81%E4%B8%9A%EF%BC%89%E7%9A%84%E7%BB%84%E7%BB%87%E4%B8%8E%E7%AE%A1%E7%90%86%E3%80%81%E8%A1%8C%E6%94%BF%E3%80%81%E8%BF%90%E8%BE%93%E3%80%80%EF%BC%88%E8%AF%8D%E6%B1%87%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%90%EF%BC%97Mathematics.Naturalsciences%20%28Vocabularies%29%E6%95%B0%E5%AD%A6%E3%80%81%E8%87%AA%E7%84%B6%E7%A7%91%E5%AD%A6%E3%80%80%EF%BC%88%E8%AF%8D%E6%B1%87%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%91%EF%BC%91Healthcaretechnology%20%28Vocabularies%29%E5%8C%BB%E8%8D%AF%E5%8D%AB%E7%94%9F%E6%8A%80%E6%9C%AF%EF%BC%88%E8%AF%8D%E6%B1%87%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%91%EF%BC%93Environmenthealthprotection.Safety%20%28Vocabularies%29%E7%8E%AF%E4%BF%9D%E3%80%81%E4%BF%9D%E5%81%A5%E4%B8%8E%E5%AE%89%E5%85%A8%E3%80%80%EF%BC%88%E8%AF%8D%E6%B1%87%EF%BC%89%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%90%EF%BC%94%EF%BC%90%EF%BC%8E%EF%BC%91%EF%BC%97Metrologymeasurement.Physicalphenomena,%E5%85%B6%E4%BB%96%E5%88%B6%E5%9B%BE%E6%A0%87%E5%87%86%20%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%91%EF%BC%91%EF%BC%90%20Technical%20product%20documentation%20%E6%8A%80%E6%9C%AF%E4%BA%A7%E5%93%81%E6%96%87%E4%BB%B6%20%EF%BC%90%EF%BC%91%EF%BC%8E%EF%BC%91%EF%BC%92%EF%BC%90%20Standardization.
            '标准编号':[],
            '标准中文名':[],
            '标准英文名':[],
            '批准单位':[],
            '发布单位':[],
            '备案号':[]

        }
        draft = '\n'.join(i for i in fp[draftf])
        # print('*'*20)
        # print(draft)
        drafttype=re.findall('.*[行业标准]|[军用标准]|[专项标准]|[国家标准]',draft)#标准类型
        if drafttype:
            draftd['标准类型'].append(drafttype)#查看标准的类型
        draftno=re.findall('\\nGB.*|\\nCMS.*|\\nJB.*|\\nGJB.*',draft)#标准编号
        if draftno:
            draftd['标准编号'].append(draftno)
        draftfabu=re.findall('([\u4e00-\u9fa5]{0,})\s+发布',draft)
        if draftfabu:
            draftd['发布单位'].append(draftfabu)
        draftpizh=re.findall('([\u4e00-\u9fa5]{0,})\s+批准',draft)
        if draftpizh:
            draftd['批准单位'].append(draftpizh)
        draftrepla=re.findall('代\s{0,4}替.*',draft)
        if draftrepla:
            draftd['代替标准'].append(draftrepla[0])
        draftzh=re.findall('\\n[A-Z]\s{0,}\d+\\n|\\nCCS.*\\n',draft)
        if draftzh:
            draftd['中文标准分类号'].append(draftzh)
        draften=re.findall('ICS\s{0,}.*\\n|ICS\s{0,}.*$|CMS.*\\n|ICS.*$|CMS.*$',draft)
        if draftzh:
            draftd['国际标准分类号'].append(draften)

        draftbeian=re.findall('备案号：(.*)\\n',draft)
        if draftbeian:
            draftd['备案号'].append(draftbeian)


        draftl=[i for i in fp[draftf]]
        repeat = []
        for i in draftl:
            # print(i)
            if '行业标准' in i or '军用标准' in i or '专项标准' in i or '国家标准' in i or '发布' in i or '实施' in i or '代替' in i or '批准' in i or '备案号' in i\
                    or 'GB' in i or 'CMS' in i or 'GJB' in i or 'JB' in i:
                repeat.append(i)
        res = list(set(draftl) - set(repeat))
        draftl='\n'.join(i for i in res)
        # print('内容删减后：',draftl)
        draftzhname=re.findall('\\n[\u4e00-\u9fa5][\d]|[\u4e00-\u9fa5].*',draftl)
        if draftzhname:
            draftd['标准中文名'].append(draftzhname)
        draftenname = re.findall('[A-Za-z]{2,}.*', draftl)
        if draftenname:
            draftd['标准英文名'].append(draftenname)
        draft_dict[draftf]=draftd
    return draft_dict


#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)


if __name__=='__main__':
    base_dir = 'E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件内容'
    fname = 'cont.json'#内容

    fpath = base_dir + '\\' + fname
    fdict = json.load(open(fpath, encoding='utf_8'))
    flist = list(fdict.keys())  # json文件中存放的文件名称

    Covs_extrac(flist)
    draft_dict=Chinese_draftextra(covfile=base_dir+'\\'+'covs.json')
    Savedic(base_dir+'\\'+'basic_cov.json',draft_dict)

    timedict=Timeexct(covfile=base_dir+'\\'+'covs.json')
    Savedic(base_dir+'\\'+'time_cov.json',timedict)