# paper-translator
中英对照论文翻译工具

使用百度翻译把 pdf 格式的英文论文转换成中英文对照的 html 文件！

![](https://cdn.nlark.com/yuque/0/2022/png/22611614/1648519063367-e9be07e9-dbba-4b8b-a2f1-cba821c5335f.png)

## 准备工作
1. 申请百度翻译接口：[通用翻译API](https://api.fanyi.baidu.com/product/11)，点击下方“立即使用”并根据提示操作
2. 在[总览页面](http://api.fanyi.baidu.com/api/trans/product/desktop)最下方的申请信息中可以看到**APPID**和**密钥**
3. 新建文件 `key.txt` ，将APPID和密钥复制粘贴到文件中，中间用一个空格隔开
4. 安装依赖 `pip install requests pymupdf`

## 使用方法
```sh
python main.py 英文文档.pdf
```

如果希望编辑提取出的文字，可以使用以下命令。程序会首先生成一个同名的 txt 文件，手动编辑保存后按回车键继续翻译。
```sh
python main.py --edit 英文文档.pdf
```

## 关于翻译接口
百度翻译突然要钱了，欢迎提供更好的/免费的翻译接口：

2022年8月1日起，通用翻译API标准版免费调用量调整为5万字符/月，高级版免费调用量调整为100万字符/月 [查看详情](https://api.fanyi.baidu.com/doc/8)
