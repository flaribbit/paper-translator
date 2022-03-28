# paper-translator
中英对照论文翻译工具

使用百度翻译把 pdf 格式的英文论文转换成中英文对照的 html 文件！

## 准备工作
1. 申请百度翻译接口：[通用翻译API](通用翻译API)，点击下方“立即使用”并根据提示操作
2. 在[总览页面](http://api.fanyi.baidu.com/api/trans/product/desktop)最下方的申请信息中可以看到**APPID**和**密钥**
3. 新建文件 `key.txt` ，将APPID和密钥复制粘贴到文件中，中间用一个空格隔开
4. 安装依赖 `pip install requests pymupdf`

## 使用方法
```sh
python main.py 英文文档.pdf
```