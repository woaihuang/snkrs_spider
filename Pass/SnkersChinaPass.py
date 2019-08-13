#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from qiniu import Auth, put_file, etag
import requests, os, pymysql, sys
import datetime, time 
import smtplib
import json
import xlwt
import re


sys.path.append(os.getcwd() + '/')
sys.path.append('/usr/local/python3/lib/python3.6/site-packages/')




class GetChinaMsg():
    def __init__(self):
        """
        初始化邮件正文的商品名称
        """
        self.Pass_china_conn = pymysql.connect(
            host='rm-bp1ao27e2h337vf2c.mysql.rds.aliyuncs.com',
            user="bigdata_rw",
            password="Eyee@934",
            database="community",
            charset='utf8'
        )

        self.Pass_china_conn1 = pymysql.connect(
            host='rm-bp1nomodr5ingvn4k.mysql.rds.aliyuncs.com',                                        #内网
            # host='rm-bp1nomodr5ingvn4k4o.mysql.rds.aliyuncs.com',
            user="bigdata_analysis",
            password="bigdata_pwd123",
            database="analysis",
            charset='utf8'
        )
        self.Pass_china_cur1 = self.Pass_china_conn1.cursor()

        self.Pass_china_cur = self.Pass_china_conn.cursor()

        self.shoesname = ''
        self.date = {}




    def GetHtml(self):
        """
        获取我们想要的网页 json 信息
        :return:
        """
        lensnkrs = 0
        last_json = None

        while lensnkrs < 200:

            reql = requests.get('https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published', timeout=5)
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
        ShoeTitle = []

        reql, publishedDate, OldPublishTime = self.GetHtml(), '', ''

        ShoesList = reql['threads']

        country = 'SNKRS中国'        #国家

        sql1 = 'select distinct productid from monitor_result where distributionid=1 and `status`=2'

        try:
            self.Pass_china_cur1.execute(sql1)

        except Exception as e:
            print('查询错误：{}'.format(e))

        SkuList = self.Pass_china_cur1.fetchall()

        OldPublishTime = [i[0] for i in SkuList]


        for i in range(len(ShoesList)):

            date = {}

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/cn/launch/t/'+seoSlug

            if ShoesList[i]['id'] not in OldPublishTime:

                if 'title' not in ShoesList[i]['product']:

                    title = ShoesList[i]['name']
                    imageUrl = ShoesList[i]['imageUrl']
                    ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(ShoesList[i]['product']['colorCode'])

                    if ShoesSku not in ['BQ4800-100', 'CD9329-001', 'AV4052-100', 'CK1905-100', 'CK1907-600', 'AO3189-001', 'AO3189-100']:

                        if title != 'SNKRS Pass':
                            Additional_information = '发售'
                        else:
                            Additional_information = 'Pass'

                        startSellDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                        #开始销售时间

                        productId = ShoesList[i]['id']

                        access_key = '92SPonlDvYbu91VZOxvrHUmc9pHi3B8Wy5PUlzQ8'
                        secret_key = 'HZ8SyNcZr7IRRXQkrNwk0v17BsHkCeW9bsriikQZ'
                        q = Auth(access_key, secret_key)
                        bucket_name = 'instagram_img'

                        key = '{}.jpg'.format(productId)

                        token = q.upload_token(bucket_name, key, 3600)

                        r = requests.get(imageUrl, timeout=5)

                        with open('/root/snker_crawler/img/beauty_1.jpg', 'wb') as f:
                            f.write(r.content)

                        localfile = '/root/snker_crawler/img/beauty_1.jpg'
                        ret, info = put_file(token, key, localfile)
                        Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                        assert ret['key'] == key
                        assert ret['hash'] == etag(localfile)

                        pushid = int(round(time.time() * 1000))

                        sql_1 = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, `status`, createtime, distributionid, linkurl, productid) VALUES("{}", '{}', 'SNKRS中国', '{}', '{}', '{}', 2, now(), 1, '{}', '{}')""".format(title, ShoesSku, Additional_information, startSellDate, Img_url, TheLinkadDress, productId)



                        try:
                            self.Pass_china_cur1.execute(sql_1)

                        except Exception as e:
                            print('插入错误：{}'.format(e))

                        self.Pass_china_conn1.commit()

                        Callbacdata = {'id': pushid}

                        Callbacheader = {'Content-Type': 'application/json'}

                        now_time = datetime.datetime.now()
                        dt_minus1day1 = (now_time + datetime.timedelta(seconds=-2)).strftime('%Y-%m-%d %H:%M:%S')
                        dt_minus1day2 = (now_time + datetime.timedelta(seconds=+2)).strftime('%Y-%m-%d %H:%M:%S')

                        sql_7 = "SELECT * FROM monitor_result WHERE linkurl='{}' AND createtime BETWEEN '{}' AND '{}'".format(TheLinkadDress, dt_minus1day1, dt_minus1day2)

                        try:
                            self.Pass_china_cur.execute(sql_7)
                        except Exception as E:
                            print(E)

                        Grab_judgment = self.Pass_china_cur.fetchall()

                        if len(Grab_judgment) == 0:

                            sql = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, `status`, createtime, distributionid, linkurl, productid, sortnum, pushid) VALUES("{}", '{}', 'SNKRS中国', '{}', '{}', '{}', 0, now(), 1, '{}', '{}', 1, {})""".format(title, ShoesSku, Additional_information, startSellDate, Img_url, TheLinkadDress, productId, pushid)

                            try:
                                self.Pass_china_cur.execute(sql)

                            except Exception as e:
                                print('插入错误：{}'.format(e))

                            self.Pass_china_conn.commit()

                            reqls = requests.post('http://mapi.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)


                            with open('/root/push/passChina.log', 'a') as d:
                                d.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + str(reqls.text) + str(pushid))
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

            self.Pass_china_cur.close()
            self.Pass_china_conn.close()

            self.Pass_china_cur1.close()
            self.Pass_china_conn1.close()
            print('发送保存成功')






if __name__=="__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    GetChinaMsg = GetChinaMsg()
    GetChinaMsg.GetMsg()

