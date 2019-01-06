# PixivSync
一个Pixiv同步工具，可以获取Pixiv的原图地址。具体的特性如下：
- 支持获取每日Top 10
- 单独列出关注者的新作品，方便增量下载
- 单独列出收藏夹（公开与私人分离）的新作品，方便增量下载

## 依赖
程序在Python 2下成功运行，如果你更喜欢Python 3，那么也应该可以兼容。但在使用前请安装pixivpy包，通过pip的简便安装命令如下：
```
pip install pixivpy
```
之后你需要编辑config.ini文件，在username和password的等号后直接填入自己的用户名和密码，在following的id的等号后填入你喜欢的画师id号码，多个id用英文逗号分隔，一个标准的示例如下：
```
[my]
username=a@a.com
password=123456

[following]
id=1,2,3
```

## 用法
请在程序目录下运行本程序，所有输出结果会保存在outputs文件夹中。
```
python2 PixivSync.py dailyrank #获取每日Top 10
python2 PixivSync.py bookmarks #获取公开收藏夹
python2 PixivSync.py pribookmarks #获取私人收藏夹
python2 PixivSync.py following #获取关注画师的作品
```
程序的运行速度直接依赖于你连接Pixiv服务器的速度，如果无法连接Pixiv，那么程序也无法运行。

为了方便大家使用，写了一些脚本放在tools目录下：
```
sh wget.sh [文件名]
#多进程调用wget下载原图到当前目录，可以直接把程序输出的txt文件作为参数。但是没有对进程数目的控制，需要小心。仅支持Linux。
```

## 提示
本程序是一个Python脚本，需要一定基础。并且Pixiv对于直接访问图片地址的行为有防盗链措施，需要一些绕过操作。

## 更新预告
- 基于Python的图片下载程序
- 账号克隆工具

## 相关程序
有很多优秀的便于使用的类似程序，一一列举：
- [PixivUserBatchDownload](https://github.com/Mapaler/PixivUserBatchDownload)
- [XZPixivDownloader](https://github.com/xuejianxianzun/XZPixivDownloader)
