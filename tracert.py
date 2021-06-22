from scapy.all import *
import re


url = input("please enter url or ip address: ")

ip = "^\d+\.\d+\.\d+\.\d+$"
valid_ip = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"

if re.match(ip, url):
    if re.match(valid_ip, url):
        pass
    else:
        print("invalid ip address")
        exit()
else:
    # url
    # I could've given the url to scapy but we don't need their help
    dns_answer = sr1(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=url)), verbose=0)
    if DNSRR not in dns_answer:
        print("Bad url")
        exit()
    url = dns_answer[DNSRR].rdata

ttl = 1
error_number = 0

while ttl <= 30 and error_number < 10:
    packet = IP(ttl=ttl, dst=url)/ICMP()/Raw(load='abcdefghijklmnopqrstuvwabcdefghi')
    responce = sr1(packet, verbose=0)
    packet.show()
    if responce[ICMP].type == 0:
        # achieved destination
        print(str(ttl) + " - last hop ->\t" + responce[IP].src)
        break
    elif responce[ICMP].type == 11:
        if responce[ICMP].code == 0:
            # ttl expired
            print(str(ttl) + " - hop ->\t\t" + responce[IP].src)
            ttl += 1
    else:
        print("error number " + str(error_number))
        error_number += 1
        continue

print("trace complete")
