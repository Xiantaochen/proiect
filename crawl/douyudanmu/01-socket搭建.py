import asyncore
import sys

#1,定义类，并继承自asynicore.diapatcher

class SockeClinet(asyncore.dispatcher):

    #实现类中的回调代码
    def __init__(self,host, port):
        #调用父类方法
        asyncore.dispatcher.__init__(self)

        #创建socket独享
        self.create_socket()

        #连接服务器
        addree = (host, port)
        self.connect(addree)
        pass

    #实现连接回调函数
    def handle_connect(self):
        print("连接成功")
        pass

    #实现writable函数
    def writable(self):
        return True

    # 实现handle_write函数
    def handle_write(self):
        self.send('hello world\n'.encode('utf-8'))

    # 实现readable函数
    def readable(self):
        return True

    # 实现handle_read函数
    def handle_read(self):
        result = self.recv(1024)
        print(result)

    # 实现hanlde_error函数
    def handle_error(self):
        t, e, trace = sys.exc_info()
        print(t,e,trace)

    # 实现handle_close函数
    def handle_close(self):
       print("连接关闭")
       self.close()

if __name__ == '__main__':
    client = SockeClinet("127.0.0.1",9000)

    asyncore.loop(timeout=5)