监督方式：标注语料（18条）
测试效果：
## 模型预测效果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/215d6d57583c4e59a2a7f3815648f3ea.png)
## 分词系统效果：
[http://thulac.thunlp.org/demo](http://thulac.thunlp.org/demo)
![在这里插入图片描述](https://img-blog.csdnimg.cn/96901317e7b349688904e3e0dde8c8e4.png)
## 全部语料
![在这里插入图片描述](https://img-blog.csdnimg.cn/da56024e1cce454c81255d73a9aca37c.png)


## 总结
可以看到，分词工具会降低词的紧密性。
在现有论文中，领域词典构建多是无监督下的方式，采用词频、TF-IDF值等统计词信息，迭代构建领域词典。
本次，主要依据NER的主要思路，接近苏剑林老师的global pointer的方法，完成了模型训练和预测工作。
从结果来看，预测的准确率还可，但是，全面性降低，应该是和语料数量有关。
整个训练了10epoch，loss并没有收敛，就终止了训练。
本机项目地址为：E:\python project\pythonProject_draftKG\词典尝试
