# coding:utf8
# DB
import MySQLdb
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class mysqldbhand:

    def dbconnect(self):
        self.dbcon = None
        cf = ConfigParser.ConfigParser()
        cf.read("config.conf")
        try:
            self.dbcon = MySQLdb.connect(host='%s' % cf.get("db", "db_host"), user='%s' % cf.get("db", "db_user"), passwd='%s' % cf.get(
                "db", "db_pass"), db='%s' % cf.get("db", "db_name"), port=cf.getint("db", "db_port"), charset='utf8')
            self.con = self.dbcon.cursor()
        except:
            print("数据库连接失败")
            quit()

    # 根据project表和project_field表，初始化存放内容表结构
    # SETP1 在project表中填写新项目详细，并记住ID
    # SETP2 在project_field表中填写此项目的详细提取规则
    # 使用db.init_tables(ID)自动生成内容表结构
    # 注意适合于新项目使用，后期修改请去改mysql表结构
    def init_tables(self, projectnum):
        project = self.FindAll('project', '*', where='id= %s' % (projectnum))
        project_field = self.FindAll(
            'project_field', '*', where='pid= %s' % (projectnum))
        # print '项目 `%s` 收集启动 ' % (project[0][1])

        # 内容存储表结构
        sql_field = '`id` int(10) unsigned NOT NULL AUTO_INCREMENT,`isok` tinyint(4) unsigned NOT NULL DEFAULT 0,'
        for m in project_field:
            if m[3] == 'varchar':
                sql_field += '`%s` varchar(255) DEFAULT NULL,' % (m[2])
            elif m[3] == 'int':
                sql_field += '`%s` int(10) DEFAULT 0,' % (m[2])
            else:
                sql_field += '`%s` text DEFAULT NULL,' % (m[2])

        table = project[0][2]

        # 检测是否有本表，如果有直接使用当前表，不存在则新建
        if self.con.execute("""SHOW TABLES LIKE '%s_content'""" % (project[0][2])):
            print " * '%s_content'表已经存在，直接使用" % (project[0][2])
            pass
        else:
            try:
                sql = """CREATE TABLE if not exists `%s_content` ( %s PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (
                    table, sql_field)
                # print sql
                print " * '%s_content'表不存在，正在生成" % (project[0][2])
                self.con.execute(sql)
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
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
