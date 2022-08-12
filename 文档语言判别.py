import os
import shutil

import langid
import re


#检查语言
import pandas as pd


def check_language(string: str) -> str:
    """检查语言
    :return zh:中文,en:英文,
    """
    new_string = re.sub(r'[0-9]+', '', string)  # 这一步剔除掉文本中包含的数字
    return langid.classify(new_string)[0]

# print(check_language('E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\otherdraft'))
#移动文件
class findPath:
    def __init__(self):
        self.fileList = []

    def gci(self, filepath):
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                self.gci(fi_d)
            else:
                self.fileList.append(fi_d)

    def getAllPaths(self, filepath):
        self.gci(filepath)
        return self.fileList



    def remove_file(self,old_path, new_path):
        src = old_path
        dst = new_path
        shutil.move(src, dst)

flange=[]
if __name__ == '__main__':
    base_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本'
    zh_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\zhdraft'
    en_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\endraft'
    other_dir='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件文本2\\otherdraft'
    os.makedirs(zh_dir,exist_ok=True)
    os.makedirs(en_dir,exist_ok=True)
    os.makedirs(other_dir,exist_ok=True)
    flist=os.listdir(base_dir)
    for fname in flist:
        if '.txt' in fname:
            f=open(base_dir+'\\'+fname,encoding='utf_8').read()
            bcontp = '\n%s\s{1,}.*?\n\d{1,2}\s' % (2)
            fcon=re.findall(bcontp,f,re.M|re.S|re.I)
            if fcon:
                lang=check_language(fcon[0])
                if lang=='zh':
                    findPath().remove_file(old_path=base_dir+'\\'+fname, new_path=zh_dir)
                    flange.append((fname,'zh'))
                elif lang=='en':
                    findPath().remove_file(old_path=base_dir+'\\'+fname,new_path=en_dir)
                    flange.append((fname,'en'))
                else:
                    findPath().remove_file(old_path=base_dir+'\\'+fname,new_path=other_dir)
                    flange.append((fname,'other'))
            else:
                findPath().remove_file(old_path=base_dir + '\\' + fname, new_path=other_dir)
                flange.append((fname, 'other'))
    df=pd.DataFrame(flange,columns=['file','lang'])
    df.to_csv(base_dir+'\\'+'flang.csv',mode='w+',encoding='utf_8')
    print(flange)