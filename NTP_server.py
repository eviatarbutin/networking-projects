#@author Eviatar Butin

import socket
from scapy.all import *

serv = socket.socket()
serv.bind(("0.0.0.0",6969))
serv.listen(1)
client_soc, client_add = serv.accept()
time_request = IP(dst="192.114.62.250")/UDP(dport=123)/NTP()
while True:
    request = client_soc.recv(2048)
    if(request.decode() == "TIME"):
        answer = sr1(time_request)
        client_soc.send(str(answer[NTPHeader].sent).encode())
    else:
        client_soc.send("GoodBye".encode())
        break

client_soc.close()
serv.close()


def conver_sec_to_time(secs):
    date = secs/60/60/24/365 + "years"
    return date