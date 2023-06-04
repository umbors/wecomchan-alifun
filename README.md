## Wecom酱
本项目是Wecom酱-python服务端（阿里云函数版）修改版本，[原版Wecom酱][1]

相比原版主要有如下改动
- 增加了图文消息发送（send_to_wecom_msgpic)，需要在POST中包含key、type（"news"）、title，text，picurl五部分内容，例如：
```
data = {
            "key":"123456",
            "type": "news",
            "title":"Hello world!",
            "msg": "This is message from wecom-chan", 
            "picurl":"https:"
}
```
- 添加了urllib.parse.parse_qs处理，POST时无需指定json格式，便于将现有server-chan推送快速修改为wecom-chan。使用例如下：
```
resp = requests.post(noti_url, data=data)
```
用index.py替换原项目的文件即可

[1]: https://github.com/easychen/wecomchan