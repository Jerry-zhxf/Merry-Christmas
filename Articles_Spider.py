# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb
import json
import pymysql
import time

def saveDataDB(datalist):
    __init__DB()
    db = pymysql.connect(host = 'localhost', user = 'root', passwd = '123456', db = 'PowerGrid')
    c = db.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 2:
                data[index] = time.strftime('%Y-%m-%d %H:%M', time.localtime(float(data[index])))
            data[index] = '"'+str(data[index])+'"'
        print(data)
        sql = '''
            insert ignore into `Articles`( `public_name`, `article_name`, `article_time`, `article_link`)  
            values(%s) '''%",".join(data)
        c.execute(sql)
        db.commit()

    db.close()

def __init__DB():
    s = '''
        create table if not exists Articles(
        id int primary key AUTO_INCREMENT not null,
        public_name text not null,
        article_name VARCHAR(256) not null unique,
        article_time text not null,
        article_link text not null
        );
    '''

    db = pymysql.connect(host = 'localhost', user = 'root', passwd = '123456', db = 'PowerGrid')
    c = db.cursor()
    c.execute(s)
    db.commit()
    db.close()

if __name__ == "__main__":
    datalist = []
    # 模拟登录微信公众号平台，获取微信文章的url
    cookie = "pgv_pvid=4964301240; fqm_pvqid=9647bd4d-808c-4e29-830a-d2222eb4e0b3; tvfe_boss_uuid=bb0ef2a4e3d83ac9; eas_sid=A1S67325r9k5a3P5o37783r4q4; LW_uid=J1o6Q3f6b2a5c978G5x9x6g3w2; LW_sid=U1h693l626V4f0A144Q4d9f7H5; RK=JxIVk027HC; ptcz=b201c4e9411deb5ee6ea2ee39703c868878b96a6747a2bfd972d179fbbcf9a98; uin_cookie=o1144237061; ied_qq=o1144237061; o_cookie=1144237061; pac_uid=1_1144237061; ua_id=6r2DvQUpTXq9HHrHAAAAAEnlCBuyfu681Hk084aR0hk=; wxuin=54439299669381; mm_lang=zh_CN; pgv_info=ssid=s5708586579; cert=w1Bw2ON9epaLkh2KNedvQgb8N4i9ojZ9; sig=h01abee291c9d4caa845c1a1f9daa4d6e8ec16bc036d558f920f4236abb62dd488c4348f8e4b471674d; uuid=8f115dcce0a2b2b9d9f7c0b130458ecb; bizuin=3879815152; ticket=a9cbe2272d2cd4869e836da01ff4294b0516a2ec; ticket_id=gh_80eedce4ca21; noticeLoginFlag=1; rand_info=CAESIAY8OfsgmBPUVEQorW4Q/H6TAfdGMyCpM6VBhegE9zBF; slave_bizuin=3879815152; data_bizuin=3879815152; data_ticket=v1X8zQcAXEYAk9k6m6vVZsgPVQb1N0bIVsfiDblhmZUhSmbt42+DjEmTQ5oC+qP3; slave_sid=bGJ1bkNTV0Y1Ym1oVlJNQjRjOTZuTVBfaDJZVUVJamQ2V2NFbzdBZFZ0cDNHTGRkOTROeFRSSTN4ZVdqZU9oVmNkVHNZaE5YTjJNVk4xajF5RXV6cHEwRHZtNDZnd0pnZ0ttMGFYMVFRSFlRNU1oc0t1SDI2OGREdmxVVThpMVc1dEFYa0NJNUg3VTUwSDl0; slave_user=gh_80eedce4ca21; xid=08c480be79a650e1c38cf08c56dd3334; openid2ticket_o8EdB59bebunpz-jqU5GjzsrRP08=fuw0SmU30Wzb57IeRwVNfJIB8qYPmhPKoaLD6gRraL8=; rewardsn=; wxtokenkey=777; wwapp.vid=; wwapp.cst=; wwapp.deviceid="
    token = "1687294214"
    nickname = ["南方电网95598", "国家电网", "广东电网", "电力网", "国家电网报", "电网头条", "国家电网杂志", "南方电网技术情报中心", "南方电网报", "广西电网"]
    biz = ["MzA3OTA2Mjc2MA==", "MzI2NDQ2ODMzMA==", "MzkxOTIzMzQ0Ng==", "MzA5NjA2ODIwNA==", "MzAxNDA1NjM2NA==", "MzI3MzAzMjMwNQ==", "MzA3NDAxNjM4NQ==", "MzAxNzQ5MjM4OQ==", "MjM5MjIwMjkxMQ==", "MzA3OTgwMzcxNA=="]
    paw = PublicAccountsWeb(cookie=cookie, token=token)
    
    for idx in range(0, len(nickname)):
        article_data = paw.get_urls(nickname[idx], biz[idx], begin="0", count="1")
        for info in article_data:
            data = []
            data.append(nickname[idx])
            data.append(info['title'])
            data.append(info['create_time'])
            data.append(info['link'])
            print(info['title'])
            print(info['create_time'])
            print(info['link'])
            datalist.append(data)

    saveDataDB(datalist)

    