import socket
import _thread


def reserve_message():
    while True:
        message, addr = udp_client.recvfrom(buffer_size)
        print(message.decode('utf-8'))


def send_message():
    while True:
        return_code = input()
        udp_client.sendto(return_code.encode(), ip_port)


if __name__ == "__main__":
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = ('127.0.0.1', 19099)  # 狼人杀 裁判主机 ip  端口
    buffer_size = 1024

    name = input("请输入用户名：").strip().encode('utf-8')
    udp_client.sendto(name, ip_port)
    _thread.start_new_thread(reserve_message, ())
    _thread.start_new_thread(send_message, ())
    while True:
        pass
