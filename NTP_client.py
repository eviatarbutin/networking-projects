#@author Eviatar Butin

import socket
from datetime import datetime

my_soc = socket.socket()
my_soc.connect(("127.0.0.1",6969))
want_to_know_time = True
while(want_to_know_time):
    print("If you want to know the time press enter! =)")
    my_soc.send("TIME".encode())
    date = my_soc.recv(2048)
    print(datetime.fromtimestamp(float(date.decode())-70*365*24*60*60).strftime("%A, %B %d, %Y %I:%M:%S"))
    print("If you want to exit enter \"bye\"")
    want_to_know_time = input() != "bye" 
my_soc.close()
print("GoodBye")