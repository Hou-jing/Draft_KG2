import json
import re



#对文件引用和术语部分解析
def Getterm(fname):
    fcont=fdict[fname]['内容']
    conkeys=list(fdict[fname]['内容'].keys())
    referfile=[]#引用文件
    terminology=[]#术语文件
    refercont=''#引用部分内容
    termcont=''#术语部分内容
    for key in conkeys:
        if '引用' in  fcont[key][0] or '规范性引用' in fcont[key][0]:
            for refernum in range(len(fcont[key])):
                refercont+=fcont[key][refernum]
            break
    for key in conkeys:
        if '术语' in fcont[key][0] or '术语和定义' in fcont[key][0] or '定义' in fcont[key][0]:
            for refernum in range(len(fcont[key])):
                termcont+=fcont[key][refernum]
                terminology.extend(fcont[key][0].split('。'))
            break
    sfdic={
        '引用':refercont,
        '术语':termcont
    }
    return sfdic

#对整个文件夹下的文件解析（粗解析）
def ParserDir(flist):
    predic = {}
    for fname in flist:
        sfdic = Getterm(fname)
        predic[fname]=sfdic
    return predic

#对每部分内容，做进一步解析
def Detailparser(predic):
    Detaild={}
    fkeys = list(predic.keys())
    for key in fkeys:
        fdetail={
            '引用':[],
            '术语':[],
            '缩略语':[]
        }
        referpart=predic[key]['引用']
        referp='规范性引用文件.*\\n\s{0,}3|引用文件.*\\n\s{0,}3|引用.*\\n\s{0,}3'
        refercon=re.findall(referp,referpart,re.M|re.S|re.I)

        termpart=predic[key]['术语']
        termp='^\\n\s{0,}\d\s{0,}术语.*|^\\n\s{0,}\d\s{0,}定义.*'
        termcon=re.findall(termp,termpart,re.M|re.S|re.I)
        if refercon:
            refercon=''.join(i for i in refercon)
            fdetail['引用']=refercon.split('\n')
        if termcon:
            termcon=''.join(i for i in termcon)
            #查看有无缩略语
            abbrep='缩略语适用于本标准(.*)'
            abbre=re.findall(abbrep,termcon,re.M|re.S|re.I)
            if abbre:
                fdetail['缩略语'].extend(abbre[0].split('；'))
                termcon=termcon.replace(abbre[0],'')
            fdetail['术语']=termcon.split('\n')
        Detaild[key]=fdetail
    return Detaild

#将抽取的文件内容保存，字典形式
def Savedic(fname,dir_dic):
    fp = open(fname, 'w+', encoding='utf_8')
    json.dump(dir_dic, fp=fp, ensure_ascii=False, indent=1)



if __name__=='__main__':
    base_dir = 'E:\python project\pythonProject_draftKG\文件信息结构化\文件内容'
    fname = 'cont.json'
    fpath = base_dir + '\\' + fname
    fdict = json.load(open(fpath, encoding='utf_8'))
    flist = list(fdict.keys())  # json文件中存放的文件名称
    predic=ParserDir(flist)
    # Savedic(base_dir+'\\'+'term&refer.json',dir_dic=predic)
    Detaildic=Detailparser(predic)
    Savedic(base_dir + '\\' + 'detailterm&refer.json', dir_dic=Detaildic)

