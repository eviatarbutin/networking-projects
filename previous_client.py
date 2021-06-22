import socket
import base64

# Eviatar Butin
user_quit = False
my_socket = socket.socket()
my_socket.connect(('54.213.229.251', 587))
my_socket.send(bytes("EHLO", "utf-8"))
login = str(input("please enter your email address"))
password = str(input("please enter you email password"))
auth_encoding = base64.b64encode(bytes(login + " " + password, "utf-8"))
while not user_quit:
    my_socket.send(bytes(f"AUTH PLAIN {auth_encoding}", "utf-8"))
    my_socket.send(bytes(f"MAIL FROM:<{login}>", "utf-8"))
    my_socket.send(bytes(f"RCPT TO:{str(input('Please enter the email address of the receiver'))}", "utf-8"))
    more_receivers = True if input("Do you have more receivers for this message") == "yes" else False
    while more_receivers:
        my_socket.send(bytes(f"RCPT TO:{str(input('Please enter the email address of the receiver'))}", "utf-8"))
        more_receivers = True if input("Do you have more receivers for this message") == "yes" else False
    my_socket.send(bytes("DATA", "utf-8"))  # only data
    my_socket.send(bytes(input("enter the message you want to send"), "utf-8"))
    user_quit = False if str(input("do you want to send another mail?")) == "yes" else True
my_socket.send(bytes("QUIT", "utf-8"))
my_socket.close()
# frusta@gmx.com
# Password1!
