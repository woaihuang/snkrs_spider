#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


from qiniu import Auth, put_file, etag
import requests, pymysql
import datetime
import json
import re






Callbacdata = {
    "title": "Nike x Stranger Things Cortez Upside Down",
    "sku": "CJ6107-100",
    "distributionchannels": "SNKRS美国",
    "replenishmenttype": "专属购买",
    "pushtime": "2019-08-15 15:19:17",
    "picurl": "http://putu4ibve.bkt.clouddn.com/fa7a91ee-ceaa-4c84-a615-a9782718d0a7.jpg",
    "size": "{'4.5': False, '5': False, '5.5': False, '6': False, '6.5': False, '7': False, '7.5': False, '8': False, '8.5': False, '9': True, '9.5': True, '10': True, '10.5': True, '11': True, '11.5': True, '12': True, '12.5': False, '13': True, '14': True, '15': True}",
    "status": "0",
    "createtime": "2019-08-15 15:19:17",
    "distributionid": "2", 
    "linkurl": "https://www.nike.com/us/launch/t/cortez-stranger-things-upside-down",
    "productid": "fa7a91ee-ceaa-4c84-a615-a9782718d0a7",
    "sortnum": "2",
    "pushstatus": "0",
    "pushid": "1565853557196"
}

Callbacheader = {'Content-Type': 'application/json'}
reqls = requests.post('http://stest.eyee.com/capi/community/monitor/open/push', data=json.dumps(Callbacdata), headers=Callbacheader, timeout=5)

print(reqls.text)

