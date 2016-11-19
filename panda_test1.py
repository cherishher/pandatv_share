# -*- coding: utf-8 -*-
# @Date    : 2016/11/17  21:34
# @Author  : 490949611@qq.com
# coding: utf-8
import urllib
import struct
import socket
import json
import time
import threading
import os
import platform
import demjson

def kmpTb(w):
    t = []
    pos = 2
    cnd = 0
    t.append(-1)
    t.append(0)
    while pos < len(w):
        if w[pos-1] == w[cnd]:
            t[pos] = cnd + 1
            cnd = cnd + 1
            pos = pos + 1
        elif cnd > 0:
            cnd = t[cnd]
        else:
            t[pos] = 0
            pos = pos + 1
    return t


CHATINFOURL = 'http://www.panda.tv/ajax_chatinfo?roomid='
DELIMITER = b'}}'
KMP_TABLE = kmpTb(DELIMITER)
IGNORE_LEN = 16
FIRST_REQ = b'\x00\x06\x00\x02'
FIRST_RPS = b'\x00\x06\x00\x06'
KEEPALIVE = b'\x00\x06\x00\x00'
RECVMSG = b'\x00\x06\x00\x03'
DANMU_TYPE = '1'
BAMBOO_TYPE = '206'
AUDIENCE_TYPE = '207'
SYSINFO = platform.system()
INIT_PROPERTIES = 'init.properties'
MANAGER = '60'
SP_MANAGER = '120'
HOSTER = '90'



def loadInit():
    with open(INIT_PROPERTIES, 'r') as f:
        init = f.read()
        init = init.split('\n')
        roomid = init[0].split(':')[1]
        #username = init[1].split(':')[1]
        #password = init[2].split(':')[1]
        return roomid


def notify(title, message):
    if SYSINFO == 'Windows':
        pass
    elif SYSINFO == 'Linux':
        os.system('notify-send {}'.format(': '.join([title, message])))
    else:   #for mac
        t = '-title {!r}'.format(title)
        m = '-message {!r}'.format(message)
        os.system('terminal-notifier {} -sound default'.format(' '.join([m, t])))


def getChatInfo(roomid):
    f = urllib.urlopen(CHATINFOURL + roomid)
    data = f.read().decode('utf-8')
    chatInfo = json.loads(data)
    chatAddr = chatInfo['data']['chat_addr_list'][0]
    socketIP = chatAddr.split(':')[0]
    socketPort = int(chatAddr.split(':')[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socketIP,socketPort))
    rid      = str(chatInfo['data']['rid']).encode('utf-8')
    appid    = str(chatInfo['data']['appid']).encode('utf-8')
    authtype = str(chatInfo['data']['authType']).encode('utf-8')
    sign     = str(chatInfo['data']['sign']).encode('utf-8')
    ts       = str(chatInfo['data']['ts']).encode('utf-8')
    msg  = b'u:' + rid + b'@' + appid + b'\nk:1\nt:300\nts:' + ts + b'\nsign:' + sign + b'\nauthtype:' + authtype
    msgLen = len(msg)
    sendMsg = FIRST_REQ + struct.pack(">H", msgLen) + msg
    s.sendall(sendMsg)
    print "send"
    recvMsg = s.recv(4)
    print recvMsg
    if recvMsg == FIRST_RPS:
        print(u'成功连接弹幕服务器')
        recvLen = struct.unpack(">H", s.recv(2))
    #s.send(b'\x00\x06\x00\x00')
    #print(s.recv(4))
    def keepalive():
        while True:
            #print('================keepalive=================')
            s.send(KEEPALIVE)
            time.sleep(300)
    threading.Thread(target=keepalive).start()

    while True:
        recvMsg = s.recv(4)
        if recvMsg == RECVMSG:
            recvLen = struct.unpack(">h", s.recv(2))[0]
            recvMsg = s.recv(recvLen)   #ack:0
            #print(recvMsg)
            recvLen = struct.unpack(">i", s.recv(4))[0]
            s.recv(IGNORE_LEN)
            recvLen -= IGNORE_LEN
            recvMsg = s.recv(recvLen)   #chat msg
            #print(recvMsg)
            try:
                analyseMsg(recvMsg)
            except Exception as e:
                pass



def analyseMsg(recvMsg):
    position = kmp(recvMsg, DELIMITER, KMP_TABLE)
    if position == len(recvMsg) - len(DELIMITER):
        formatMsg(recvMsg)
    else:
        preMsg = recvMsg[:position + len(DELIMITER)]
        formatMsg(preMsg)
        # analyse last msg
        analyseMsg(recvMsg[position + len(DELIMITER) + IGNORE_LEN:])

# pass one audience alert
is_second_audience = False
def formatMsg(recvMsg):
    try:
        jsonMsg = demjson.decode(recvMsg)
        content = jsonMsg['data']['content']
        if jsonMsg['type'] == DANMU_TYPE:
            identity = jsonMsg['data']['from']['identity']
            nickName = jsonMsg['data']['from']['nickName']
            try:
                spIdentity = jsonMsg['data']['from']['sp_identity']
                if spIdentity == SP_MANAGER:
                    nickName = '*超管*' + nickName
            except Exception as e:
                pass
            if identity == MANAGER:
                nickName = '*房管*' + nickName
            if identity == HOSTER:
                nickName = '*主播*' + nickName
            print(nickName + ":" + content)
            notify(nickName, content)
        elif jsonMsg['type'] == BAMBOO_TYPE:
            nickName = jsonMsg['data']['from']['nickName']
            print(nickName + "送给主播[" + content + "]个竹子")
            notify(nickName, "送给主播[" + content + "]个竹子")
        elif jsonMsg['type'] == AUDIENCE_TYPE:
            global is_second_audience
            if is_second_audience:
                print('===========观众人数' + content + '==========')
                is_second_audience = False
            else:
                is_second_audience = True
        else:
            pass
    except Exception as e:
        pass


def testRoomid(roomid):
    if not roomid:
        roomid = input('roomid:')
        with open(INIT_PROPERTIES, 'r') as f:
            init = f.readlines()
            editInit = ''
            for i in init:
                if 'roomid' in i:
                    i = i[:-1] + str(roomid)
                editInit += i + '\n'
        with open(INIT_PROPERTIES, 'w') as f:
            f.write(''.join(editInit))
    return roomid


def kmp(s, w, t):

    m = 0
    i = 0
    while m + i < len(s):
        if w[i] == s[m + i]:
            if i == len(w) - 1:
                return m
            i = i + 1
        else:
            if t[i] > -1:
                m = m + i - t[i]
                i = t[i]
            else:
                i = 0
                m = m + 1




# algorithm kmp_table:
#     input:
#         an array of characters, W (the word to be analyzed)
#         an array of integers, T (the table to be filled)
#     output:
#         nothing (but during operation, it populates the table)

#     define variables:
#         an integer, pos ← 2 (the current position we are computing in T)
#         an integer, cnd ← 0 (the zero-based index in W of the next
# character of the current candidate substring)

#     (the first few values are fixed but different from what the algorithm
# might suggest)
#     let T[0] ← -1, T[1] ← 0

#     while pos < length(W) do
#         (first case: the substring continues)
#         if W[pos-1] = W[cnd] then
#             let T[pos] ← cnd + 1, cnd ← cnd + 1, pos ← pos + 1

#         (second case: it doesn't, but we can fall back)
#         else if cnd > 0 then
#             let cnd ← T[cnd]

#         (third case: we have run out of candidates.  Note cnd = 0)
#         else
#             let T[pos] ← 0, pos ← pos + 1

def main():
    roomid = loadInit()
    roomid = testRoomid(roomid)
    getChatInfo(roomid)

if __name__ == '__main__':
    main()