# Draft_KG2
整个过程面向标准PDF文件，构建知识图谱。
整个过程大致分为3部分：一是PDF可编辑转换，二是结构化信息提取，三是图谱构建。
为了保证整个文件的内容无缺失性，在构造中，将文件内容分为纯文本、表格、图片三部分，分类整理。
内容结构框架如下，其中，中英文名称识别，采用了bert二分类的方式（效果还可以）。
在范围内容整理时，参考了标准导则中的编写规则，如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/50b0514f7c644853919754612a565f77.png)
### 内容部分
![在这里插入图片描述](https://img-blog.csdnimg.cn/682908cc6e43440c911a8875bd330c64.png)
## 程序执行
1.	

GJBremove.py——移除国军标文件

pdf2word.py

文档提取图片.py

文档读取表格.py

2.	

文档内容提取.py——先word2TXT

文档语言判别.py——判断标准是中文or外文

文档内容提取.py——在extract(分章节和模块粗提取)

封面结构化信息提取.py

文档术语提取.py

标准前言信息提取.py

图片链接生成.py

3.	

parser_1.py——对上述结构化信息再整理

4.	
图谱搭建.py

## 技术路线
![在这里插入图片描述](https://img-blog.csdnimg.cn/3859292427624dbc9d54cd142c3d63de.png)
## 本体构建
![在这里插入图片描述](https://img-blog.csdnimg.cn/ff87ac020bb94e929e8ea0c8ea3afb5e.png)
![请添加图片描述](https://img-blog.csdnimg.cn/a2d856a316c3428ab1962378acaec2d6.png)

## 图谱效果
### 单个标准文件
![请添加图片描述](https://img-blog.csdnimg.cn/07ffacfad65a41419d4e036fa3aeea22.png)
### 标准与标准之间
![请添加图片描述](https://img-blog.csdnimg.cn/85ab1288ba1f4b94b452a05252c0ec80.png)
git地址：
本机地址：E:\python project\pythonProject_draftKG\文件信息结构化
