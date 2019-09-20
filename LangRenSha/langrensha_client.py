import socket


sk_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_port = ('127.0.0.1', 9099)  # 狼人杀 裁判主机 ip  端口
buffer_size = 1024

name = input("请输入用户名：").strip().encode('utf-8')
sk_client.sendto(name, ip_port)


while True:
    message, addr = sk_client.recvfrom(buffer_size)
    print(message.decode('utf-8'))

