>因为需要对文件的主题，做聚类分析，得到本体或者文件所属类别，尝试了现有的两种非常常用的聚类手段，K-means均值聚类和LDA主题聚类模型（主题-词语，文件-主题分布）
>可参考资料：
>LDA模型：[https://blog.csdn.net/baidu_15113429/article/details/79959261](https://blog.csdn.net/baidu_15113429/article/details/79959261)
([https://blog.csdn.net/accumulate_zhang/article/details/62453672](https://blog.csdn.net/accumulate_zhang/article/details/62453672))

## 实现效果
文件总数量为26
数据格式为：data_set=[[],[],[]],类似于如下（二元列表，每个子列表存放每个文件分词后得到的列表）
```bash
data_set [['载人', '航天', '工程', '专项', '标准', '载人', '航天', '工程', '有效载荷', '生物', '通用', '发布', '实施', '中国', '载人', '航天', '工程', '办公室', '批准', '前言', '标准', '附录', '资料性', '附录', '标准'], ['中国', '载人', '航天', '工程', '办公室', '提出', '标准', '载人', '航天', '工程', '标准化', '管理', '咨询中心', '归口', '标准', '起草', '单位',  '飞行', '动物', '植物', '实验', '样品', '飞行', '确认', '实验', '样品', '包含', '生物', '危害', '凡不注', '日期', '版次', '引用', '文件', '最新', '版本', '于本', '标准', '工作', '场所', '物理', '因素', '测量', '紫外', '辐射'],[ '声学', '测量', '常用', '频率', '声学', '倍频程', '分数',  '安装', '到位', '测量', '接地', '电阻', '满足要求', '设备', '自带', '接地', '螺钉', '涂胶', '拧紧', '设备', '优先', '安装', '面来', '接地', '电阻', '满足要求', '轻微', '打磨', '设备', '支架', '安装', '方法', '加以解决', '搭接', '设备', '舱体', '安装', '打磨', '安装', '安装', '后应', '实测']]
```

### K-means
![在这里插入图片描述](https://img-blog.csdnimg.cn/def5d2ddda8c4caa8a346bb8ad6efe9c.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/e4c7b465a4d345e093eeea2c77202e1e.png)
### LDA聚类
![在这里插入图片描述](https://img-blog.csdnimg.cn/bdec3296069d49f3a615ba434c9b44a7.png)
可视化展示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/edd6f383a58d4c8ab1ddb10698f3258d.png)



## 地址
项目本机地址：E:\python project\pythonProject_draftKG\主题聚类
项目git地址：


