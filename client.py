import socket

# python Desktop\python\protocols\HTTP\client.py
CONNECTION_ADDRESS = '127.0.0.1'


class HTTPClient:
    def __init__(self):
        self.my_socket = socket.socket()
        self.my_socket.connect(('127.0.0.1', 8080))

    def send_msg(self, msg):
        self.my_socket.sendall(bytes(str(len(bytes(msg, "utf-8"))), 'utf-8'))
        print('length sent')
        self.my_socket.sendall(msg.encode('utf-8'))
        print('message sent')

    def get_msg(self):
        return self.my_socket.recv(1024)

    def __del__(self):
        print('closed')


if __name__ == "__main__":
    c = HTTPClient()
    c.send_msg('GET /moshe.txt HTTP/1.1\r\n')
    c.get_msg()