#coding:utf-8
import configparser
import time

import pymysql


config = configparser.ConfigParser()
config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
db_local = pymysql.connect(
    host="%s" % config.get("LOCAL_MYSQL", "Host"),
    user="%s" % config.get("LOCAL_MYSQL", "User"),
    password="%s" % config.get("LOCAL_MYSQL", "Passwd"),
    db="%s" % config.get("LOCAL_MYSQL", "Db"),
    port=int(config.get("LOCAL_MYSQL", "Port")),
    charset="%s" % config.get("LOCAL_MYSQL", "Charset")
)
cur = db_local.cursor()

for i in range(1, 5000):
    sql_arctiny = "select `id` , `sourceurl`, `sourceid` from yy_arctiny where sourceid = 0 and sourceurl !=''  order by id asc limit 1"
    try:
        cur.execute(sql_arctiny)
        res_arc = cur.fetchone()
        if not res_arc:
            print('no records ID: %s' % (res_arc[0]))
        else:
            new_sid = res_arc[1]
            new_sid = new_sid.replace(".html", "")
            new_sid = new_sid.replace("http://%s/bbs/archiver/tid-" % (config.get("SITE_URL", "Url1")), "")
            new_sid = new_sid.replace("http://%s/bbs/archiver/tid-" % (config.get("SITE_URL", "Url2")), "")
            new_sid = new_sid.replace("http://%s/bbs/archiver/tid-" % (config.get("SITE_URL", "Url3")), "")
            mark_sql = 'update `yy_arctiny` set `sourceid`=\'%s\' where `id`=\'%s\' ' %(new_sid,res_arc[0])
            cur.execute(mark_sql)
            print('Success Change: id: %s, SouceID: %s' % (res_arc[0],new_sid))

    except Exception as e:
        raise e

    time.sleep(0.2)

db_local.close()
