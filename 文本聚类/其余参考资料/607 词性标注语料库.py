# 创建词性标注语料库

# 一个语料库（集）是多个语料库的集合。
import nltk
import os,os.path

# 在主目录里生成一个数据目录
create = os.path.expanduser('~/nltkdoc')
if not os.path.exists(create):
    os.mkdir(create)
print(os.path.exists(create))

# 如果返回True表示创建了目录，反之，返回False表示尚未创建，我们就需要手动创建它。
import nltk.data
print(create in nltk.data.path)

# 手动创建数据目录后，我们可以再测一下最后一行代码，它将返回True了。
