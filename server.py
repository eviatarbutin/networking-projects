import socket
import os

LISTENING_PORT = 8080
LISTENING_ADDRESS = '0.0.0.0'
NUMBER_OF_CLIENTS_ALLOWED = 1
STARTING_DIRECTORY = r'C:\Users\USER\Desktop\python\protocols\HTTP'
# python Desktop\python\protocols\HTTP\server.py


class HTTPServer:
    def __init__(self):
        self.server = socket.socket()
        self.server.bind((LISTENING_ADDRESS, LISTENING_PORT))
        self.get_client()

    def get_client(self):
        self.server.listen(NUMBER_OF_CLIENTS_ALLOWED)
        self.talk()

    def get_msg(self):
        data = self.client.recv(1024).decode('utf-8')
        if data != '' and data != ' ':
            return data

    def talk(self):
        while True:
            self.client, self.client_address = self.server.accept()
            data = self.client.recv(1024).decode('utf-8')
            rows = data.split('\r\n')
            if data != '':
                first_row = rows[0].split(' ')
                if first_row[0] == 'GET' and (first_row[2] == 'HTTP/1.1' or first_row[2] == 'HTTP/1.0'):
                    file_path = STARTING_DIRECTORY + \
                        first_row[1].replace('/', '\\')
                    if(file_path == STARTING_DIRECTORY+'\\'):
                        file_path += 'index.html'
                    if(os.path.isfile(file_path)):
                        if file_path ==STARTING_DIRECTORY + "\\page1.html":
                            file_path = STARTING_DIRECTORY + "\\page.html"
                            print(302)
                            self.client.sendall('HTTP/1.0 302 Moved Temporarily\r\nLocation: /page.html\r\n\r\n'.encode())
                        file = open(file_path, 'rb')
                        file = file.read()
                        self.file_length = str(len(file))
                        print('length est')
                        self.client.sendall(
                            (f'HTTP/1.0 200 OK\r\nContent-Length: {self.file_length}\r\nContent-Type: {self.content_type(file_path)}\r\n\r\n'.encode()))
                        print('poslal')
                        self.client.sendall(file)
                    else:
                        self.client.sendall('HTTP/1.0 404 Not Found\r\n\r\n'.encode())
                        print(404)
                        break
                else:
                    print(500)
                    self.client.sendall('HTTP/1.0 500 Internal Server Error\r\n\r\n'.encode())
                    break
        self.client.close()
        self.talk()
    def content_type(self, path: str):
        if path.endswith('html'):
            return 'text/html; charset=utf-8'
        if path.endswith('jpg'):
            return 'image/jpeg'
        if path.endswith('js'):
            return 'text/javascript; charset=UTF-8'
        if path.endswith('css'):
            return 'text/css'
        if path.endswith('ico'):
            return 'image/x-icon'

if __name__ == "__main__":
    s = HTTPServer()
