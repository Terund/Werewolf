import random
import copy
import json
import socket
from langrensha import *


udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 9099
buffer_size = 1024
udp_server.bind((host, port)) # 绑定系统服务端

addr_list = []
id_info_list = ["狼人", "狼人", "狼人", "平民", "平民", "平民", "女巫", "预言家", "猎人"]
data = {}

print('server start working...')


if __name__ == '__main__':
    # 9 人局 狼人杀游戏
    num = 9
    while len(addr_list) < num:
        name, addr = udp_server.recvfrom(1024)# 接收玩家的用户名和IP、端口
        name = name.decode('utf-8')
        if addr not in addr_list:# 判断玩家是否在列表中
            # print(addr)
            addr_list.append(addr)# 将IP、端口添加到列表中
            data[addr] = {'name': name, 'addr': addr}# 将玩家名字和IP、端口添加到字典里
            print(data)
            message = "游戏即将开始，请稍等...".encode('utf-8')
            udp_server.sendto(message, addr)# 将提示信息发送给客户端

    print("\033[1;32m玩家IP确定：\033[0m", addr_list)# 打印玩家列表

    # 系统随机分配身份 3个狼人 3 个平民 其他各一个
    new_addr_list = copy.deepcopy(addr_list)
    for id_info in id_info_list:
        choice_addr = random.choice(new_addr_list)
        # 对一个玩家增加一个身份
        data[choice_addr]['id_info'] = id_info
        new_addr_list.remove(choice_addr)
    # 打印玩家具体信息
    print("\033[1;32m玩家详细信息:\033[0m", data)

    # 游戏开始，系统通知玩家身份
    player_list = []
    wolf_list = []  # 狼人身份列表

    # 遍历玩家信息字典
    for k, v in data.items():
        person_id_info = v['id_info']# 获取玩家角色
        player_list.append(v['name'])# 给玩家列表增加玩家姓名
        # 发送身份信息给玩家
        message = "\033[1;32m游戏开始，您的身份：{}\033[0m".format(person_id_info).encode('utf-8')
        udp_server.sendto(message, k)# 将玩家身份发送到玩家所在地址
        # id_info指的是身份表示
        if v['id_info'] == '狼人':
            wolf_list.append(k)# 狼人存一个列表
    # 展示狼人玩家列表
    print("\033[1;32m狼人玩家：\033[0m", wolf_list)

    # 向每个玩家 展示本局所有玩家
    player_str = ''
    for a, b in enumerate(player_list, 1):
        print(a, b)
        player_str += str(a) + ' ' + b + '\n'

    for x in addr_list:
        udp_server.sendto("\033[1;32m本局所有玩家：\033[0m".encode('utf-8'), x)
        udp_server.sendto(player_str.encode('utf-8'), x)

    # 天黑了，请闭眼，狼人睁眼，相互确认身份，选择刀人
    live_player = copy.deepcopy(addr_list)
    message = "\033[1;34m天黑了，请闭眼...狼人睁眼 ...\033[0m".encode('utf-8')
    for x in addr_list:
        udp_server.sendto(message, x)












