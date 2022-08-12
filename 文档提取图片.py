
import docx
import os, re

#捕获单个文件中的图片
def get_pictures(word_path, result_path):
    """
    图片提取
    :param word_path: word路径
    :return:
    """
    result_path=result_path+'\\'+word_path.split('\\')[-1]
    os.makedirs(result_path,exist_ok=True)
    try:
        doc = docx.Document(word_path)
        dict_rel = doc.part._rels
        for rel in dict_rel:
            rel = dict_rel[rel]
            if "image" in rel.target_ref:
                img_name = re.findall("/(.*)", rel.target_ref)[0]
                print('img_name0',img_name)
                word_name = os.path.splitext(word_path)[0]
                if os.sep in word_name:
                    new_name = word_name.split('\\')[-1]
                else:
                    new_name = word_name.split('/')[-1]
                img_name = f'{new_name}'+f'{img_name}'
                img_name=img_name.split('/')[-1]
                with open(f'{result_path}/{img_name}', "wb") as f:
                    f.write(rel.target_part.blob)
    except:
        pass


if __name__ == '__main__':
    #获取文件夹下的word文档列表,路径自定义
    dir='E:\python project\pythonProject_draftKG\标准文件\转换文件'
    # os.chdir("E:\\python project\\pythonProject_draftKG\\文件内容抽取")
    spam=os.listdir(dir)
    print(spam)
    result_path='E:\\python project\\pythonProject_draftKG\\文件信息结构化\\文件图片'
    os.makedirs(result_path,exist_ok=True)
    for i in spam:
        get_pictures(dir+'\\'+i,result_path)