import socket
import random
import copy
import json
import time

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 19099
buffer_size = 1024
udp_server.bind((host, port))  # 绑定系统服务端


# 游戏运行类
class RunGame(object):
    def __init__(self):
        # 存放玩家具体信息
        self.data = {}
        # 所有玩家的IP和端口号
        self.addr_list = []
        # 存活玩家的IP和端口号
        self.alive_list = []
        # 存放濒死玩家的IP和端口号
        self.going_live_list = []
        # 存放狼人的杀人选择{"狼人玩家IP和端口号":"被杀玩家的编号"}
        self.kill_choose = {}
        # 存放当前允许操作的IP和端口号
        self.can_operate = []
        # 存放狼人列表
        self.worf_list = []
        # 存放平民列表
        self.civilian_list = []
        # 存放预言家
        self.prophet = None
        # 存放女巫
        self.witch = None
        # 存放猎人
        self.huntsman = None

    # 游戏初始化
    def Initialization(self):
        # 存放游戏角色列表
        id_info_list = ["狼人", "狼人", "狼人", "平民", "平民", "平民", "女巫", "预言家", "猎人"]
        number = 0
        print('server start working...')
        # 等待玩家连接入
        while len(self.addr_list) < 9:
            name, addr = udp_server.recvfrom(1024)  # 接收玩家的用户名和IP、端口
            name = name.decode('utf-8')
            if addr not in self.addr_list:  # 判断玩家是否在列表中
                number += 1
                self.addr_list.append(addr)  # 将IP、端口添加到列表中
                self.data[addr] = {'number': number, 'name': name, 'addr': addr, 'live_status': 2}  # 将玩家编号和IP、端口添加到字典里
                print("第{}位玩家{}接入".format(number, name))
                message = "本次游戏中，您的编号为{}".format(number).encode('utf-8')
                udp_server.sendto(message, addr)  # 将提示信息发送给客户端
                message = "游戏即将开始，请稍等...".encode('utf-8')
                udp_server.sendto(message, addr)  # 将提示信息发送给客户端

        # 系统随机分配身份 3个狼人 3 个平民 其他各一个
        new_addr_list = copy.deepcopy(self.addr_list)
        for id_info in id_info_list:
            # 随机选取一个玩家ID
            choice_addr = random.choice(new_addr_list)
            # 对这个玩家增加一个身份
            self.data[choice_addr]['id_info'] = id_info
            # 将玩家ID从列表中移除
            new_addr_list.remove(choice_addr)
        # 打印玩家具体信息
        print("\033[1;32m玩家详细信息:\033[0m", self.data)

        # 将玩家编号和姓名发给每个玩家
        for k1, v1 in self.data.items():
            udp_server.sendto("\033[1;32m本局所有玩家：\033[0m".encode('utf-8'), k1)
            for k2, v2 in self.data.items():
                udp_server.sendto("\033[1;32m{}号玩家:{}\033[0m".format(v2['number'], v2['name']).encode('utf-8'), k1)
            # 宣布游戏开始，天黑请闭眼
            time.sleep(1)
            udp_server.sendto("\033[1;32m游戏开始，天黑请闭眼……\n-----狼人请睁眼-----\033[0m".encode('utf-8'), k1)

        # 遍历玩家信息列表，角色分配完毕，给每位玩家发放身份信息
        for addr in self.addr_list:
            player_id_info = self.data[addr]["id_info"]  # 获取玩家角色
            player_name = self.data[addr]["name"]  # 获取玩家编号
            player_number = self.data[addr]["number"]  # 获取玩家编号
            # 发送身份信息给玩家
            message = "\033[1;32m游戏开始，您的游戏编号为：{}，您的身份为：{}\033[0m".format(player_number, player_id_info).encode('utf-8')
            udp_server.sendto(message, addr)  # 将玩家身份发送到玩家所在地址
            # id_info指的是身份表示
            print("玩家编号：", player_number, "玩家名字", player_name, "玩家角色：", player_id_info)

    # 存放活着玩家和濒死玩家的IP和端口号
    def save_alive(self):
        self.alive_list = []
        self.going_die = []
        for addr in self.addr_list:
            # 记录存活的玩家的端口和IP
            if self.data[addr]["live_status"] == 2:
                self.alive_list.append(addr)
            # 存放濒死的玩家的端口和IP
            if self.data[addr]["live_status"] == 1:
                self.going_die.append(addr)

    # 将玩家IP和端口号根据身份分配到列表和变量中
    def save_info(self):
        self.worf_list = []
        self.civilian_list = []
        self.prophet = None
        self.witch = None
        self.huntsman = None
        for k, v in self.data.items():
            if v["live_status"] == 2:
                if v["id_info"] == "狼人":
                    self.worf_list.append(k)
                if v["id_info"] == "平民":
                    self.civilian_list.append(k)
                if v["id_info"] == "预言家":
                    self.prophet = k
                if v["id_info"] == "女巫":
                    self.witch = k
                if v["id_info"] == "猎人":
                    self.huntsman = k

    # 狼人的动作
    def langren(self):
        # 将狼人列表发给每个狼人玩家
        message = "狼人玩家有："
        for worf_port in self.worf_list:
            message += "\n{}号玩家：{}".format(self.data[worf_port]['number'], self.data[worf_port]['name'])
        for worf_port in self.worf_list:
            udp_server.sendto(message.encode('utf-8'), worf_port)

        # 将存活玩家列表发给狼人，并授予狼人发言权利
        message = "存活玩家有："
        for alive_port in self.alive_list:
            message += "\n{}号玩家：{}".format(self.data[alive_port]['number'], self.data[alive_port]['name'])
        for worf_port in self.worf_list:
            udp_server.sendto(message.encode('utf-8'), worf_port)

        # 循环捕获狼人输入内容，判断被狼人击杀的玩家
        self.kill_choose = {}
        be_kill = []  # 被击杀玩家的IP和端口号存一个列表
        last_time = time.time()  # 获取当前时间
        while True:
            message, addr = udp_server.recvfrom(1024)
            if message.decode('utf-8') in [str(x) for x in range(1, len(self.data))] and addr in self.addr_list:
                message = int(message.decode('utf-8'))
                if addr in self.worf_list:
                    if self.addr_list[message - 1] in self.alive_list:
                        self.kill_choose = {addr: message}
                        # 将从狼人处接收到的信息转发给每一位狼人
                        for worf in self.worf_list:
                            udp_server.sendto(
                                "{}号狼人玩家想击杀{}号玩家".format(self.data[addr]["number"], message).encode('utf-8'), worf)
                    else:
                        udp_server.sendto("该玩家不存在或已死亡，请重新选择".encode('utf-8'), addr)
                else:
                    udp_server.sendto("本阶段您无法操作".encode('utf-8'), addr)
            else:
                udp_server.sendto("您的输入不合法，请重新输入：".encode('utf-8'), addr)

            now_time = time.time()
            if now_time - last_time > 30:
                # 将狼人的杀人选择存放到列表里
                for k, v in self.kill_choose.items():
                    be_kill.append(self.addr_list[v - 1])
                # 分析狼人的杀人列表
                num = 0
                kill_addr = ()
                for addr in be_kill:
                    if be_kill.count(addr) > num:
                        num = be_kill.count(addr)
                        kill_addr = addr

                # 如果这个玩家地址在狼人的杀人列表里出现次数超过2次，或者狼人玩家仅有一个，将该玩家的状态设置为濒死
                if num >= 2 or len(self.worf_list) < 2:
                    self.data[kill_addr]["status"] = 1
                    for addr in self.worf_list:
                        udp_server.sendto(
                            "狼人今晚击杀的是{}号玩家{}".format(self.data[kill_addr]["number"], self.data[kill_addr]["name"]).encode(
                                'utf-8'), addr)
                    break
                else:
                    # 如果狼人之间没能协商好，重来
                    self.langren()
                    break

    def nvwu(self):
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
        # 卜永凡
        # 循环发言
        # 投票，票多者死，否则票多且票数一样多得人重新发言，直到有人出局
        pass


start_game = RunGame()
start_game.Initialization()
start_game.save_info()
start_game.save_alive()
start_game.langren()
