# 分块器

# 使用词性标注语料库开发分块器
# 分块（chunking）是一个可用于执行实体识别的过程。
# 它用于分割和标记句中的多个标识符序列。

import nltk
# 名词短语及其词性
sent=[("A","DT"),("wise", "JJ"), ("small", "JJ"),("girl", "NN"), ("of", "IN"), ("village", "N"),  ("became", "VBD"), ("leader", "NN")]
sent=[("A","DT"),("wise", "JJ"), ("small", "JJ"),("girl", "NN"), ("of", "IN"), ("village", "NN"),  ("became", "VBD"), ("leader", "NN")]

# 分块语法，包括如何进行分块的规则。
grammar = "NP: {<DT>?<JJ>*<NN><IN>?<NN>*}"
find = nltk.RegexpParser(grammar)

# 执行名词短语分块（Noun Phrase Chunking）
res = find.parse(sent)

# 生成解析树
print(res)
res.draw()

# 此处，名词短语的语块规则，即组成方式：
#（1）可选的 DT（限定词），后跟：
#（2）任意数量的 JJ（形容词），再跟：
#（3）一个NN（名词）、可选的IN（介词）以及任意数量的NN
