#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from pixivpy3 import *
import sys
import os
import threadpool
import getpass
import shutil
import time

class BasicUtils(object):
    my_id = 0
    my_name = ""
    aapi = None
    conn = None
    
    def __init__(self):
        self.conn = sqlite3.connect('database', check_same_thread=False)
        self.aapi = AppPixivAPI()

    def __del__(self):
        self.conn.close()

    def _secure_name(self,name):
        if "/" in name:
            name = name.replace("/"," ")
        return name

    def _find_new(self,seta, setb):
        temp = []
        tempa = []
        tempb = []
        for eacha in seta:
            tempa.append(str(eacha).strip('\r').strip('\n'))
        for eachb in setb:
            tempb.append(str(eachb).strip('\r').strip('\n'))
        for eachc in tempb:
            temp.append(str(eachc))
        for eachd in tempb:
            for eache in tempa:
                if eachd == eache:
                    try:
                        temp.remove(str(eachd))
                    except:
                        pass
        return temp

    def _is_illust_added(self, iid):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id FROM illusts WHERE id = ?;"
        cursor.execute(sqlcmd,(iid,))
        result = cursor.fetchall()
        if result == []:
            return False
        else:
            return True
   
    def _get_illusts(self,uid):
        aapi = self.aapi
        json_result = aapi.user_illusts(uid)
        ids = []
        uname = ""
        illusts = json_result['illusts']
        while 1:
            for each in illusts:
                ids.append(each.id)
                uname = each.user.name
            try:
                next_qs = aapi.parse_qs(json_result.next_url)
                if next_qs is None:
                    break
                json_result = aapi.user_illusts(**next_qs)
                illusts = json_result['illusts']
            except Exception as e:
                print(e)
                break
        return ids,uname

    def _add_user_illusts(self,uid):
        aapi = self.aapi
        conn = self.conn
        cursor = conn.cursor()
        json_result = aapi.user_illusts(uid)
        illusts = json_result['illusts']
        while 1:
            for each in illusts:
                if not self._is_illust_added(each.id):
                    if each.page_count == 1 and each.type != 'ugoira':
                        sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                        cursor.execute(sqlcmd,(each.id,1,each.title,each.user.id,each.meta_single_page.original_image_url,0))
                        conn.commit()
                    elif each.page_count > 1:
                        count = 1
                        for page in each.meta_pages:
                            sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                            try:
                                url = each.image_urls.original
                            except:
                                url = each.image_urls.large 
                            cursor.execute(sqlcmd,(each.id,count,each.title,each.user.id,url,0))
                            count += 1
            try:
                next_qs = aapi.parse_qs(json_result.next_url)
                if next_qs is None:
                    break
                json_result = aapi.user_illusts(**next_qs)
                illusts = json_result['illusts']
            except Exception as e:
                print(e)
                break                

    def _add_illusts(self,iid):
        aapi = self.aapi
        json_result = aapi.illust_detail(iid)
        detail = json_result['illust'] 
        conn = self.conn
        cursor = conn.cursor()
        if not self._is_illust_added(iid):
            if detail.page_count == 1 and detail.type != 'ugoira':
                sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                cursor.execute(sqlcmd,(iid,1,detail.title,detail.user.id,detail.meta_single_page.original_image_url,0))
                conn.commit()
            elif detail.page_count > 1:
                count = 1
                for page in detail.meta_pages:
                    sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                    try:
                        url = each.image_urls.original
                    except:
                        url = each.image_urls.large                          
                    cursor.execute(sqlcmd,(iid,count,detail.title,detail.user.id,url,0))
                    count += 1
        """
        sqlcmd = "SELECT name FROM users WHERE id = ?;"
        cursor.execute(sqlcmd,(detail.user.id,))
        result = cursor.fetchall()
        if result == []:
            self.add_user(detail.user.id)
        """

    def _get_bookmarks(self, rule):
        aapi = self.aapi
        conn = self.conn
        cursor = conn.cursor()
        json_result = aapi.user_bookmarks_illust(aapi.user_id,restrict=rule)
        ids = []
        illusts = json_result['illusts']
        while 1:
            for each in illusts:
                ids.append(each.id)
            try:
                next_qs = aapi.parse_qs(json_result.next_url)
                if next_qs is None:
                    break
                json_result = aapi.user_bookmarks_illust(**next_qs)
                illusts = json_result['illusts']
            except Exception as e:
                print(e)
                break
        return ids
        
    def _add_bookmarks(self, rule):
        aapi = self.aapi
        conn = self.conn
        cursor = conn.cursor()
        json_result = aapi.user_bookmarks_illust(aapi.user_id,restrict=rule)
        ids = []
        illusts = json_result['illusts']
        while 1:
            for each in illusts:
                ids.append(each.id)
                if not self._is_illust_added(each.id):
                    if each.page_count == 1 and each.type != 'ugoira':
                        sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                        cursor.execute(sqlcmd,(each.id,1,each.title,each.user.id,each.meta_single_page.original_image_url,0))
                        conn.commit()
                    elif each.page_count > 1:
                        count = 1
                        for page in each.meta_pages:
                            sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                            cursor.execute(sqlcmd,(each.id,count,each.title,each.user.id,page.image_urls.original,0))
                            count += 1
            try:
                next_qs = aapi.parse_qs(json_result.next_url)
                if next_qs is None:
                    break
                json_result = aapi.user_bookmarks_illust(**next_qs)
                illusts = json_result['illusts']
            except Exception as e:
                print(e)
                break
        for each in ids:
            sqlcmd = "INSERT INTO bookmarks(id,restrict,downloaded) values(?,?,0);"
            if rule == "public":
                cursor.execute(sqlcmd,(each,1))
            else:
                cursor.execute(sqlcmd,(each,2))
            conn.commit()
    
    def login(self, username, password):
        try:
            userinfo = self.aapi.login(username, password)
            self.my_id = self.aapi.user_id
            self.my_name = str(userinfo.response.user.name)
            print("登录成功。欢迎您，" + self.my_name + "。")
        except:
            exit("登录失败。")
    
    def download_user_one(self, iid):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id,number,name,user,url FROM illusts WHERE id = ?;"
        result = cursor.execute(sqlcmd,(iid,))
        results = []
        for row in result:
            results.append(row)
        for row in results:
            iid = row[0]
            number = row[1]
            name = row[2]
            uid = row[3]
            url = row[4]
            sqlcmd = "SELECT name FROM users WHERE id = ?"
            cursor.execute(sqlcmd,(uid,))
            uname = cursor.fetchone()[0]
            filename = url.split("/")
            filename = filename[len(filename) - 1]
            if not os.path.exists("./illusts/" + self._secure_name(uname)):
                os.makedirs("./illusts/" + self._secure_name(uname))
            self.aapi.download(url, path="./illusts/" + self._secure_name(uname), name=filename)
            sqlcmd = "UPDATE illusts set downloaded = 1 WHERE id = ? AND number = ?;"
            cursor.execute(sqlcmd,(iid,number))
            conn.commit()
            print("作品 " + name + "下载成功（第" + str(number) + "张）。")

    def download_bookmarks_one(self, iid):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id,number,name,user,url FROM illusts WHERE id = ?;"
        result = cursor.execute(sqlcmd,(iid,))
        results = []
        for row in result:
            results.append(row)
        for row in results:
            iid = row[0]
            number = row[1]
            name = row[2]
            uid = row[3]
            url = row[4]
            sqlcmd = "SELECT restrict FROM bookmarks WHERE id = ?"
            cursor.execute(sqlcmd,(iid,))
            rule = cursor.fetchone()[0]
            if rule == 1:
                rule = "bookmakrs_public"
            elif rule == 2:
                rule = "bookmarks_private"
            filename = url.split("/")
            filename = filename[len(filename) - 1]
            if not os.path.exists("./illusts/" + str(rule)):
                try:
                    os.makedirs("./illusts/" + str(rule))
                except:
                    pass
            self.aapi.download(url, path="./illusts/" + str(rule),name=filename)
            sqlcmd = "UPDATE illusts set downloaded = 1 WHERE id = ? AND number = ?;"
            cursor.execute(sqlcmd,(iid,number))
            conn.commit()
            sqlcmd = "UPDATE bookmarks set downloaded = 1 WHERE id = ?;"
            cursor.execute(sqlcmd,(iid,))
            conn.commit()
            print("作品 " + name + "下载成功（第" + str(number) + "张）。")

    def add_user(self, uid):
        aapi = self.aapi
        json_result = aapi.user_detail(uid)
        uid = json_result.user.id
        name = json_result.user.name
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "INSERT INTO users(id,name) values(?,?);"
        cursor.execute(sqlcmd,(uid,name))
        conn.commit()
        self._add_user_illusts(uid)
        print("画师 " + name + " 已经加入数据库。")

    def update_user(self, uid):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT name FROM users WHERE id = ?;"
        cursor.execute(sqlcmd,(uid,))
        result = cursor.fetchall()
        try:
            uname = result[0][0]
        except:
            pass
        if result == []:
            self.add_user(uid)
        else:
            ids,nuname = self._get_illusts(uid)
            sqlcmd = "SELECT id FROM illusts WHERE user = ?;"
            cursor.execute(sqlcmd,(uid,))
            result = cursor.fetchall()
            old = []
            for each in result:
                old.append(each[0])
            new = self._find_new(old,ids)
            if not new == []:
                for each in new:
                    self._add_illusts(each)
                print("画师 " + str(uname) + " 有新作品，已更新。")
            if nuname != uname:
                try:
                    shutil.move("./illusts/" + uname, "./illusts/" + nuname)
                except:
                    pass
                sqlcmd = "UPDATE users set name = ? WHERE name = ?;"
                cursor.execute(sqlcmd,(_secure_name(nuname),_secure_name(uname)))
                conn.commit()
                print("画师 " + uname + " 更名为 " + nuname + " 。")

    def download_user(self, uid):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id FROM illusts WHERE user = ? and downloaded = 0;"
        cursor.execute(sqlcmd,(uid,))
        result = cursor.fetchall()
        ids = []
        for each in result:
            ids.append(each[0])
        task_pool=threadpool.ThreadPool(10)
        requests=threadpool.makeRequests(self.download_user_one,ids)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()

    def download_bookmarks(self, rule):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id FROM bookmarks WHERE restrict = ? and downloaded = 0;"
        if rule == "public":
            rule = 1
        elif rule == "private":
            rule = 2
        cursor.execute(sqlcmd,(rule,))
        result = cursor.fetchall()
        ids = []
        for each in result:
            ids.append(each[0])
        task_pool=threadpool.ThreadPool(10)
        requests=threadpool.makeRequests(self.download_bookmarks_one,ids)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()

    def get_following(self, rule):
        aapi = self.aapi
        json_result = aapi.user_following(aapi.user_id,restrict=rule)
        uids = []
        users = json_result['user_previews']
        while 1:
            for each in users:
                uids.append(each.user.id)
            try:
                next_qs = aapi.parse_qs(json_result.next_url)
                if next_qs is None:
                    break
                json_result = aapi.user_following(**next_qs)
                users = json_result['user_previews']
            except Exception as e:
                print(e)
                break
        return uids
        
    def update_bookmarks(self, rule):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id FROM bookmarks WHERE restrict = ?;"
        if rule == "public":
            restrict = 1
        elif rule == "private":
            restrict = 2
        cursor.execute(sqlcmd,(restrict,))
        result = cursor.fetchall()
        if result == []:
            self._add_bookmarks(rule)
        else:
            ids = self._get_illusts(rule)
            old = []
            for each in result:
                old.append(each[0])
            new = self._find_new(old,ids)
            if not new == []:
                json_result = aapi.user_bookmarks_illust(aapi.user_id,restrict=rule)
                ids = []
                illusts = json_result['illusts']
                while 1:
                    for each in illusts:
                        if each.id in new:
                            ids.append(each.id)
                            if not self._is_illust_added(each.id):
                                if each.page_count == 1 and each.type != 'ugoira':
                                    sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                                    cursor.execute(sqlcmd,(each.id,1,each.title,each.user.id,each.meta_single_page.original_image_url,0))
                                    conn.commit()
                                elif each.page_count > 1:
                                    count = 1
                                    for page in each.meta_pages:
                                        sqlcmd = "INSERT INTO illusts(id,number,name,user,url,downloaded) values(?,?,?,?,?,?);"
                                        cursor.execute(sqlcmd,(each.id,count,each.title,each.user.id,page.image_urls.original,0))
                                        count += 1
                    try:
                        next_qs = aapi.parse_qs(json_result.next_url)
                        if next_qs is None:
                            break
                        json_result = aapi.user_bookmarks_illust(**next_qs)
                        illusts = json_result['illusts']
                    except Exception as e:
                        print(e)
                        break
                for each in ids:
                    sqlcmd = "INSERT INTO bookmarks(id,restrict,downloaded) values(?,?,0);"
                    if rule == "public":
                        cursor.execute(sqlcmd,(each,1))
                    else:
                        cursor.execute(sqlcmd,(each,2))
                    conn.commit()
        print("更新收藏夹成功。")

    def _add_following(self, rule):
        uids = self.get_following(rule)
        for each in uids:
            self.update_user(each)
            #time.sleep(5)
                    
    def update_following(self, rule):
        self._add_following(rule)
        print("更新关注用户成功。")
        
    def download_following(self,rule):
        conn = self.conn
        cursor = conn.cursor()
        sqlcmd = "SELECT id FROM users;"
        cursor.execute(sqlcmd)
        result = cursor.fetchall()
        for each in result:
            self.download_user(each[0])
        print("下载完毕。")

def main():
    bu = BasicUtils()
    print("Pixiv Sync - 基于Python的Pixiv客户端")
    print("由ChinaKevinLi制作，欢迎关注Github、Twitter（同名）。")
    username = input("Pixiv用户名：")    
    password = getpass.getpass("Pixiv密码：")
    bu.login(username,password)
    if 'bookmarks' in sys.argv:
        if 'public' and 'update' in sys.argv:
            bu.update_bookmarks("public")
        elif 'public' and 'download' in sys.argv:
            bu.download_bookmarks("public")
        elif 'private' and 'update' in sys.argv:
            bu.update_bookmarks("private")
        elif 'private' and 'download' in sys.argv:
            bu.download_bookmarks("private")
        else:
            print("缺少参数。")
    elif 'following' in sys.argv:
        if 'public' and 'update' in sys.argv:
            bu.update_following("public")
        elif 'public' and 'download' in sys.argv:
            bu.download_following("public")
        elif 'private' and 'update' in sys.argv:
            bu.update_following("private")
        elif 'private' and 'download' in sys.argv:
            bu.download_following("private")
        else:
            print("缺少参数。")
    else:
        print("缺少参数。")

if __name__ == '__main__':
    main()
