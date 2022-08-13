# 分块器：消除部分语块

#分块是语块的一部分被消除的过程。操作方式可以是：
#（1）使用整个语块；
#（2）使用语块中间的一部分并删除剩余的部分；
#（3）使用语块从开始或结尾截取的一部分并删除剩余的部分。


import nltk

# 此处，我们用任意数量的名词，构建名词短语的分块规则
noun1=[("financial","NN"),("year","NN"),("account","NN"),("summary","NN")]
gram="NP:{<NN>+}"

# 使用【函数nltk.RegexpParser(规则)】执行分块和解析
# 英语Parser就是解析器的意思。
find = nltk.RegexpParser(gram)
print(find.parse(noun1))

# 以解析树的形式输出结果
x=find.parse(noun1)
x.draw()
