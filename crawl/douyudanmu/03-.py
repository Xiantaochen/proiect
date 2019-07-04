'''
文件名：爬取斗鱼直播间信息到jsonline文件.py
'''
from __future__ import unicode_literals
import multiprocessing
import socket
import time
import re
import requests
from bs4 import BeautifulSoup
import json

# 配置socket的ip和端口
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

# 获取用户昵称及弹幕信息的正则表达式
danmu = re.compile(b'type@=chatmsg.*?/nn@=(.*?)/txt@=(.*?)/.*?/level@=(.*?)/.*?/bnn@=(.*?)/bl@=(.*?)/')


def sendmsg(msgstr):
    '''
    客户端向服务器发送请求的函数，集成发送协议头的功能
    msgHead: 发送数据前的协议头，消息长度的两倍，及消息类型、加密字段和保密字段
    使用while循环发送具体数据，保证将数据都发送出去
    '''
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def start(roomid):
    '''
    发送登录验证请求后，获取服务器返回的弹幕信息，同时提取昵称及弹幕内容
    登陆请求消息及入组消息末尾要加入\0
    '''
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    sendmsg(msg)
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    sendmsg(msg_more)

    print('---------------欢迎连接到{}的直播间---------------'.format(get_name(roomid)))
    while True:
        data = client.recv(1024)
        danmu_more = danmu.findall(data)
        if not data:
            break
        else:
            with open(format(get_name(roomid)) + time.strftime('%Y.%m.%d', time.localtime(time.time())) + '直播弹幕',
                      'a') as f:
                try:
                    for i in danmu_more:
                        dmDict = {}
                        # print(i)
                        dmDict['昵称'] = i[0].decode(encoding='utf-8', errors='ignore')
                        dmDict['弹幕内容'] = i[1].decode(encoding='utf-8', errors='ignore')
                        dmDict['等级'] = i[2].decode(encoding='utf-8', errors='ignore')
                        dmDict['徽章昵称'] = i[3].decode(encoding='utf-8', errors='ignore')
                        dmDict['徽章等级'] = i[4].decode(encoding='utf-8', errors='ignore')
                        dmJsonStr = json.dumps(dmDict, ensure_ascii=False) + '\n'
                        # print(dmDict['昵称'])
                        print(dmDict['弹幕内容'])
                        f.write(dmJsonStr)
                        danmuNum = danmuNum + 1
                except:
                    continue


def keeplive():
    '''
    发送心跳信息，维持TCP长连接
    心跳消息末尾加入\0
    '''
    while True:
        msg = 'type@=mrkl/\0'
        sendmsg(msg)
        time.sleep(45)


def get_name(roomid):
    '''
    利用BeautifulSoup获取直播间标题
    '''
    r = requests.get("http://www.douyu.com/" + roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'Title-anchorName'}).string


# 启动程序
if __name__ == '__main__':
    room_id = input('请输入房间ID： ')
    p1 = multiprocessing.Process(target=start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()