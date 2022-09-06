# paper-translator
中英对照论文翻译工具

使用百度翻译把 pdf 格式的英文论文转换成中英文对照的 html 文件！

![](https://cdn.nlark.com/yuque/0/2022/png/22611614/1648519063367-e9be07e9-dbba-4b8b-a2f1-cba821c5335f.png)

## 使用百度翻译
提示：百度翻译突然要钱了

2022年8月1日起，通用翻译API标准版免费调用量调整为5万字符/月，高级版免费调用量调整为100万字符/月 [查看详情](https://api.fanyi.baidu.com/doc/8)

当然，如果你是付费用户，仍可以继续使用

1. 安装依赖 `pip install requests pymupdf`
2. 申请百度翻译接口：[通用翻译API](https://api.fanyi.baidu.com/product/11)，点击下方“立即使用”并根据提示操作
3. 在[总览页面](http://api.fanyi.baidu.com/api/trans/product/desktop)最下方的申请信息中可以看到 **APPID** 和 **密钥**
4. 初次使用，运行 `python main.py`，程序会生成 `key.py` 文件，用任意编辑器打开后填写 appid 和 appkey ，保存
5. 之后就可以正常使用本程序了

## 使用腾讯翻译
提示：根据[计费概述](https://cloud.tencent.com/document/product/551/35017)，文本翻译的**每月免费额度为 5 百万字符**，请留意后台使用量。

1. 安装依赖 `pip install tencentcloud-sdk-python pymupdf`
2. 申请腾讯翻译接口：[机器翻译](https://console.cloud.tencent.com/tmt)
3. 在[API密钥管理]新建密钥，之后可以看到 **SecretId** 和 **SecretKey**
4. 初次使用，运行 `python main.py`，程序会生成 `key.py` 文件，用任意编辑器打开后填写 SecretId 和 SecretKey ，保存
5. 之后就可以正常使用本程序了

## 使用方法
```sh
python main.py 英文文档.pdf
```

如果希望编辑提取出的文字，可以使用以下命令。程序会首先生成一个同名的 txt 文件，手动编辑保存后按回车键继续翻译。
```sh
python main.py --edit 英文文档.pdf
```
