from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("Serveren er klar til at modtage data...")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print("Modtaget fra Raspberry Pi:", message.decode())

    