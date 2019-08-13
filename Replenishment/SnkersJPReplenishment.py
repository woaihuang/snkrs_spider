#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


from qiniu import Auth, put_file, etag
import requests, pymysql, os, sys
import datetime, time
import json
import re


sys.path.append(os.getcwd() + '/')
sys.path.append('/usr/local/python3/lib/python3.6/site-packages/')




class GetChinaMsg():
    def __init__(self):
        """
        初始化邮件正文的商品名称
        """
        self.Rep_JP_conn = pymysql.connect(
            host='rm-bp1ao27e2h337vf2c.mysql.rds.aliyuncs.com',
            user="bigdata_rw",
            password="Eyee@934",
            database="community",
            charset='utf8'
        )

        self.Rep_JP_conn1 = pymysql.connect(
            host='rm-bp1nomodr5ingvn4k.mysql.rds.aliyuncs.com',  # 内网
            # host='rm-bp1nomodr5ingvn4k4o.mysql.rds.aliyuncs.com',
            user="bigdata_analysis",
            password="bigdata_pwd123",
            database="analysis",
            charset='utf8'
        )
        self.Rep_JP_cur1 = self.Rep_JP_conn1.cursor()

        self.Rep_JP_cur = self.Rep_JP_conn.cursor()

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
            reql = requests.get('{}'.format(
                'https://api.nike.com/snkrs/content/v1/?&country=JP&language=ja&offset=0&orderBy=published'), timeout=5)
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

        country = 'SNKRS日本'  # 国家

        for i in range(len(ShoesList)):

            skustr, date = '', {}

            productId = ShoesList[i]['id']

            print(productId)

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/jp/launch/t/' + seoSlug

            ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(ShoesList[i]['product']['colorCode'])

            if 'title' in ShoesList[i]['product'] and ShoesSku not in ['BQ4800-100', 'CD9329-001', 'AV4052-100',
                                                                       'CK1905-100', 'CK1907-600', 'AO3189-001',
                                                                       'AO3189-100']:

                sql = 'select id, size, productid from monitor_result where distributionid=4 and `status`=0 and productid="{}"'.format(
                    productId)

                try:
                    self.Rep_JP_cur1.execute(sql)
                except Exception as E:
                    print("查询错误：{}".format(E))

                ReplenishmentList = self.Rep_JP_cur1.fetchall()

                if ReplenishmentList:

                    OneShoeDict = eval(ReplenishmentList[0][1])  # 每双鞋的鞋码字典

                    if 'skus' in ShoesList[i]['product']:

                        for j in ShoesList[i]['product']['skus']:

                            localizedSize = j['localizedSize']

                            if localizedSize in OneShoeDict:

                                if j['available'] != OneShoeDict[localizedSize] and OneShoeDict[localizedSize] is False:
                                    skustr = skustr + '/ ' + str(j['localizedSize'])

                                    OneShoeDict[localizedSize] = j['available']

                    if len(skustr) > 1:

                        sql_1 = """UPDATE monitor_result SET size="%s" WHERE id=%d""" % (
                        str(OneShoeDict), int(ReplenishmentList[0][0]))

                        try:
                            self.Rep_JP_cur1.execute(sql_1)

                        except Exception as e:
                            print('插入错误：{}'.format(e))

                        self.Rep_JP_conn1.commit()

                        title = ShoesList[i]['product']['title']
                        imageUrl = ShoesList[i]['product']['imageUrl']
                        ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(
                            ShoesList[i]['product']['colorCode'])

                        Additional_information = '补货'

                        replenishment_dict = skustr[1:]

                        access_key = '92SPonlDvYbu91VZOxvrHUmc9pHi3B8Wy5PUlzQ8'
                        secret_key = 'HZ8SyNcZr7IRRXQkrNwk0v17BsHkCeW9bsriikQZ'
                        q = Auth(access_key, secret_key)
                        bucket_name = 'instagram_img'

                        key = '{}.jpg'.format(productId)

                        token = q.upload_token(bucket_name, key, 3600)

                        r = requests.get(imageUrl, timeout=5)

                        with open('/root/snker_crawler/img/beauty_5.jpg', 'wb') as f:
                            f.write(r.content)

                        localfile = '/root/snker_crawler/img/beauty_5.jpg'
                        ret, info = put_file(token, key, localfile)
                        Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                        assert ret['key'] == key
                        assert ret['hash'] == etag(localfile)

                        pushid = int(round(time.time() * 1000))

                        Callbacdata = {'id': pushid}

                        Callbacheader = {'Content-Type': 'application/json'}

                        now_time = datetime.datetime.now()
                        dt_minus1day1 = (now_time + datetime.timedelta(seconds=-4)).strftime('%Y-%m-%d %H:%M:%S')
                        dt_minus1day2 = (now_time + datetime.timedelta(seconds=+4)).strftime('%Y-%m-%d %H:%M:%S')

                        sql_7 = "SELECT * FROM monitor_result WHERE linkurl='{}' AND createtime BETWEEN '{}' AND '{}'".format(
                            TheLinkadDress, dt_minus1day1, dt_minus1day2)

                        try:
                            self.Rep_JP_cur.execute(sql_7)
                        except Exception as E:
                            print(E)

                        Grab_judgment = self.Rep_JP_cur.fetchall()

                        if len(Grab_judgment) == 0:

                            sql = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, picurl, size, `status`, createtime, distributionid, linkurl, productid, sortnum, pushid)
                                                    VALUES("{}", '{}', 'SNKRS日本', '{}', '{}', "{}", 1, now(), 4, '{}', '{}', 3, {})""".format(
                                title, ShoesSku, Additional_information, Img_url, replenishment_dict, TheLinkadDress,
                                productId, pushid)

                            try:
                                self.Rep_JP_cur.execute(sql)

                            except Exception as e:
                                print('插入错误：{}'.format(e))

                            self.Rep_JP_conn.commit()

                            try:
                                self.Rep_JP_cur1.execute(sql)

                            except Exception as e:
                                print('插入错误：{}'.format(e))

                            self.Rep_JP_conn1.commit()

                            try:
                                reqls = requests.post('http://mapi.eyee.com/capi/community/monitor/open/push',
                                                      data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)

                                with open('/root/push/pushreplenishmentJP.log', 'a') as d:
                                    d.write(
                                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + str(reqls.text) + str(
                                            pushid))
                                    d.write('\n')
                            except Exception as E:
                                print(E)

                            date['productname'] = title
                            date['ShoesSku'] = ShoesSku
                            date['country'] = country
                            date['information'] = Additional_information
                            date['replenishment'] = replenishment_dict
                            date['imageUrl'] = imageUrl
                            date['TheLinkadDress'] = TheLinkadDress

                            ShoeTitle.append(date)

        if len(ShoeTitle) > 0:
            for i in ShoeTitle:
                print(i)

            # self.weixinsend(ShoeTitle)

            self.Rep_JP_cur.close()
            self.Rep_JP_conn.close()

            self.Rep_JP_cur1.close()
            self.Rep_JP_conn1.close()
            print('发送保存成功')





if __name__ == "__main__":
    GetChinaMsg = GetChinaMsg()

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    GetChinaMsg.GetMsg()

