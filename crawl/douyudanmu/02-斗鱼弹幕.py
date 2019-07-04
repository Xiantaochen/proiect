import asyncore
import sys
import time
from queue import Queue
import threading

DATA_PACK_TYPE_SEND = 689
DATA_PACK_TYPE_RECV = 690

def encode_content(content):
    """
    序列化函数
    :param content:
    :return:
    """
    if isinstance(content,str):
        return content.replace(r"@",r"@A").replace(r"/",r"@S")
    elif isinstance(content,dict):
        return r'/'.join(["{}@={}".format(encode_content(k) ,encode_content(v)) for k, v in content.items()]) + r'/'
    elif isinstance(content,list):
        return r"/".join(([encode_content(data) for data in content])) + r"/"
    else:
        return ""

def decode_to_string(content):
    """
    反序列化字符串
    :param content:
    :return:
    """
    if isinstance(content,str):
        return content.replace(r"@S",r"/").replace('@A',r"@")
    return ""

def decode_to_dict(content):
    """
    反序列化字典
    :param content:
    :return:
    """
    ret_dict = dict()

    if isinstance(content,str):
        item_strings = content.split(r"/")
        for item_string in item_strings:
            k_v_list = item_string.split(r'@=')
            if k_v_list is not None and len(k_v_list) > 1:
                k = k_v_list[0]
                v = k_v_list[1]
                ret_dict[decode_to_string(k)] =decode_to_string(v)
        return ret_dict
    return ""

def decode_to_list(content):
    """
    反序列化列表数据
    :param content:
    :return:
    """
    ret_list = []
    if isinstance(content,str):
        items = content.split(r"/")
        for idx, item in enumerate(items):
            if idx <len(items) -1:
                ret_list.append(decode_to_string(item))
    return ret_list

class DataPacket():
    def __init__(self,type = DATA_PACK_TYPE_SEND,content = "",data_bytes =None):
        if data_bytes ==None:
            self.type = type
            self.content = content
            self.encrypt_flag = 0
            self.preserve_flag = 0
        else:
            self.type = int.from_bytes(data_bytes[4:6],byteorder="little",signed=False)
            self.encrypt_flag = int.from_bytes(data_bytes[6:7],byteorder="little",signed=False)
            self.preserve_flag = int.from_bytes(data_bytes[7:8],byteorder="little",signed=False)
            self.content = str(data_bytes[8:-1],encoding="utf-8",errors='ignore')


    def get_length(self):
        """
        获取当前数据包的长度，为以后需要发送的数据做准备
        :return:
        """

        return 4 + 2 + 1 + 1 + len(self.content.encode(encoding='utf-8', errors='ignore')) + 1

    def get_bytes(self):
        data = bytes()
        #构建 4 个字节的消息长度数据
        data_package_length = self.get_length()
        #to_byte 把一个整型数据转换成二进制数据
        #第一个参数 把需要的转换的二进制数据占几个字节
        #第二个参数 描述字节数
        #第三个参数 设置是否有符号
        data += data_package_length.to_bytes(4, byteorder="little",signed=False)
        data += self.type.to_bytes(2, byteorder="little", signed=False)
        data += self.encrypt_flag.to_bytes(1, byteorder="little", signed=False)
        data += self.preserve_flag.to_bytes(1, byteorder="little", signed=False)
        data += self.content.encode(encoding='utf-8', errors='ignore')
        data += b"\0"
        return data

class DouyuClient(asyncore.dispatcher):
    def __init__(self,host, port,callback = None):
        #构建发送数据包的队列
        self.send_queue = Queue()

        #c存放接受的数据包
        self.recv_queue =Queue()

        #定义外部传入的回调函数
        self.callback = callback

        asyncore.dispatcher.__init__(self)
        self.create_socket()
        address = (host, port)
        self.connect(address)

        self.callback_thread = threading.Thread(target=self.do_callback)
        self.callback_thread.setDaemon(True)
        self.callback_thread.start()

        #构建心跳线程
        self.heart_thread = threading.Thread(target=self.do_ping)
        self.heart_thread.setDaemon(True)
        self.ping_runing = False
        pass

    def handle_connect(self):
        print("连接成功")
        self.start_ping()
        pass

    def writable(self):
        return self.send_queue.qsize() > 0

    def handle_write(self):
        #从发送数据包的队列中获取数据包对象
        dq = self.send_queue.get()

        #获取数据包的长度，并且发送给服务器
        dq_length = dq.get_length()
        dq_length_data = dq_length.to_bytes(4,byteorder="little",signed=False)
        self.send(dq_length_data)

        #发送数据包二进制数据
        self.send(dq.get_bytes())
        self.send_queue.task_done()
        pass



    def readable(self):
        return True

    def handle_read(self):
        #读取长度， 二进制数据
        data_length_data = self.recv(4)
        data_length = int.from_bytes(data_length_data,byteorder="little",signed=False)

        data = self.recv(data_length)
        #构建数据包对象
        dp =DataPacket(data_bytes=data)
        self.recv_queue.put(dp)


    def handle_error(self):
        t, e, trace = sys.exc_info()
        print(t, e, trace)
        self.close()

        # 实现handle_close函数

    def handle_close(self):
        print("连接关闭")
        self.stop_runing()
        self.close()

    def login_room_id(self,roomId):
        self.roomId = roomId
        send_data = {
            "type" :"loginreq",
            "roomId" : str(roomId)
        }
        # 构建登录数据包
        content = encode_content(send_data)
        login_dq = DataPacket(DATA_PACK_TYPE_SEND,content=content)
        self.send_queue.put(login_dq)

    def join_room_group(self):
        """
        加入弹幕分组
        :return:
        """
        send_data = {
            "type" :"joingroup",
            "rid":str(self.roomId),
            "gid":'-9999'
        }
        content = encode_content(send_data)
        dq = DataPacket(type=DATA_PACK_TYPE_SEND,content = content)
        self.send_queue.put(dq)
        pass

    def send_heart_data_packet(self):
        send_data = {
            "type":"mrkl"
        }
        content = encode_content(send_data)
        dq = DataPacket(type=DATA_PACK_TYPE_SEND,content=content)
        self.send_queue.put(dq)

    def do_ping(self):
        while True:
            if self.ping_runing:
                self.send_heart_data_packet()
                time.sleep(40)

    def start_ping(self):
        """
        开始心跳
        :return:
        """
        self.ping_runing = True

    def stop_runing(self):
        """
        停止心跳
        :return:
        """
        self.ping_runing = False

    def do_callback(self):
        """
        专门负责处理接受数据包容器中的数据
        :return:
        """
        while True:
            dq = self.recv_queue.get()
            if self.callback is not None:
                self.callback(self,dq)
            self.recv_queue.task_done()
        pass

def data_callback(client,dp):
    """
    自定义回调函数
    :param dp:
    :return:
    """
    response = decode_to_dict(dp.content)
    if response['type'] == "loginres":
        print("登录成功 :",response)
        client.join_room_group()
        pass
    elif response["type"] == "chatmsg":
        print("{}:{}".format(response["nn"],response["txt"]))
    pass

if __name__ == '__main__':
    room_id = input('请输入房间ID： ')
    client  =DouyuClient("openbarrage.douyutv.com", 8601,callback = data_callback)
    client.login_room_id(room_id)
    asyncore.loop(timeout=5)

