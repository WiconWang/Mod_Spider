# coding:utf8
# DB
import MySQLdb
import ConfigParser


class mysqldbhand:
    def __init__(self, logger):
        self.logger = logger

    def dbconnect(self):
        self.dbcon = None
        cf = ConfigParser.ConfigParser()
        cf.read("config.conf")
        try:
            self.dbcon = MySQLdb.connect(host='%s' % cf.get("db", "db_host"), user='%s' % cf.get("db", "db_user"), passwd='%s' % cf.get(
                "db", "db_pass"), db='%s' % cf.get("db", "db_name"), port=cf.getint("db", "db_port"), charset='utf8')
            self.con = self.dbcon.cursor()
            # self.con.close()
            # self.dbcon.close()
            self.logger.info("数据库已连接")
        except:
            self.logger.info("数据库连接失败")
            print("数据库连接失败")
            quit()

    def init_tables(self, table):
        if self.con.execute("""SHOW TABLES LIKE '%s'""" % (table)):
            print " * '%s'表已经存在，直接使用" % (table)
            pass
        else:
            try:
                sql1 = """CREATE TABLE if not exists `%s` (
      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `url` varchar(255) DEFAULT NULL,
      `title` varchar(255) DEFAULT NULL,
      `content` text,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """ % (table)
                self.con.execute(sql1)
                self.logger.info("数据表初始化成功")
            except MySQLdb.Error, e:
                self.logger.info("Mysql Error %d: %s" % (e.args[0], e.args[1]))
                # exit() 报错可能是表已存在，使其继续运行
                pass

    # 查找记录
    def FindAll(self, table, var='*', where=''):
        if where != '':
            where = ' where ' + where
        sql = "select " + var + " from " + table + where
        self.con.execute(sql)
        return self.con.fetchall()

    # 存在where字典时为更新，否则为新加
    def Save(self, table, info, where=[]):
        name = []
        value = []
        upstr = ''
        where_str = ''
        try:
            for k, v in info.iteritems():
                name.append("`%s`" % (str(k)))
                value.append("'%s'" % (str(v)))
                upstr += "`%s` = '%s', " % (str(k), str(v))
        except UnicodeEncodeError:
            pass
        namestr = ','.join(name)
        valuestr = ','.join(value)
        print upstr
        upstr = upstr[:-1]

        if where:
            for m, n in where.iteritems():
                where_str += "`%s` = '%s', " % (str(m), str(n))

            where_str = where_str[:-1]
            sql = "update `%s` set  %s where %s" % (table, upstr, where_str)
        else:
            sql = "insert into `%s` (%s) values (%s) " % (
                table, namestr, valuestr)
        print sql
        try:
            self.con.execute(sql)
            self.dbcon.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            pass
        except:
            pass
        pass
