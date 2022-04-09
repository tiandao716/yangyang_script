#!/bin/env python3
# -*- coding: utf-8 -*

import requests
import time,datetime
import requests,re,os,sys,random,json
from urllib.parse import quote, unquote
import threading
import urllib3
import multiprocessing
import random
import sqlite3 as sqlite
import mysql.connector as mysql
import hashlib 


def printT(s):
    print("[{0}]: {1}".format(datetime.datetime.now(), s), flush=True)
    sys.stdout.flush()

def getEnvs(label):
    try:
        if label == 'True' or label == 'yes' or label == 'true' or label == 'Yes':
            return True
        elif label == 'False' or label == 'no' or label == 'false' or label == 'No':
            return False
    except:
        pass
    try:
        if '.' in label:
            return float(label)
        elif '&' in label:
            return label.split('&')
        elif '@' in label:
            return label.split('@')
        else:
            return int(label)
    except:
        return label

def userAgent():
    
    """
    随机生成一个UA
    :return: jdapp;iPhone;9.4.8;14.3;xxxx;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/2455696156;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1
    """
    uuid = ''.join (random.sample ('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
    addressid = ''.join (random.sample ('1234567898647', 10))
    iosVer = ''.join (
        random.sample (["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
    iosV = iosVer.replace ('.', '_')
    iPhone = ''.join (random.sample (["8", "9", "10", "11", "12", "13"], 1))
    ADID = ''.join (random.sample ('0987654321ABCDEF', 8)) + '-' + ''.join (
        random.sample ('0987654321ABCDEF', 4)) + '-' + ''.join (
        random.sample ('0987654321ABCDEF', 4)) + '-' + ''.join (
        random.sample ('0987654321ABCDEF', 4)) + '-' + ''.join (random.sample ('0987654321ABCDEF', 12))
    return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone{iPhone},1;addressid/{addressid};supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1'


## 获取通知服务
class msg(object):
    def __init__(self, m=''):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        printT(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()           #这代码的作用就是刷新缓冲区。
                                     # 当我们打印一些字符时，并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区，然后再打印。
                                     # 这就存在一个问题，如果你想等时间间隔的打印一些字符，但由于缓冲区没满，不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    printT("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                printT("加载通知服务失败~")
        ###################

class SQLProcess:

    def __init__(self, table_name, database_dict = {
                                                    'type': 'sqlite',
                                                    'name': "filtered_cks.db"
                                                   }):
        self.database_dict = database_dict
        self.table_name = self.getTableName(table_name)
        print(self.table_name)
        self.createDatebase()
        self.createTable()
    
    def getTableName(self, name):
        return 'table_' + name.replace('=', '').replace('%', '').replace('_', '').split("key")[-1][::10]
    
    def deleteTable(self):
        self.c.execute(f'''
                        DROP TABLE IF EXISTS {self.table_name}
                        ''')
        self.conn.commit()
    
    def createDatebase(self):
        if 'type' not in self.database_dict:
            print("Error in database configure! Exit...")
            exit()
        
        if self.database_dict['type'] == 'mysql':
            try:
                start = time.time()
                self.conn = mysql.connect(
                    host = self.database_dict['host'],       # 数据库主机地址
                    port = self.database_dict['port'],
                    user = self.database_dict['user'],    # 数据库用户名
                    passwd = self.database_dict['passwd'],   # 数据库密码
                    database = self.database_dict['database']
                )
                end = time.time()
                # 两秒超时
                if end - start > 2:
                    raise Exception
                print("Connected to remote mysql successfully...")
            except Exception as e:
                print("Try to connecting to remote mysql but timeout occurs...", e)
                self.conn = sqlite.connect("filtered_cks.db")
                print("Connected to local sqlite successfully...")
        else:
            self.conn = sqlite.connect("filtered_cks.db")
            print("Connected to local sqlite successfully...")
        self.c = self.conn.cursor()
        return self.conn
        
    def createTable(self):
        # 时间戳；ck；日期；优先级；权重（拟运行次数）
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                           (TIMESTAMP REAL PRIMARY KEY NOT NULL, 
                           USER_NAME TEXT NOT NULL, 
                           DATE TEXT NOT NULL, 
                           PRIORITY INT NOT NULL,
                           TIMES INT NOT NULL DEFAULT 0);
                           ''')
        
        self.conn.commit()
        print(f"Table {self.table_name} has been created.")

    def deleteTable(self):
        self.c.execute(f"DROP TABLE {self.table_name};")
        self.conn.commit()
        print(f"Table {self.table_name} has been deleted.")
        
    def insertItem(self, user_name, timestamp, year_month_day, priority):
        if self.findUserName(user_name, year_month_day):
            print(f"{getUserName(user_name)} is in Table {self.table_name}. Updating...")
            self.updateItem(user_name, timestamp, year_month_day, priority)
            return
        self.c.execute(f'''INSERT INTO {self.table_name} (USER_NAME, TIMESTAMP, DATE, PRIORITY)
                            VALUES ('{user_name}', {timestamp}, '{year_month_day}', {priority})''')
        self.conn.commit()
        print(f"Item {getUserName(user_name)} has been inserted into Table {self.table_name}.")

    def addTimes(self, user_name, year_month_day = str(datetime.date.today())):
        if not self.findUserName(user_name, year_month_day):
            print(f"Error in updating: No item found...")
            return
        self.c.execute(f'''
                        UPDATE {self.table_name} set 
                        TIMES = TIMES + 1
                        WHERE USER_NAME='{user_name}' AND DATE = '{year_month_day}'
                        ''')
        self.conn.commit()
        print(f"Item {getUserName(user_name)}'s times have been added in Table {self.table_name}.")
        
    def updateItem(self, user_name, timestamp, year_month_day, priority):
        if not self.findUserName(user_name, year_month_day):
            print(f"Error in updating: No item found...")
            return
        if priority > 0:
            print(f"Item {getUserName(user_name)}:{priority} is not updated because it only supports decrease.")
            return

        # 时间戳为primary key，不更新
        self.c.execute(f'''
                        UPDATE {self.table_name} set 
                        DATE='{year_month_day}',
                        PRIORITY={priority}
                        WHERE USER_NAME='{user_name}' AND PRIORITY > 0 AND DATE = '{year_month_day}'
                        ''')
        self.conn.commit()
        print(f"Item {getUserName(user_name)}:{priority} has been updated in Table {self.table_name}.")
    
    def filterUsers(self, user_number, year_month_day = str(datetime.date.today())):
        self.c.execute(f'''
                        SELECT USER_NAME, TIMES FROM {self.table_name} WHERE PRIORITY > -1 AND DATE = '{year_month_day}' ORDER BY PRIORITY DESC;
                        ''')
        p = self.c.fetchall()
        users, times = [], []
        for x in p:
            users.append(x[0])
            times.append(x[1])
        # users, times = [x[0] for x in p], [x[-1] for x in p]
        return users[:min(len(users), user_number)], times[:min(len(times), user_number)]
    
    def findUserName(self, user_name, year_month_day = str(datetime.date.today())):
        p = self.c.execute(f'''
                        SELECT count(*) from {self.table_name} WHERE USER_NAME = '{user_name}' AND DATE = '{year_month_day}'
                        ''')
        return self.c.fetchone()[0] != 0
    
    def printTodayItems(self):
        self.printAllItems(str(datetime.date.today()))
    
    def printAllItems(self, year_month_day = None):
        if year_month_day is None:
            print(f"{'user_name'.ljust(17, ' ')}{'date'.ljust(12, ' ')}prio  times")
            self.c.execute(f"SELECT * FROM {self.table_name}")
            for item in self.c.fetchall():
                print(f"{getUserName(item[1]).ljust(17, ' ')}{item[2]}  {str(item[3]).ljust(6, ' ')}{item[4]}")
        else:
            print(f"{'user_name'.ljust(17, ' ')}{'date'.ljust(12, ' ')}prio  times")
            self.c.execute(f"SELECT * FROM {self.table_name} WHERE DATE = '{year_month_day}'")
            for item in self.c.fetchall():
                print(f"{getUserName(item[1]).ljust(17, ' ')}{item[2]}  {str(item[3]).ljust(6, ' ')}{item[4]}")
        
    def getAllUsers(self, year_month_day = str(datetime.date.today())):
        res = []
        for item in self.c.execute(f"SELECT USER_NAME from {self.table_name} WHERE DATE = '{year_month_day}'"):
            res.append(item[0])
        return res
            
    def close(self):
        self.conn.close()
    

def getUserName(cookie):
    try:
        r = re.compile(r"pt_pin=(.*?);")    #指定一个规则：查找pt_pin=与;之前的所有字符,但pt_pin=与;不复制。r"" 的作用是去除转义字符.
        userName = r.findall(cookie)        #查找pt_pin=与;之前的所有字符，并复制给r，其中pt_pin=与;不复制。
        #print (userName)
        userName = unquote(userName[0])     #r.findall(cookie)赋值是list列表，这个赋值为字符串
        #print(userName)
        return userName
    except Exception as e:
        print(e,"cookie格式有误！")
        exit(2)

def postUrl(request_url):
    response = requests.post(url=request_url['url'], verify=False, headers=request_url['headers'], data=request_url['body'])
    return response.json()


def filterCks(cks, url, body):
    request_url = {
        'url': url,
        'headers': {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            'origin': 'https://pro.m.jd.com',
            "Referer": "https://pro.m.jd.com/jdlite/active/3H885vA4sQj6ctYzzPVix4iiYN2P/index.html?lng=106.476617&lat=29.502674&sid=fbc43764317f538b90e0f9ab43c8285w&un_area=4_50952_106_0",
            "Cookie": "None",
            "User-Agent": userAgent(),
        },
        'body': body,
    }
    buf_cks = []
    for ck in cks:
        request_url['headers']['Cookie'] = ck
        response = requests.post(url=request_url['url'], verify=False, headers=request_url['headers'], data=request_url['body'])
        result = response.json()
        if 'subCode' in result.keys() and (result['subCode'] == 'A13' or result['subCode'] == 'A28'): # 今日已领取；很抱歉没抢到
            continue
        buf_cks.append(ck)
    return buf_cks


def exchange(process_id, cks, loop_times, request_url_dict, mask_dict):
    flag = False
    # request_url = {
    #     'url': url,
    #     'headers': {
    #         "Accept": "*/*",
    #         "Accept-Encoding": "gzip, deflate, br",
    #         "Accept-Language": "zh-cn",
    #         "Connection": "keep-alive",
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         'origin': 'https://pro.m.jd.com',
    #         "Referer": "https://pro.m.jd.com/jdlite/active/3H885vA4sQj6ctYzzPVix4iiYN2P/index.html?lng=106.476617&lat=29.502674&sid=fbc43764317f538b90e0f9ab43c8285w&un_area=4_50952_106_0",
    #         "Cookie": "None",
    #         "User-Agent": userAgent(),
    #     },
    #     'body': body,
    # }

    # flag_arr = [True]*len(cks)
    for t in range(loop_times):
        # 每次loop的ua一样
        
        # request_url['headers']['User-Agent'] = userAgent()
        for i in range(len(cks)):
            ck = cks[i]
            request_url = request_url_dict[ck]
            if mask_dict[ck] <= 0: continue
            # if not mask_dict[ck]: continue
            # request_url['headers']['Cookie'] = ck
            # request_url['headers']['User-Agent'] = userAgent()
            response = requests.post(url=request_url['url'], verify=False, headers=request_url['headers'], data=request_url['body'])
            result = response.json()
            msg(f"进程：{process_id}-执行次数：{t+1}/{loop_times}\n账号：{getUserName(ck)} {result['subCode'] + ' : ' + result['subCodeMsg'] if 'subCodeMsg' in result.keys() else result}")
            # if 'subCode' in result.keys() and (result['subCode'] == 'D2' or result['subCode'] == 'A14' or result['subCode'] == 'A25'): # 当前时间段抢空；今日没了；火爆了
            # # if 'subCode' in result.keys() and (result['subCode'] == 'A14' or result['subCode'] == 'A25'): # 今日没了；火爆了
            #     flag = True
            #     break
            if 'subCode' in result.keys():
                # if result['subCode'] == 'D2' or result['subCode'] == 'A14' or result['subCode'] == 'A25': # 当前时间段抢空；今日没了；火爆了
                if result['subCode'] == 'D2' or result['subCode'] == 'A14' or result['subCode'] == 'A15': # 当前时间段抢空；今日没了；
                    # 直接停止该线程
                    msg("停止所有进程...")
                    flag = True
                    break
                if result['subCode'] == 'A1' or result['subCode'] == 'A13': # 领取成功；今日已领取；
                    # 停止该号
                    # flag_arr[i] = False
                    mask_dict[ck] = -1
                    msg(f"所有进程停止账号：{getUserName(ck)}")
                if result['subCode'] == 'A19' or result['subCode'] == 'A28': # 很抱歉没抢到
                    mask_dict[ck] = 0
                    msg(f"所有进程停止账号：{getUserName(ck)}")
                    

        if flag:
            break

def exchangeCoupons(url='https://api.m.jd.com/client.action?functionId=lite_newBabelAwardCollection&client=wh5&clientVersion=1.0.0', body='None', batch_size=4):

    debug_flag = False

    requests.packages.urllib3.disable_warnings()

    pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
    path = pwd + "env.sh"

    sid = ''.join (random.sample ('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    sid_ck = ''.join (random.sample ('123456789abcdef123456789abcdef123456789abcdef123456789abcdefABCDEFGHIJKLMNOPQRSTUVWXYZ', 43))

    cookies = os.environ["JD_COOKIE"].split('&')

    # 测试
    # cookies = cookies[-7:]

    if 'DATABASE_TYPE' in os.environ and \
        'DATABASE_HOST' in os.environ and \
        'DATABASE_PORT' in os.environ and \
        'DATABASE_USER' in os.environ and \
        'DATABASE_PASSWD' in os.environ and \
        'DATABASE_DATABASE' in os.environ:
        database_dict = {
                    "type":     os.environ['DATABASE_TYPE'],
                    "host":     os.environ['DATABASE_HOST'],       # 数据库主机地址
                    "port":     os.environ['DATABASE_PORT'],
                    "user":     os.environ['DATABASE_USER'],    # 数据库用户名
                    "passwd":   os.environ['DATABASE_PASSWD'],   # 数据库密码
                    "database": os.environ['DATABASE_DATABASE']
                }
    else:
        database_dict = {
                    'type': 'sqlite',
                    'name': "filtered_cks.db"
                }

    # 存入数据库
    database = SQLProcess(body, database_dict)
    # 插入所有数据，如果存在则更新
    insert_start = time.time()
    for i, ck in enumerate(cookies):
        database.insertItem(ck, time.time(), str(datetime.date.today()), len(cookies) - i)
    insert_end = time.time()
    print("\n插入/更新数据库操作耗时为：{:.2f}s\n".format(insert_end - insert_start))


    print('\n更新前数据库如下：')
    database.printTodayItems()

    # 可修订仓库batch size
    cookies, visit_times = database.filterUsers(batch_size)

    # 每个账户的请求头及UA固定
    request_url_dict = {}
    for ck in cookies:
        request_url_dict[ck] = {
            'url': url,
            'headers': {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                'origin': 'https://pro.m.jd.com',
                "Referer": "https://pro.m.jd.com/jdlite/active/3H885vA4sQj6ctYzzPVix4iiYN2P/index.html?lng=106.476617&lat=29.502674&sid=fbc43764317f538b90e0f9ab43c8285w&un_area=4_50952_106_0",
                "Cookie": ck,
                "User-Agent": userAgent(),
            },
            'body': body,
        }

    # 将优先级最高的且权重最高的ck增加一次机会
    if len(set(visit_times)) > 1:
        max_times = max(visit_times)
        for i in range(len(visit_times)):
            if visit_times[i] == max_times:
                cookies.append(cookies[i])
                break
    
    print("\n待抢账号：")
    print("\n".join([getUserName(ck) for ck in cookies]), '\n')

    process_number = 8

    # 进程共享数据, -1为抢到，0为火爆
    mask_dict = multiprocessing.Manager().dict()
    for ck in cookies:
        mask_dict[ck] = 1

    # 打乱数组
    cookies_array = []
    for i in range(process_number):
        random.shuffle(cookies)
        cookies_array.append(cookies.copy())

    msg().main()

    nex_minute = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
    waiting_time = (nex_minute - datetime.datetime.now()).total_seconds()
    loop_times = 10 // len(cookies) + 1

    if not debug_flag:
        msg(f"等待{waiting_time}s")

        # waiting # 部署时需要去掉注释
        time.sleep(max(waiting_time - 0.22, 0))

        msg("Sub-process(es) start.")
        process_number = 8
        pool = multiprocessing.Pool(processes = process_number)
        for i in range(process_number):
            # random.shuffle(cookies)
            pool.apply_async(exchange, args=(i+1, cookies_array[i], loop_times, request_url_dict, mask_dict, ))

        pool.close()
        pool.join()

        msg("Sub-process(es) done.")

    print()

    # 将为False的ck更新为负值
    for ck, state in mask_dict.items():
        if state <= 0:
            database.insertItem(ck, time.time(), str(datetime.date.today()), state)
        # else:
            # 当前尚未抢到时，权重+1，state为0时说明火爆，不自增
        database.addTimes(ck, str(datetime.date.today()))
        if state == -1:
            print(f"账号：{getUserName(ck)} 抢到优惠券")

    print('\n更新后数据库如下：')
    database.printTodayItems()

    database.close()