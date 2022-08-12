import os
import pathlib
import shutil
from pathlib import Path #用于获取当前目录并遍历路径下所有文件与文件夹
from filecmp import cmp  #cmd（）用于文件比较
#移除重复文件
folder = 'E:\\python project\\pythonProject_draftKG\\标准文件\\转换文件'  #获取当前目录
flist=os.listdir(folder)
for f in flist:
    if "(1)" in f:
        os.remove(folder+'\\'+f)


#移除国军标pdf文件
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


dir = 'E:\\python project\\pythonProject_draftKG\\标准文件'
flist = findPath().getAllPaths(dir)
os.makedirs('E:\\python project\\pythonProject_draftKG\\国军标',exist_ok=True)
newpath='E:\\python project\\pythonProject_draftKG\\国军标'
for fpath in flist:
    if "转换文件" not in fpath:
        if 'GJB' in fpath or 'gjb' in fpath or '军用' in fpath:
            findPath().remove_file(old_path=fpath,new_path=newpath)