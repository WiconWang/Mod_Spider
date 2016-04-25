# coding:utf8
# 入库程序
import MySQLdb


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        try:
            conn = MySQLdb.connect(
                host='localhost', user='root', passwd='l9851223', db='python', port=3306, charset='utf8')
            cur = conn.cursor()

            for data in self.datas:
                value = [data['url'], data['title'].encode(
                    'utf-8'), data['summary'].encode('utf-8')]
                cur.execute(
                    'insert into spider (url,title,content) values(%s,%s,%s)', value)

            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        exit

        # 第二种写法
        # 以下是写入文件的写法
        # fout = open('output_html', 'w')

        # fout.write("<html>")
        # fout.write("<body>")
        # fout.write("<table>")

        # # ascii
        # for data in self.datas:
        #     fout.write("<tr>")
        #     fout.write("<td> %s </td>" % data['url'])
        #     fout.write("<td> %s </td>" % data['title'].encode('utf-8'))
        #     fout.write("<td> %s </td>" % data['summary'].encode('utf-8'))
        #     fout.write("</tr>")

        # fout.write("</table>")
        # fout.write("</body>")
        # fout.write("</html>")
