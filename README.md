# DataMining
DB project
# note, to run this app:
```
pip install -r requirements.txt

npm ci

$env:FLASK_APP = "app.py"
flask run
```

# framework documentation
* https://read.helloflask.com/template/
* https://tailwindcss.com/docs

## update log
对于 filestorage 文件夹
upload 存放的是用户上传的 csv 文件
result 存放的是决策树文件
test 中包含一个可运行的 jupyter notebook 决策树示例文件
    该文件首先以 wine 数据集绘制了一个决策树, 演示了基本步骤
    其次是结合本项目需求演示了从读取csv文件到构造训练数据再到决策树图像存储的过程

更新了 requirements 依赖
主要是 graphviz 以及 pandas 库

问题说明:
calc_tree_from_file(file, ["Play", "Not Play"])
还需要用户填入的 target 字段作为参数传入，这一点并未体现
以课上的天气为例，需要 "Play" "Not Play"
另外就是网页显示png图片的问题，这里结果已经保存为图片了

此外，dot 文件应该支持一层一层的显示，网页是否支持直接显示 dot 文件

注意事项：
为了debug方便，app 添加了最后的main语句, 因此运行时可以直接run这个py文件(常规运行python程序的方法)
