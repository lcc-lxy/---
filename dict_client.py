from socket import *
import getpass
HOST = '0.0.0.0'
PORT = 8888
class Client:
    def __init__(self):
        self.client_socket = socket()
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.client_socket.connect((HOST,PORT))
    def display1(self):
        s1 = '1注册'.center(10,'*')
        s2 = '2登录'.center(10,'*')
        s3 = '3退出'.center(10,'*')
        print(s1)
        print(s2)
        print(s3)
    def display2(self):
        s1 = '1查询单词'.center(10,'*')
        s2 = '2历史记录'.center(10,'*')
        s3 = '3退出'.center(10,'*')
        print(s1)
        print(s2)
        print(s3)
    def show(self):
        while True:
            self.display1()
            id = input('>>')
            if id == '1':
                self.do_regin()
            elif id == '2':
                self.do_log()
                self.show1()
            else:
                break
    def show1(self):
        while True:
            self.display2()
            id = input('>>')
            if id == '1':
                self.serch_words() #查询单词
            elif id == '2':
                self.inquire() #查看日志
            else:
                break
#查询单词
    def serch_words(self):  #差询单词
        data = 'W '
        data += input('请输入要查询的单词:')
        self.client_socket.send(data.encode())
        mes = self.client_socket.recv(1024)
        print(mes.decode())
    def main(self):
        self.show()
#注册
    def do_regin(self):  #注册
        while True:
            name = input('请输入用户名:')
            pwd = getpass.getpass()
            pwd1 = getpass.getpass()
            if pwd != pwd1:
                print('两次输入的密码不一样!请重新输入')
                continue
            st1 = 'R %s %s'%(name,pwd)
            self.client_socket.send(st1.encode())
            msg = self.client_socket.recv(128).decode()
            if msg == 'OK':
                print('注册成功!!')
                return
            else:
                print('注册失败')
            return
#登录
    def do_log(self):
        while True:
            name = input('请输入用户名:')
            pwd = getpass.getpass()
            st1 = 'L %s %s'%(name,pwd)
            self.client_socket.send(st1.encode())
            msg = self.client_socket.recv(128).decode()
            if msg == 'OK':
                print('登录成功!!')
                return
            else:
                print('登录失败')
                continue
#历史记录
    def inquire(self):
        st1 = 'I'
        self.client_socket.send(st1.encode())
        # while True:
        #     data = self.client_socket.recv(1024).decode()
        #     if not data:
        #         break
        #     tu.append(data)
        while True:
            data = self.client_socket.recv(1024).decode()
            if data == '##':
                break
            print(data)


        # print(tup)
        # for item in tup:
        #     print(item)
        # for i in tu:
        #     print(i)



if __name__ == '__main__':
    c1 = Client()
    c1.main()
    # c1.inquire()