# coding:utf-8
import configparser

import pymysql
import re

config = configparser.ConfigParser()
config.readfp(open('config.ini'))

db = pymysql.connect(
    host="%s" % config.get("AWS_MYSQL", "Host"),
    user="%s" % config.get("AWS_MYSQL", "User"),
    password="%s" % config.get("AWS_MYSQL", "Passwd"),
    db="%s" % config.get("AWS_MYSQL", "Db"),
    port=int(config.get("AWS_MYSQL", "Port")),
    charset="%s" % config.get("AWS_MYSQL", "Charset")
)
cur = db.cursor()

db_local = pymysql.connect(
    host="%s" % config.get("LOCAL_MYSQL", "Host"),
    user="%s" % config.get("LOCAL_MYSQL", "User"),
    password="%s" % config.get("LOCAL_MYSQL", "Passwd"),
    db="%s" % config.get("LOCAL_MYSQL", "Db"),
    port=int(config.get("LOCAL_MYSQL", "Port")),
    charset="%s" % config.get("LOCAL_MYSQL", "Charset")
)
cur_local = db_local.cursor()

sql_arctiny = "select `id`, `typeid`, `typeid2`, `arcrank`, `channel`, `senddate`, `sortrank`, `mid`, `linkmd5id`," \
              " `sourceurl`, `sourceid`, `ismoved` from yy_arctiny where ismoved = 0  order by id asc limit 1"
try:
    cur.execute(sql_arctiny)
    res_arc = cur.fetchone()
    if not res_arc:
        if res_arc == None:
            print('no records ID: %s' % (res_arc))
        else:
            print('no records ID: %s' % (res_arc[0]))
    else:
        sql_exist_arctiny = 'select `id` from yy_arctiny where  sourceid = %s' % (res_arc[10])
        # print(sql_exist_arctiny)
        cur_local.execute(sql_exist_arctiny)
        res_exist_arc = cur_local.fetchone()
        print(res_exist_arc)
        if res_exist_arc:
            mark_sql = 'update `yy_arctiny` set `ismoved`=\'1\' where `id`=\'%s\' ' % (res_arc[0])
            cur.execute(mark_sql)
            print('exist source ID: %s' % (res_arc[10]))
        else:
            local_sql_arctiny = 'insert into `yy_arctiny` ( `typeid`, `typeid2`, `arcrank`, `channel`, ' \
                                '`senddate`, `sortrank`, `mid`, `linkmd5id`, `sourceurl`, `sourceid`) ' \
                                'values ( \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' \
                                % (res_arc[1], res_arc[2], res_arc[3], res_arc[4], res_arc[5],
                                   res_arc[6], res_arc[7], res_arc[8], res_arc[9], res_arc[10])
            cur_local.execute(local_sql_arctiny)
            id_local = cur_local.lastrowid
            if id_local:
                # 继续后续
                sql_archives = 'select `typeid`, `typeid2`, `sortrank`, `flag`, `ismake`, ' \
                               '`channel`, `arcrank`, `click`,`money`, `title`, `shorttitle`, `color`, `writer`,' \
                               ' `source`, `litpic`, `pubdate`, `senddate`,`mid`, `keywords`, `lastpost`, `scores`,' \
                               ' `goodpost`, `badpost`, `notpost`, `description`, `filename`, `dutyadmin`, `tackid`,' \
                               ' `mtype`, `weight`, `duplicate` from yy_archives where id = %s' % (res_arc[0])
                # print(sql_archives)
                cur.execute(sql_archives)
                res_av = cur.fetchone()
                description = res_av[24]
                description = re.sub('\[[^\]]+\]', '', description)
                description = description.replace("<br>", "").replace("<br />", "").replace("\n", "") \
                    .replace("\t", "").replace("??", "").replace(" ", "")
                local_sql_archives = 'insert into `yy_archives`(`id`, `typeid`, `typeid2`, `sortrank`, `flag`, `ismake`, ' \
                                     '`channel`, `arcrank`, `click`,`money`, `title`, `shorttitle`, `color`, `writer`,' \
                                     ' `source`, `litpic`, `pubdate`, `senddate`,`mid`, `keywords`, `lastpost`, `scores`,' \
                                     ' `goodpost`, `badpost`, `notpost`, `description`, `filename`, `dutyadmin`, `tackid`,' \
                                     ' `mtype`, `weight`, `duplicate`) values(\'%s\',\'%s\',\'%s\',\'%s\',null,\'%s\',' \
                                     '\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',' \
                                     '\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',' \
                                     '\'%s\',\'%s\')' % (id_local, res_av[0], res_av[1], res_av[2], res_av[4],
                                                         res_av[5], res_av[6], res_av[7], res_av[8], res_av[9],
                                                         res_av[10], res_av[11], res_av[12], res_av[13],
                                                         res_av[14], res_av[15], res_av[16], res_av[17],
                                                         res_av[18], res_av[19], res_av[20], res_av[21],
                                                         res_av[22], res_av[23], description, res_av[25],
                                                         res_av[26], res_av[27], res_av[28], res_av[29],
                                                         res_av[30])
                # print(local_sql_archives)
                cur_local.execute(local_sql_archives)

                # 继续内容
                sql_addon = 'select `typeid`, `body` from yy_addonarticle where aid = %s' % (res_arc[0])
                # print(sql_addon)
                cur.execute(sql_addon)
                res_addon = cur.fetchone()
                # print(res_addon)
                addon_body = res_addon[1]

                addon_body = re.sub('\[pp=([\s\S]*)pp\]', '', addon_body)
                addon_body = re.sub('\[[^\]]+\]', '', addon_body)
                addon_body = addon_body.replace("<br />", "<br>").replace("\r<br>\n\r<br>\n", "<br>").replace(
                    "\r<br>\n", "") \
                    .replace("版主提醒：阅文前请点击右边小手images/thanks.gif给作者点赞！", "") \
                    .replace("版主提醒：阅文后请用你的认真回复支持作者！", "") \
                    .replace("点击右边的小手images/thanks.gif同样可以给作者点赞！", "") \
                    .replace("予人玫瑰:flower手留余香，", "").replace("希望您高抬贵手点一下右上角的", "") \
                    .replace("http://i.imgur.com/XlA5IuC.png", "").replace("举手之劳:handshake", "") \
                    .replace("您的支持:excellence 是我发帖的动力，谢谢:heart ！", "") \
                    .replace("＊＊＊", "*").replace("。。", "。").replace("～～", "～").replace("……", "…") \
                    .replace("　", " ").replace("  ", " ")

                local_sql_archives = 'insert into `yy_addonarticle`(`aid`, `typeid`, `body`) values(\'%s\',\'%s\',\'%s\')' % \
                                     (id_local, res_addon[0], addon_body)
                # print(local_sql_archives)
                cur_local.execute(local_sql_archives)

                # up make
                mark_sql = 'update `yy_arctiny` set `ismoved`=\'1\' where `id`=\'%s\' ' % (res_arc[0])
                cur.execute(mark_sql)
                print('Success moved: AID: %s, SouceID: %s' % (res_arc[0], res_arc[10]))



except Exception as e:
    raise e
finally:
    db.close()  # 关闭连接
