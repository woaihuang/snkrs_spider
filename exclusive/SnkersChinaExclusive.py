#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from qiniu import Auth, put_file, etag
import requests, os, pymysql
import datetime, time
import smtplib
import json
import xlwt
import re




class GetChinaMsg():
    def __init__(self):
        """
        初始化邮件正文的商品名称
        """
        self.conn = pymysql.connect(
            host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
            user="eyee",
            password="Eyeetest-181024",
            database="community_test",
            charset='utf8mb4'
        )

        self.conn1 = pymysql.connect("localhost", user='root', passwd='Eyee@934', db='snkrs', port=3306, charset='utf8mb4')
        self.cur1 = self.conn1.cursor()

        self.cur = self.conn.cursor()

        self.shoesname = ''
        self.date = {}


    def weixinsend(self, date):
        """
        微信发送接口
        :param date:
        :return:
        """
        reql = requests.get('http://47.111.128.125:8889/snkrs/?date={}'.format(date))
        # reql = requests.get('http://127.0.0.1:8000/snkrs/?date={}'.format(date))

        return reql.text




    def GetHtml(self):
        """
        获取我们想要的网页 json 信息
        :return:
        """
        lensnkrs = 0
        last_json = None

        while lensnkrs < 200:

            reql = requests.get('https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published')
            lensnkrs = len(reql.text)
            myjson = json.loads(reql.text)  # data是向 api请求的响应数据，data必须是字符串类型的
            newjson = json.dumps(myjson, ensure_ascii=False)  # ensure_ascii=False 就不会用 ASCII 编码，中文就可以正常显示了
            last_json = json.loads(newjson)

        return last_json



    def GetMsg(self):
        """
        获取我们想要的商品信息
        :return:
        """
        ShoeTitle, cccc = [], ''

        reql, publishedDate, OldPublishTime = self.GetHtml(), '', ''

        ShoesList = reql['threads']

        country = 'SNKRS中国'        #国家

        sql1 = 'select distinct productid from monitor_result where distributionid=1 and `status`=3'

        try:
            self.cur1.execute(sql1)

        except Exception as e:
            print('查询错误：{}'.format(e))

        SkuList = self.cur1.fetchall()

        OldPublishTime = [i[0] for i in SkuList]

        for i in range(len(ShoesList)):

            date = {}

            replenishment_dict = {}

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/cn/launch/t/'+seoSlug

            ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(ShoesList[i]['product']['colorCode'])

            restricted = ShoesList[i]['restricted']

            productId = ShoesList[i]['id']

            if productId not in OldPublishTime and ShoesSku not in ['BQ4800-100', 'CD9329-001', 'AV4052-100', 'CK1905-100', 'CK1907-600', 'AO3189-001', 'AO3189-100']:

                if 'title' in ShoesList[i]['product'] and restricted is True:

                    title = ShoesList[i]['product']['title']
                    imageUrl = ShoesList[i]['product']['imageUrl']

                    startSellDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    Additional_information = '专属购买'  # 附加信息

                    if 'skus' in ShoesList[i]['product']:

                        for j in ShoesList[i]['product']['skus']:

                            replenishment_dict[j['localizedSize']] = j['available']

                    access_key = '92SPonlDvYbu91VZOxvrHUmc9pHi3B8Wy5PUlzQ8'
                    secret_key = 'HZ8SyNcZr7IRRXQkrNwk0v17BsHkCeW9bsriikQZ'
                    q = Auth(access_key, secret_key)
                    bucket_name = 'instagram_img'

                    key = '{}.jpg'.format(productId)

                    token = q.upload_token(bucket_name, key, 3600)

                    r = requests.get(imageUrl)

                    with open('/root/snker_crawler/img/beauty_13.jpg', 'wb') as f:
                        f.write(r.content)

                    localfile = '/root/snker_crawler/img/beauty_13.jpg'
                    ret, info = put_file(token, key, localfile)
                    Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                    assert ret['key'] == key
                    assert ret['hash'] == etag(localfile)

                    pushid = int(round(time.time() * 1000))

                    sql = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, size, `status`, createtime, distributionid, linkurl, productid, sortnum, pushid) VALUES("{}", '{}', 'SNKRS中国', '{}', '{}', '{}', "{}", 0, now(), 1, '{}', '{}', 1, {})""".format(title, ShoesSku, Additional_information, startSellDate, Img_url, replenishment_dict, TheLinkadDress, productId, pushid)

                    try:
                        self.cur.execute(sql)

                    except Exception as e:
                        print('插入错误：{}'.format(e))

                    sql_1 = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, size, `status`, createtime, distributionid, linkurl, productid) VALUES("{}", '{}', 'SNKRS中国', '{}', '{}', '{}', "{}", 3, now(), 1, '{}', '{}')""".format(
                        title, ShoesSku, Additional_information, startSellDate, Img_url, replenishment_dict,
                        TheLinkadDress, productId)

                    try:
                        self.cur1.execute(sql_1)

                    except Exception as e:
                        print('插入错误：{}'.format(e))

                    Callbacdata = {'id': pushid}

                    Callbacheader = {'Content-Type': 'application/json'}

                    now_time = datetime.datetime.now()
                    dt_minus1day1 = (now_time + datetime.timedelta(seconds=-4)).strftime('%Y-%m-%d %H:%M:%S')
                    dt_minus1day2 = (now_time + datetime.timedelta(seconds=+4)).strftime('%Y-%m-%d %H:%M:%S')

                    sql_7 = "SELECT * FROM monitor_result WHERE linkurl='{}' AND createtime BETWEEN '{}' AND '{}'".format(
                        TheLinkadDress, dt_minus1day1, dt_minus1day2)

                    try:
                        self.cur.execute(sql_7)
                    except Exception as E:
                        print(E)

                    Grab_judgment = self.cur.fetchall()

                    if len(Grab_judgment) == 0:
                        self.conn.commit()
  
                        reqls = requests.post('http://stest.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader)

                        with open('/root/push/pushrexclChain.log', 'a') as d:
                            d.write(str(reqls.text))
                            d.write('\n')

                        date['productname'] = title
                        date['ShoesSku'] = ShoesSku
                        date['country'] = country
                        date['information'] = Additional_information
                        date['sellstarttime'] = startSellDate
                        date['imageUrl'] = imageUrl
                        date['TheLinkadDress'] = TheLinkadDress

                        ShoeTitle.append(date)

        if len(ShoeTitle) > 0:
            for i in ShoeTitle:
                print(i)

            # self.weixinsend(ShoeTitle)

            self.cur.close()
            self.conn.close()

            self.conn1.commit()
            self.cur1.close()
            self.conn1.close()
            print('发送保存成功')






if __name__=="__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    GetChinaMsg = GetChinaMsg()
    GetChinaMsg.GetMsg()

