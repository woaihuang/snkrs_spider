#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

import pymysql


def sale_china():
    china_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    china_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    china_cur1 = china_conn1.cursor()

    china_cur = china_conn.cursor()

    return china_cur, china_cur1, china_conn1, china_conn


def sale_JP():
    JP_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    JP_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    JP_cur1 = JP_conn1.cursor()

    JP_cur = JP_conn.cursor()

    return JP_cur, JP_cur1, JP_conn, JP_conn1


def sale_UK():
    UK_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    UK_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    uk_cur1 = UK_conn1.cursor()

    uk_cur = UK_conn.cursor()

    return UK_conn, UK_conn1, uk_cur1, uk_cur


def sale_Usa():
    Usa_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Usa_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Usa_cur1 = Usa_conn1.cursor()

    Usa_cur = Usa_conn.cursor()

    return Usa_conn, Usa_conn1, Usa_cur1, Usa_cur


def excl_chain():
    excl_chain_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    excl_chain_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    excl_chain_cur1 = excl_chain_conn1.cursor()

    excl_chain_cur = excl_chain_conn.cursor()

    return excl_chain_conn, excl_chain_conn1, excl_chain_cur1, excl_chain_cur


def excl_JP():
    excl_JP_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    excl_JP_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    excl_JP_cur1 = excl_JP_conn1.cursor()

    excl_JP_cur = excl_JP_conn.cursor()

    return excl_JP_conn, excl_JP_conn1, excl_JP_cur1, excl_JP_cur


def excl_Uk():
    excl_Uk_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    excl_Uk_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    excl_Uk_cur1 = excl_Uk_conn1.cursor()

    excl_Uk_cur = excl_Uk_conn.cursor()

    return excl_Uk_conn, excl_Uk_conn1, excl_Uk_cur1, excl_Uk_cur


def excl_Usa():
    excl_Usa_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    excl_Usa_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    excl_Usa_cur1 = excl_Usa_conn1.cursor()

    excl_Usa_cur = excl_Usa_conn.cursor()

    return excl_Usa_conn, excl_Usa_conn1, excl_Usa_cur1, excl_Usa_cur


def Pass_china():
    Pass_china_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Pass_china_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Pass_china_cur1 = Pass_china_conn1.cursor()

    Pass_china_cur = Pass_china_conn.cursor()

    return Pass_china_conn, Pass_china_conn1, Pass_china_cur1, Pass_china_cur


def Pass_JP():
    Pass_JP_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Pass_JP_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Pass_JP_cur1 = Pass_JP_conn1.cursor()

    Pass_JP_cur = Pass_JP_conn.cursor()

    return Pass_JP_conn, Pass_JP_conn1, Pass_JP_cur1, Pass_JP_cur


def Pass_Uk():
    Pass_Uk_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Pass_Uk_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Pass_Uk_cur1 = Pass_Uk_conn1.cursor()

    Pass_Uk_cur = Pass_Uk_conn.cursor()

    return Pass_Uk_conn, Pass_Uk_conn1, Pass_Uk_cur1, Pass_Uk_cur


def Pass_Usa():
    Pass_Usa_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Pass_Usa_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Pass_Usa_cur1 = Pass_Usa_conn1.cursor()

    Pass_Usa_cur = Pass_Usa_conn.cursor()

    return Pass_Usa_conn, Pass_Usa_conn1, Pass_Usa_cur1, Pass_Usa_cur


def Rep_china():
    Rep_china_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Rep_china_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Rep_china_cur1 = Rep_china_conn1.cursor()

    Rep_china_cur = Rep_china_conn.cursor()

    return Rep_china_conn, Rep_china_conn1, Rep_china_cur1, Rep_china_cur



def Rep_JP():
    Rep_JP_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Rep_JP_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Rep_JP_cur1 = Rep_JP_conn1.cursor()

    Rep_JP_cur = Rep_JP_conn.cursor()

    return Rep_JP_conn, Rep_JP_conn1, Rep_JP_cur1, Rep_JP_cur


def Rep_Uk():
    Rep_Uk_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Rep_Uk_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Rep_Uk_cur1 = Rep_Uk_conn1.cursor()

    Rep_Uk_cur = Rep_Uk_conn.cursor()

    return Rep_Uk_conn, Rep_Uk_conn1, Rep_Uk_cur1, Rep_Uk_cur


def Rep_Usa():
    Rep_Usa_conn = pymysql.connect(
        host='rm-bp160wp5wbvzp4a6m.mysql.rds.aliyuncs.com',
        user="eyee",
        password="Eyeetest-181024",
        database="community_test",
        charset='utf8'
    )

    Rep_Usa_conn1 = pymysql.connect('localhost', user='root', password='Eyee@934', database='snkrs', charset='utf8')

    Rep_Usa_cur1 = Rep_Usa_conn1.cursor()

    Rep_Usa_cur = Rep_Usa_conn.cursor()

    return Rep_Usa_conn, Rep_Usa_conn1, Rep_Usa_cur1, Rep_Usa_cur
