import socket
import random

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 9099
buffer_size = 1024
udp_server.bind((host, port)) # 绑定系统服务端

ip_port = ('127.0.0.1', 9099)


class Person(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.addr = kwargs['addr']
        self.id_info = kwargs['id_info']
        self.live = 1

    def speak(self):
        message = input("请开始你的发言：").encode('utf-8')
        sk.sendto(message, ip_port)  # 将提示信息发送给客户端

    def vote(self):
        message = input("请开始你的发言：").encode('utf-8')
        sk.sendto(message, ip_port)  # 将提示信息发送给客户端

    def open_eye(self):
        pass

    def close_eye(self):
        pass


class Werewolf(Person):
    """
    狼人
    """

    def murder(self, other):
        """
        谋杀
        :param other:
        :return:
        """
        pass


class Villager(Person):
    pass


class StartGame(object):
    def __init__(self):
        self.addr_list = []
        self.id_info_list = ["狼人", "狼人", "狼人", "平民", "平民", "平民", "女巫", "预言家", "猎人"]
        self.data = {}

    # 游戏初始化
    def Initialization(self):
        print('server start working...')
        num = 9
        while len(self.addr_list) < num:
            name, addr = udp_server.recvfrom(1024)  # 接收玩家的用户名和IP、端口
            name = name.decode('utf-8')
            if addr not in self.addr_list:  # 判断玩家是否在列表中
                # print(addr)
                self.addr_list.append(addr)  # 将IP、端口添加到列表中
                self.data[addr] = {'name': name, 'addr': addr}  # 将玩家名字和IP、端口添加到字典里
                print(self.data)
                message = "游戏即将开始，请稍等...".encode('utf-8')
                udp_server.sendto(message, addr)  # 将提示信息发送给客户端

        print("\033[1;32m玩家IP确定：\033[0m", self.addr_list)  # 打印玩家列表


    # 晚上狼人的动作
    def langrensharen(self):
        # 王龙岩
        # 狼人睁眼
        # 系统将狼人列表和活着的人列表发给每一个狼人
        # 建立狼人与系统之间的回话，指定要杀的人的序号
        # 根据序号杀人，不一致就随机杀
        # 狼人闭眼
        pass

    def nvwudongzuo(self):
        # 方双盛
        # 是否救人
        # 是否毒人
        pass

    def show_live(self):
        # 每个人都写一份
        # 展示生存状态
        pass

    def yuyanjiadongzuo(self):
        # 陈晓磊
        # 查验身份
        pass

    def baitian(self):
        #卜永凡
        # 循环发言
        # 投票，票多者死，否则票多且票数一样多得人重新发言，直到有人出局
        pass
