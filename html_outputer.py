# coding:utf8
# 入库程序
from DBmodel import mysqldbhand


class HtmlOutputer(object):
    global db
    global tablename

    def __init__(self, table):
        self.datas = []
        self.tablename = table

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        db = mysqldbhand()
        db.dbconnect()
        for data in self.datas:
            insert_data = {'url': data['url'], 'biaoti':data['title'].encode('utf-8'), 'jianjie': data['summary'].encode('utf-8')}
            res = db.Save(self.tablename, insert_data)
        exit

        # 第二种写法
        # 以下是写入文件的写法
        # fout = open('output_html', 'w')

        # fout.write("<html>")
        # fout.write("<body>")
        # fout.write("<table>")

        # ascii
        # for data in self.datas:
        #     fout.write("<tr>")
        #     fout.write("<td> %s </td>" % data['url'])
        #     fout.write("<td> %s </td>" % data['title'].encode('utf-8'))
        #     fout.write("<td> %s </td>" % data['summary'].encode('utf-8'))
        #     fout.write("</tr>")

        # fout.write("</table>")
        # fout.write("</body>")
        # fout.write("</html>")
