#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


from config import sqlFile as sqlFile_test
from qiniu import Auth, put_file, etag
import requests, os, pymysql, sys
# from config import sqlFile_test
import datetime, time
import json


sys.path.append(os.getcwd() + '/')
sys.path.append('/usr/local/python3/lib/python3.6/site-packages/')




class GetChinaMsg():
    def __init__(self):
        """
        初始化邮件正文的商品名称
        """
        self.excl_Uk_conn, self.excl_Uk_conn1, self.excl_Uk_cur1, self.excl_Uk_cur = sqlFile_test.excl_Uk()



    def GetHtml(self):
        """
        获取我们想要的网页 json 信息
        :return:
        """
        lensnkrs = 0
        last_json = None

        while lensnkrs < 200:

            reql = requests.get('https://api.nike.com/snkrs/content/v1/?country=GB&language=en-GB&offset=0&orderBy=published', timeout=5)
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

        country = 'SNKRS英国'        #国家

        sql1 = 'select distinct productid from monitor_result where distributionid=3 and `status`=3'

        try:
            self.excl_Uk_cur1.execute(sql1)

        except Exception as e:
            print('查询错误：{}'.format(e))

        SkuList = self.excl_Uk_cur1.fetchall()

        OldPublishTime = [i[0] for i in SkuList]

        for i in range(len(ShoesList)):

            replenishment_dict = {}

            seoSlug = ShoesList[i]['seoSlug']

            TheLinkadDress = 'https://www.nike.com/jb/launch/t/'+seoSlug

            ShoesSku = str(ShoesList[i]['product']['style']) + '-' + str(ShoesList[i]['product']['colorCode'])

            restricted = ShoesList[i]['restricted']

            productId = ShoesList[i]['id']

            if productId not in OldPublishTime and ShoesSku not in ['BQ4800-100', 'CD9329-001', 'AV4052-100', 'CK1905-100', 'CK1907-600', 'AO3189-001', 'AO3189-100']:

                if 'title' in ShoesList[i]['product'] and restricted is True:

                    title = str(ShoesList[i]['product']['title']).replace('\'', '').replace('\"', '')
                    imageUrl = ShoesList[i]['product']['imageUrl']

                    startSellDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    Additional_information = '专属>突袭'  # 附加信息


                    if 'skus' in ShoesList[i]['product']:

                        for j in ShoesList[i]['product']['skus']:

                            replenishment_dict[j['localizedSize']] = j['available']

                    access_key = '92SPonlDvYbu91VZOxvrHUmc9pHi3B8Wy5PUlzQ8'
                    secret_key = 'HZ8SyNcZr7IRRXQkrNwk0v17BsHkCeW9bsriikQZ'
                    q = Auth(access_key, secret_key)
                    bucket_name = 'instagram_img'

                    key = '{}.jpg'.format(productId)

                    token = q.upload_token(bucket_name, key, 3600)

                    r = requests.get(imageUrl, timeout=5)

                    with open('/root/snker_crawler/img/beauty_15.jpg', 'wb') as f:
                        f.write(r.content)

                    localfile = '/root/snker_crawler/img/beauty_15.jpg'
                    ret, info = put_file(token, key, localfile)
                    Img_url = 'http://putu4ibve.bkt.clouddn.com/' + json.loads(info.text_body).get('key')
                    assert ret['key'] == key
                    assert ret['hash'] == etag(localfile)

                    pushid = int(round(time.time() * 1000))

                    sql_1 = """INSERT INTO monitor_result (title, sku, distributionchannels, replenishmenttype, pushtime, picurl, size, `status`, createtime, distributionid, linkurl, productid, sortnum) VALUES("{}", "{}", 'SNKRS英国', '{}', now(), '{}', "{}", 3, now(), 3, '{}', '{}', 4)""".format(title, ShoesSku, Additional_information, Img_url, replenishment_dict, TheLinkadDress, productId)

                    try:
                        self.excl_Uk_cur1.execute(sql_1)

                    except Exception as e:
                        print('插入错误：{}'.format(e))

                    self.excl_Uk_conn1.commit()

                    Callbacdata = {
                        "title": "{}".format(title),
                        "sku": "{}".format(ShoesSku),
                        "distributionchannels": "{}".format(country),
                        "replenishmenttype": "{}".format(Additional_information),
                        "pushtime": "{}".format(startSellDate),
                        "picurl": "{}".format(Img_url),
                        "size": "{}".format(replenishment_dict),
                        "status": "0",
                        "createtime": "{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        "distributionid": "3",
                        "linkurl": "{}".format(TheLinkadDress),
                        "productid": "{}".format(productId),
                        "sortnum": "4",
                        "pushstatus": "0",
                        "pushid": "{}".format(pushid)
                    }

                    Callbacheader = {'Content-Type': 'application/json'}

                    now_time = datetime.datetime.now()
                    dt_minus1day1 = (now_time + datetime.timedelta(seconds=-4)).strftime('%Y-%m-%d %H:%M:%S')
                    dt_minus1day2 = (now_time + datetime.timedelta(seconds=+4)).strftime('%Y-%m-%d %H:%M:%S')

                    sql_7 = "SELECT * FROM monitor_result WHERE linkurl='{}' AND createtime BETWEEN '{}' AND '{}'".format(TheLinkadDress, dt_minus1day1, dt_minus1day2)

                    try:
                        self.excl_Uk_cur.execute(sql_7)
                    except Exception as E:
                        print(E)

                    Grab_judgment = self.excl_Uk_cur.fetchall()

                    if len(Grab_judgment) == 0:

                        try:
                            reqls = requests.post('http://mapi.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)
                            # reqls = requests.post('http://stest.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)

                            with open('/root/push/pushexclUK.log', 'a') as d:
                                d.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+str(reqls.text) + str(pushid))
                                d.write('\n')

                        except Exception as E:
                            print(E)



        if len(ShoeTitle) > 0:

            self.excl_Uk_cur.close()
            self.excl_Uk_conn.close()

            self.excl_Uk_cur1.close()
            self.excl_Uk_conn1.close()
            print('发送保存成功')







if __name__=="__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    GetChinaMsg = GetChinaMsg()
    GetChinaMsg.GetMsg()

