import base64
import socket

SERVER_IP = '54.234.205.119'
SERVER_PORT = 2525
IP = '77.137.112.37'

my_socket = socket.socket()
my_socket.connect((SERVER_IP, SERVER_PORT))
my_socket.send((f"EHLO {IP}" + "\n").encode())

login = input("Enter your login\n").encode()
password = input("Enter your password\n").encode()
sender = input("Enter you email address\n")
reciever = input('Enter recievers email address\n')

my_socket.send("AUTH LOGIN\r\n".encode())
my_socket.send(base64.encodebytes(login))
my_socket.send(base64.encodebytes(password))

my_socket.send((f"MAIL FROM: <{sender}>" + "\r\n").encode())
my_socket.send((f"RCPT TO: <{reciever}>" + "\r\n").encode())
my_socket.send("DATA\r\n".encode())
my_socket.send(
    (f"From: {input('Enter your name  ')} <{sender}>" + "\n").encode())
my_socket.send(
    (f"To: {input('Enter recievers name  ')} <{reciever}>" + "\n").encode())
my_socket.send((f"Subject: {input('Enter the subject  ')}" + "\n").encode())
my_socket.send((f'\n{input("Enter your message  ")}\r\n\r\n.\r\n').encode())
input()  # doesn't work without this line
my_socket.send("QUIT\r\n".encode())
input()  # doesn't work without this line
my_socket.close()


#   login:          6c116ec82b09ea
#   password:       45ff89bbed3398
#   sender email:   example@mail.com
#   reciever email: golanmor45@gmail.com
#   sender name:    Eviatar Butin
#   reciever name:  Golan Mor
#   mail subject:   Hello there
#   message:        Hello pal
