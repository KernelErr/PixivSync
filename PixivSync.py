# -*- coding: utf-8 -*
from pixivpy3 import AppPixivAPI
import ConfigParser
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time

def get_config():
    print("尝试读取配置...")
    configfile = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__)[0] + '/config.ini')
    configfile.read(path)
    config=[]    
    try:
        config.append(configfile.get('my','username'))
        config.append(configfile.get('my','password'))
        config.append(configfile.get('following','id'))
        print("配置读取成功。")
    except:
        exit("检查你的配置文件是否正常。")
    else:
        return config

def del_same(seta, setb):
    temp = []
    tempa = []
    tempb = []
    for eacha in seta:
        tempa.append(eacha.strip('\r').strip('\n'))
    for eachb in setb:
        tempb.append(eachb.strip('\r').strip('\n'))
    for eachc in tempb:
        temp.append(eachc)
    for eachd in tempb:
        for eache in tempa:
            if eachd == eache:
                temp.remove(eachd)
    return temp

def get_user(aapi, uid):
    json_result = aapi.user_illusts(uid)
    urls = []
    while 1:
        try:
            nLen = len(json_result.illusts)
        except Exception as e:
            print(e)

        for illust in json_result.illusts:
            if illust.page_count == 1 and illust.type != 'ugoira':
                urls.append(illust.meta_single_page.original_image_url)
            elif illust.page_count > 1:
                image_urls = [
                    page.image_urls.original
                    for page in illust.meta_pages
                    ]
                for url in image_urls:
                    urls.append(url)
            else:
                image_urls = []

        try:
            next_qs = aapi.parse_qs(json_result.next_url)
            if next_qs is None:
                break
            json_result = aapi.user_illusts(**next_qs)
        except Exception as e:
            print(e)
            break

    return urls
    
def get_bookmarks(aapi, rule):
    json_result = aapi.user_bookmarks_illust(aapi.user_id,restrict=rule)
    urls = []
    while 1:
        try:
            nLen = len(json_result.illusts)
        except Exception as e:
            print(e)

        for illust in json_result.illusts:
            if illust.page_count == 1 and illust.type != 'ugoira':
                urls.append(illust.meta_single_page.original_image_url)
            elif illust.page_count > 1:
                image_urls = [
                    page.image_urls.original
                    for page in illust.meta_pages
                    ]
                for url in image_urls:
                    urls.append(url)
            else:
                image_urls = []

        try:
            next_qs = aapi.parse_qs(json_result.next_url)
            if next_qs is None:
                break
            json_result = aapi.user_bookmarks_illust(**next_qs)
        except Exception as e:
            print(e)
            break

    filename = './outputs/bookmarks_' + rule
    if not os.path.exists(filename + '.txt'):
       open(filename + '.txt','w+')
    with open(filename + '.txt','r+') as f:
       old = f.readlines()
       now = urls
       new = del_same(old, now)
       with open(filename + '.txt','w+') as fa:
           for url in now:
               fa.write(str(url) + '\n')
       with open(filename + '_new.txt','w+') as fb:
           for url in new:
               fb.write(str(url) + '\n')
    print("更新收藏夹成功。")

def get_daily_rank(aapi):
    json_result = aapi.illust_ranking(mode='day', date=None)
    json_result = json_result.illusts
    ids = []
    urls = []
    for number in range(0,10):
        ids.append(json_result[number].id)
    for each in ids:
        illust = aapi.illust_detail(each)
        illust = illust.illust
        if illust.page_count == 1 and illust.type != 'ugoira':
            urls.append(illust.meta_single_page.original_image_url)
        elif illust.page_count > 1:
            image_urls = [
                    page.image_urls.original
                    for page in illust.meta_pages
                    ]
            for url in image_urls:
                urls.append(url)
    filename = './outputs/' + str(time.strftime("%Y%m%d",time.localtime())) + ".txt"
    with open(filename,'w+') as f:
        for url in urls:
            f.write(str(url) + '\n')
    print("获取每日Top 10成功。")

def get_following(aapi,following):
    for user in following:
        userinfo = aapi.user_detail(user)
        username = userinfo.user.name
        username = str(username).split("/")[0]
        filename = './outputs/' + str(username)
        urls = get_user(aapi,user)
        if not os.path.exists(filename + '.txt'):
            with open(filename + '.txt','w+') as f:
                f.write('')
        with open(filename + '.txt','r+') as f:
           old = f.readlines()
           now = get_user(aapi,user)
           new = del_same(old, now)
           with open(filename + '.txt','w+') as fa:
               for url in now:
                   fa.write(str(url) + '\n')
           with open(filename + '_new.txt','w+') as fb:
               for url in new:
                     fb.write(str(url) + '\n')
        print("更新画师 " + str(username) + " 的作品成功。")

def main():
    print("PixivSync 由 ChinaKevinLi 制作")
    print("Github地址：https://github.com/ChinaKevinLi/PixivSync")
    print("交流QQ群：761049620")
    try:
        test = sys.argv[1]
    except:
        exit("无命令，请查询文档。")
    aapi = AppPixivAPI()
    config = get_config()
    username = config[0]
    password = config[1]
    following = []
    for id in config[2].split(','):
        following.append(id)
    print("登录帐号中...")
    try:
        userinfo = aapi.login(username,password)
    except:
        exit("登录失败。")
    else:
        print("登录成功。欢迎您，" + str(userinfo.response.user.name) + "。")
    if sys.argv[1] == "dailyrank":
        print("开始获取每日Top 10，请耐心等待。")
        get_daily_rank(aapi)
    elif sys.argv[1] == "following":
        print("开始更新关注者的作品，请耐心等待。")
        get_following(aapi,following)
    elif sys.argv[1] == "bookmarks":
        print("开始更新公开收藏列表，请耐心等待。")
        get_bookmarks(aapi, 'public')       
    elif sys.argv[1] == "pribookmarks":
        print("开始更新私人收藏列表，请耐心等待。")
        urls = get_bookmarks(aapi, 'private')
    else:
        exit("无对应命令，请查询文档。")

if __name__ == '__main__':
    main()
