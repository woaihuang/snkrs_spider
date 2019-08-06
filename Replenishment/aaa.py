#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


from qiniu import Auth, put_file, etag
import requests, pymysql
import datetime
import json
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
        # reql = requests.get('http://47.111.128.125:8889/snkrs/?date={}'.format(date))
        reql = requests.get('http://127.0.0.1:8000/snkrs/?date={}'.format(date))

        print(reql.text)


    def selectDate(self):
        """
        数据库查询
        :param date:
        :return:
        """
        sql = 'select id, size, productid from monitor_result where distributionid=1 and `status`=0'
        try:
            self.cur1.execute(sql)
        except Exception as E:
            print("查询错误：{}".format(E))

        ReplenishmentList = self.cur1.fetchall()
        ReplenishmentId = [i[2] for i in ReplenishmentList]

        return ReplenishmentList, ReplenishmentId


    def GetHtml(self):
        """
        获取我们想要的网页 json 信息
        :return:
        """
        lensnkrs = 0
        last_json = None

        while lensnkrs < 200:
            reql = requests.get('{}'.format('https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published'))
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

        # ReplenishmentList, ReplenishmentId = self.selectDate()

        for i in range(len(ShoesList)):

            skustr, date = '', {}

            productId = ShoesList[i]['id']

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/cn/launch/t/'+seoSlug

            if 'title' in ShoesList[i]['product']:

                sql = 'select id, size, productid from monitor_result where distributionid=1 and `status`=0 and productid="{}"'.format(productId)
                try:
                    self.cur1.execute(sql)
                except Exception as E:
                    print("查询错误：{}".format(E))

                ReplenishmentList = self.cur1.fetchall()

                if ReplenishmentList:

                    OneShoeDict = eval(ReplenishmentList[0][1])                               #每双鞋的鞋码字典
                    
                    if 'skus' in ShoesList[i]['product']:

                        for j in ShoesList[i]['product']['skus']:

                            localizedSize = j['localizedSize']

                            if localizedSize in OneShoeDict:

                                if j['available'] != OneShoeDict[localizedSize] and OneShoeDict[localizedSize] is False:
                                    
                                    skustr = skustr + '/' + str(j['localizedSize'])

                                    OneShoeDict[localizedSize] = j['available']


                    if len(skustr) > 1:

                        sql_1 = """UPDATE monitor_result SET size="%s" WHERE id=%d""" % (str(OneShoeDict), int(ReplenishmentList[0][0]))
                        
                        try:
                            self.cur.execute(sql_1)

                        except Exception as E:
                            print("更改数据错误：{}".format(E))
                            
                        try:
                            self.cur1.execute(sql_1)

                        except Exception as e:
                            print('插入错误：{}'.format(e))

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

                        r = requests.get(imageUrl)

                        with open('/root/snker_crawler/img/beauty_6.jpg', 'wb') as f:
                            f.write(r.content)

                        localfile = '/root/snker_crawler/img/beauty_6.jpg'
                        ret, info = put_file(token, key, localfile)
                        Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                        assert ret['key'] == key
                        assert ret['hash'] == etag(localfile)

                        sql = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, picurl, size, `status`, createtime, distributionid, linkurl, productid) VALUES("{}", '{}', 'SNKRS中国', '{}', '{}', "{}", 1, now(), 1, '{}', '{}')""".format(title, ShoesSku, Additional_information, Img_url, replenishment_dict, TheLinkadDress, productId)

                        try:
                            self.cur.execute(sql)

                        except Exception as e:
                            print('插入错误：{}'.format(e))

                        try:
                            self.cur1.execute(sql)

                        except Exception as e:
                            print('插入错误：{}'.format(e))


                        date['productname'] = title
                        date['ShoesSku'] = ShoesSku
                        date['country'] = 'SNKRS中国'
                        date['information'] = Additional_information
                        date['replenishment'] = replenishment_dict
                        date['imageUrl'] = imageUrl
                        date['TheLinkadDress'] = TheLinkadDress

                        ShoeTitle.append(date)

        if len(ShoeTitle) > 0:
            for i in ShoeTitle:
                print(i)

            # self.weixinsend(ShoeTitle)

            self.conn.commit()
            self.cur.close()
            self.conn.close()

            self.conn1.commit()
            self.cur1.close()
            self.conn1.close()
            print('发送保存成功')






if __name__ == "__main__":
    GetChinaMsg = GetChinaMsg()

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    GetChinaMsg.GetMsg()



