
from socket import *
import explorerhat
import time

serverName = '255.255.255.255'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

DRY_VALUE = 1.5 
WET_VALUE = 3.8 

def get_moisture_percentage(raw_value):
    raw_value = max(min(raw_value, WET_VALUE), DRY_VALUE)
    percentage = 100 * (raw_value - DRY_VALUE) / (WET_VALUE - DRY_VALUE)
    return round(percentage, 1)

print("Måler og sender data som UDP broadcast hvert minut...")

try:
    while True:
        raw_value = explorerhat.analog.one.read()
        moisture = get_moisture_percentage(raw_value)

        message = f"moisture:{moisture}%;raw:{raw_value:.2f}"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(f"Sendt: {message}")
        time.sleep(30) 

except KeyboardInterrupt:
    print("Afslutter...")
    clientSocket.close()
