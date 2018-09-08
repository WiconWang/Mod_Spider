#coding:utf-8
import configparser
import time

import pymysql
import re
import redis

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

pool = redis.ConnectionPool(host='%s' % (config.get("LOCAL_REDIS", "Host")), port=config.get("LOCAL_REDIS", "Port"), db=0)
r = redis.StrictRedis(connection_pool=pool)

for i in range(1, 80):
    aid = r.incr('dn:cls:id')
    # aid =9055
    sql = "select `body` from yy_addonarticle where aid = %s " % aid
    # print(sql)
    try:
        cur.execute(sql)
        res = cur.fetchone()
        # print(res)
        if not res:
            print('no records ID: %s' % (aid))
        else:
            body = res[0]
            body = re.sub('\[pp=([\s\S]*)pp\]', '', body)
            body = re.sub('\[[^\]]+\]', '', body)
            body = body.replace("<br />", "<br>")
            body = body.replace("\r<br>\n\r<br>\n", "<br>")
            body = body.replace("\r<br>\n", "")
            body = body.replace(" <br>", "<br>")
            body = body.replace("<br>\n", "<br>")
            body = body.replace("<br><br>", "<br>")
            body = body.replace("\n\n", "\n")
            body = body.replace("??", " ")
            body = re.sub('[\u4e00-\u9fa5]<br>', '', body)
            body = body.replace("版主提醒：阅文前请点击右边小手images/thanks.gif给作者点赞！", "")
            body = body.replace("版主提醒：阅文后请用你的认真回复支持作者！", "")
            body = body.replace("点击右边的小手images/thanks.gif同样可以给作者点赞！", "")
            body = body.replace("予人玫瑰:flower手留余香，", "")
            body = body.replace("希望您高抬贵手点一下右上角的", "")
            body = body.replace("http://i.imgur.com/XlA5IuC.png", "")
            body = body.replace("举手之劳:handshake", "")
            body = body.replace("您的支持:excellence 是我发帖的动力，谢谢:heart ！", "")
            body = body.replace("＊＊＊", "*")
            body = body.replace("。。", "。")
            body = body.replace("～～", "～")
            body = body.replace("┅┅", "…")
            body = body.replace("……", "…")
            body = body.replace("&nbsp;", " ")

            body = body.replace("　", " ")
            body = body.replace("  ", " ")

            mark_sql = 'update `yy_addonarticle` set `body`=\'%s\' where `aid`=\'%s\' ' %(body,aid)
            cur.execute(mark_sql)
            print('Success Change: aid: %s' % (aid))

    except Exception as e:
        raise e
    time.sleep(0.5)

db_local.close()
