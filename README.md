# PixivSync
基于Python的Pixiv客户端、同步工具。具体的特性如下：
- 多线程下载图片
- 用户更名提醒
- 数据库保存数据，实时更新

## 依赖
程序在Python 3下成功运行，请先安装依赖包：
```
pip install -r requirements.txt
```

## 用法
请在程序目录下运行本程序，图片会下载到illusts文件夹中。
```
python3 PixivSync.py update following public  #更新公开关注用户
python3 PixivSync.py update following private #更新私人关注用户
python3 PixivSync.py update bookmarks public  #更新公开收藏夹
python3 PixivSync.py update bookmarks private #更新私人收藏夹

python3 PixivSync.py download following public  #下载公开关注用户
python3 PixivSync.py download following private #下载私人关注用户
python3 PixivSync.py download bookmarks public  #下载公开收藏夹
python3 PixivSync.py download bookmarks private #下载私人收藏夹
```
程序的运行速度直接依赖于你连接Pixiv服务器的速度，如果无法连接Pixiv，那么程序也无法运行。

## 提示
输入密码时为了保护您的隐私，不会显示出来，直接输入完后回车即可。

## 更新预告
- 任何需要和Bug反馈直接提交issues，将会考虑更新。

## 相关程序
有很多优秀的便于使用的类似程序，一一列举：
- [PixivUserBatchDownload](https://github.com/Mapaler/PixivUserBatchDownload)
- [XZPixivDownloader](https://github.com/xuejianxianzun/XZPixivDownloader)
