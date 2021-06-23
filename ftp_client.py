import socket
import sys
import threading
import time

commands = ["quit", "download", "list"]
STARTING_SERVER_TALKING_COMMANDS = 1
IP = "ftp.hp.com"#"ftp.iitb.ac.in"
PACKET_LENGTH = 1024
PORT = 21

SELF_IP = "10.0.0.14" #"79.179.76.174"
OPEN_PORT = 8989
IP_BINDING = "0.0.0.0"

# connect
def login(username: str, password: str, counter: int) -> bool:
	print(str(counter) + " - attempt to login")
	if counter > 10:
		return False

	g_client.send(("USER " + username + "\r\n").encode())
	response = g_client.recv(PACKET_LENGTH).decode()
	response = response.split()[0]
	#print("first " + response)
	if response != "331" and response != "230":
		login(username, password, counter + 1)

	g_client.send(("PASS " + password + "\r\n").encode())
	response = g_client.recv(PACKET_LENGTH).decode()
	response = response.split()[0]
	#print("second " + response)
	if response != "230":
		login(username, password, counter + 1)
	return True

def choose_command() -> str:
	print("What would you like to do?\nPlease choose from the options below and type the number of the option or it's name.")

	while True:
		for command in range(len(commands)):
			print(str(command+1) + ' - ' + commands[command])
		choice = input("Please choose the command by typing it's name or number: ")
		if choice in commands:
			return choice
		else:
			try:
				choice = int(choice) - 1
				if choice < 0:
					raise IndexError
				choice = commands[choice]
				return choice
			except TypeError:
				print("Wrong input try again")
			except IndexError:
				print("The number is not pointing to a command try again")
			except:
				print("Some error happened try again")

def choose_mode() -> str:
	mode = ""
	while mode != "pass" and mode != "act":
		print("Please choose the way of talking with the server.")
		print("You can choose the active mode (in work) or the passive mode (in work)")
		mode = input("Enter pass for passive mode and act for active")
	return mode

def passive_print_stream(server:str, stream:str):
	server = server[server.index('(') + 1:server.index(')')]
	# print(server)
	ip = server.split(',')[0] + "." + server.split(',')[1] + "." + server.split(',')[2] + "." +server.split(',')[3]
	# print(ip)
	# print(server.split(',')[4], server.split(',')[5])
	port = int(server.split(',')[4]) * 256 + int(server.split(',')[5])
	# print(ip, str(port))
	server:socket.socket = socket.socket()
	server.connect((ip,port))
	while(True):
		if stream == "":
			message = server.recv(PACKET_LENGTH).decode()
			if message == "":
				break
			print(message)
		else:
			file_t = open(stream, "a")
			message = server.recv(PACKET_LENGTH).decode()
			if message == "":
				file_t.close()
				break
			print(message, file=file_t)
	server.close()

def active_print_stream(port:str, stream:str):
	server = socket.socket()
	server.bind((IP_BINDING,port))
	server.listen(1)
	data_stream_socket, address = server.accept()

	while(True):
		if stream == "":
			message = data_stream_socket.recv(PACKET_LENGTH).decode()
			if message == "":
				break
			print(message)
		else:
			file_t = open(stream, "a")
			message = data_stream_socket.recv(PACKET_LENGTH).decode()
			if message == "":
				file_t.close()
				break
			print(message, file=file_t)
	
	data_stream_socket.close()
	server.close()

def main():
	global g_client

	g_client = socket.socket()
	g_client.connect((IP, PORT))
	g_client.recv(PACKET_LENGTH)
	print("Connection Established")

	print("enter your username and password for the server")
	username = input("Enter your username: ")
	password = input("Enter your password: ")

	while not login(username, password, 0):
		print("You couldn't connect to the server. Try again")
		username = input("Enter your username: ")
		password = input("Enter your password: ")

	print("You have connected to the server!")
	
	while True:
		command = choose_command()

		if commands.index(command) >= STARTING_SERVER_TALKING_COMMANDS:
			mode = choose_mode()
			if mode == "pass":
				g_client.send(("PASV" + "\r\n").encode())
				serv_details = g_client.recv(1024).decode()
				print(serv_details)
				if command == "list":
					thread = threading.Thread(target=passive_print_stream, args=(serv_details,"",))
					thread.start()
					time.sleep(2)
					g_client.send(("LIST" + "\r\n").encode())
					while thread.is_alive():
						time.sleep(1)
					print(g_client.recv(PACKET_LENGTH).decode())
					print("sent")	
				elif command == "download":
					file_name = input("Enter the file name you want to download: ")
					g_client.send(("RETR " + file_name + "\r\n").encode())
					if g_client.recv(PACKET_LENGTH).decode().split()[0] != 150:
						print("try again")
					else:
						thread = threading.Thread(target=passive_print_stream, args=(serv_details,file_name,))
						thread.start()
						time.sleep(2)
						while thread.is_alive():
							time.sleep(1)
						print(g_client.recv(PACKET_LENGTH).decode())
						print("sent")	
			else:
				# port = get_port()
				ip = "(" + SELF_IP.replace('.',',')
				port = "," + str(OPEN_PORT//256) + "," + str(OPEN_PORT%256) + ")"
				print("IP = " + ip)
				print("port = " + port)
				g_client.send(("PORT " + ip + port + "\r\n").encode())
				if command == "list":
					thread = threading.Thread(target=active_print_stream, args=(OPEN_PORT,"",))
					thread.start()
					time.sleep(2)
					g_client.send(("LIST" + "\r\n").encode())
					while thread.is_alive():
						time.sleep(1)
					print(g_client.recv(PACKET_LENGTH).decode())
					print("sent")	
		else:
			if command == "quit":
				g_client.send(("QUIT" + "\r\n").encode())
				g_client.close()
				break


if __name__ == "__main__":
	main()
