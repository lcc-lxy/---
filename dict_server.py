from threading import *
import time
import pymysql
from select import select
from socket import *
HOST = '0.0.0.0'
PORT = 8888
USER_NAME = []
class Server:
    def __init__(self):
        self.server_socket = socket()
        self.server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.server_socket.bind((HOST,PORT))
        self.rlist = []
        self.xlist = []
        self.wlist = []
        self.db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             database='dict',
                             charset='utf8'
                             )

    def server_forever(self):
        self.server_socket.listen(5)
        # 这是关注的IO
        self.rlist.append(self.server_socket)
        while True:
            rs, ws, xs = select(self.rlist,
                                self.wlist,
                                self.xlist)
            for r in rs:
                if r is self.server_socket:
                    c, addr = r.accept()
                    self.rlist.append(c)
                else:
                    self.handle(r)

    def handle(self, r):
        while True:
            data = r.recv(1024).decode()
            tmp = data.split(' ',1)
            # print(tmp[1])
            if not data:
                self.rlist.remove(r)
                r.close()
                return
            if tmp[0] == 'W': #查询单词
                self.look_mysql(tmp[1], r)
            elif tmp[0] == 'R':
                self.do_regin(tmp[1],r)
            elif tmp[0] =='L':
                self.do_log(tmp[1],r)
            elif tmp[0] == 'I':
                self.inquire(r)
#查询单词
    def look_mysql(self, data,r):

        cur = self.db.cursor()
        hist_sql = 'insert into hist (name,word) values (%s,%s)'
        cur.execute(hist_sql,[USER_NAME[-1],data])

        sql = 'select word,ex from words where word=%s'
        cur.execute(sql,data)
        word = cur.fetchone()
        self.db.commit()
        if not word:
            r.send('没有找到该单词'.encode())
        # print(a)
        else:
            tmp = '%s%s'%(word[0],word[1])
            r.send(tmp.encode())

#注册
    def do_regin(self, param, r): #注册
        cur = self.db.cursor()
        print(param)
        tmp = param.split(' ')
        sql = "select * from user where name=%s"
        cur.execute(sql, [tmp[0]])
        print(tmp[0])
        r1 = cur.fetchone()
        # print(r1+'到了r1')
        # 查找到说明用户存在
        if r1:
            r.send(b'False')
            # print('失败')
            return False

        # 插入用户名密码
        sql1 = "insert into user (name,pwd) \
                values (%s,%s)"
        try:
            # print('进入了try')
            cur.execute(sql1, [tmp[0], tmp[1]])
            # print('进入了execute')
            self.db.commit()
            # print('成功')
            r.send(b'OK')
            return True
        except:
            self.db.rollback()
#登录
    def do_log(self, param, r):
        cur = self.db.cursor()
        print(param)
        tmp = param.split(' ')

        sql = 'select * from user where name=%s and pwd=%s'
        cur.execute(sql,[tmp[0],tmp[1]])
        r1 = cur.fetchone()
        if r1:
            r.send(b'OK')
            USER_NAME.append(tmp[0])
            print(USER_NAME)
            return True
        else:
            r.send(b'False')
            return False

    def inquire(self,r):
        cur = self.db.cursor()
        sql = 'select name,word,time from hist order by time desc '
        cur.execute(sql)
        data = cur.fetchmany(10)
        # print(type(data))
        for item in data:
            msg = '%s     %-16s   %s'%item
            r.send(msg.encode())
            time.sleep(0.01)
        r.send(b'##')
        # s1 = str(data)
        # print(s1)
        # r.send(s1.encode())
if __name__ == '__main__':
    s1 = Server()
    # s1.look_mysql('book')
    # print(USER_NAME)
    s1.server_forever()
    # s1.inquire()