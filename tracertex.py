from scapy.all import *
import re


url = input("please enter url or ip address")

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
    if responce[ICMP].type == 0:
        # achieved destination
        print(str(ttl) + " - last hop ->\t " + responce[IP].src)
        break
    elif responce[ICMP].type == 11:
        if responce[ICMP].code == 0:
            # ttl expired
            print(str(ttl) + " - hop ->\t" + responce[IP].src)
            ttl += 1
        else:
            error_number += 1
            print(str(ttl) + " - ERROR ->\tFragment reassembly time exceeded")
            continue
    elif responce[ICMP].type == 3:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tDestination Unreachable\t",end="")
        if responce[ICMP].code == 0:
            print("Destination network unreachable")
        elif responce[ICMP].code == 1:
            print("Destination host unreachable")
        elif responce[ICMP].code == 2:
            print("Destination protocol unreachable")
        elif responce[ICMP].code == 3:
            print("Destination port unreachable")
        elif responce[ICMP].code == 4:
            print("Fragmentation required, and DF flag set")
        elif responce[ICMP].code == 5:
            print("Source route failed")
        elif responce[ICMP].code == 6:
            print("Destination network unknown")
        elif responce[ICMP].code == 7:
            print("Destination host unknown")
        elif responce[ICMP].code == 8:
            print("Source host isolated")
        elif responce[ICMP].code == 9:
            print("Network administratively prohibited")
        elif responce[ICMP].code == 10:
            print("Host administratively prohibited")
        elif responce[ICMP].code == 11:
            print("Network unreachable for ToS")
        elif responce[ICMP].code == 12:    
            print("Host unreachable for ToS")
        elif responce[ICMP].code == 13:    
            print("Communication administratively prohibited")
        elif responce[ICMP].code == 14:    
            print("Host Precedence Violation")
        elif responce[ICMP].code == 15:    
            print("Precedence cutoff in effect")
        else:
            print(" ")
    elif responce[ICMP].type == 5:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tRedirect Message\t",end="")
        if responce[ICMP].code == 0:
            print("Redirect Datagram for the Network")
        elif responce[ICMP].code == 1:
            print("Redirect Datagram for the Host")
        elif responce[ICMP].code == 2:
            print("Redirect Datagram for the ToS & network")
        elif responce[ICMP].code == 3:
            print("Redirect Datagram for the ToS & host")
        else:
            print(" ")
    elif responce[ICMP].type == 9:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tRouter Advertisement")
    elif responce[ICMP].type == 10:
        error_number += 1
        print(str(ttl) +" - ERROR ->\tRouter discovery/selection/solicitation")
    elif responce[ICMP].type == 12:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tParameter Problem: Bad IP header\t",end="")
        if responce[ICMP].code == 0:
            print("Pointer indicates the error")
        elif responce[ICMP].code == 1:
            print("Missing a required option")
        elif responce[ICMP].code == 2:
            print("Bad length")
        else:
            print("")
    elif responce[ICMP].type == 13:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tTimestamp")

    elif responce[ICMP].type == 14:
        error_number += 1
        print(str(ttl) + " - ERROR ->\tTimestamp Reply")
    else:
        error_number += 1
        continue
    
print("trace complete")
