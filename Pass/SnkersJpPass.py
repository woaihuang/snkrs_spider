#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

from qiniu import Auth, put_file, etag
import requests, pymysql
import datetime, time
import json




class GetChinaMsg():
    def __init__(self):
        """
        初始化邮件正文的商品名称
        """
        self.conn = pymysql.connect(
            host='rm-bp1ao27e2h337vf2c.mysql.rds.aliyuncs.com',
            user="bigdata_rw",
            password="Eyee@934",
            database="community",
            charset='utf8'
        )

        self.conn1 = pymysql.connect(
            host='rm-bp1nomodr5ingvn4k.mysql.rds.aliyuncs.com',                                        #内网
            # host='rm-bp1nomodr5ingvn4k4o.mysql.rds.aliyuncs.com',
            user="bigdata_analysis",
            password="bigdata_pwd123",
            database="analysis",
            charset='utf8'
        )
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

        print(reql.text)




    def GetHtml(self):
        """
        获取我们想要的网页 json 信息
        :return:
        """
        lensnkrs = 0
        last_json = None

        while lensnkrs < 200:
            reql = requests.get('https://api.nike.com/snkrs/content/v1/?&country=JP&language=ja&offset=0&orderBy=published', timeout=5)
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

        country = 'SNKRS日本'        #国家

        sql1 = 'select distinct productid from monitor_result where distributionid=4 and `status`=2'

        try:
            self.cur1.execute(sql1)

        except Exception as e:
            print('查询错误：{}'.format(e))

        SkuList = self.cur1.fetchall()

        OldPublishTime = [i[0] for i in SkuList]

        for i in range(len(ShoesList)):

            date = {}

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/jp/launch/t/'+seoSlug

            if ShoesList[i]['id'] not in OldPublishTime:

                if 'title' not in ShoesList[i]['product']:

                    title = ShoesList[i]['name']
                    imageUrl = ShoesList[i]['imageUrl']
                    ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(ShoesList[i]['product']['colorCode'])

                    if ShoesSku not in ['BQ4800-100', 'CD9329-001', 'AV4052-100', 'CK1905-100', 'CK1907-600',
                                        'AO3189-001', 'AO3189-100']:

                        if 'pass' not in imageUrl:
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

                        with open('beauty_2.jpg', 'wb') as f:
                            f.write(r.content)

                        localfile = 'beauty_2.jpg'
                        ret, info = put_file(token, key, localfile)
                        Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                        assert ret['key'] == key
                        assert ret['hash'] == etag(localfile)

                        pushid = int(round(time.time() * 1000))

                        sql_1 = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, `status`, createtime, distributionid, linkurl, productid) VALUES("{}", '{}', 'SNKRS日本', '{}', '{}', '{}', 2, now(), 4, '{}', '{}')""".format(title, ShoesSku, Additional_information, startSellDate, Img_url, TheLinkadDress, productId)

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

                            sql = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, `status`, createtime, distributionid, linkurl, productid, sortnum, pushid) VALUES("{}", '{}', 'SNKRS日本', '{}', '{}', '{}', 0, now(), 4, '{}', '{}', 3, {})""".format(
                                title, ShoesSku, Additional_information, startSellDate, Img_url, TheLinkadDress,
                                productId, pushid)

                            try:
                                self.cur.execute(sql)

                            except Exception as e:
                                print('插入错误：{}'.format(e))

                            self.conn.commit()

                            reqls = requests.post('http://stest.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)

                            with open('/root/push/pushpassJP.log', 'a') as d:
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
    GetChinaMsg = GetChinaMsg()
    
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    GetChinaMsg.GetMsg()
    print('查询完毕')
    



