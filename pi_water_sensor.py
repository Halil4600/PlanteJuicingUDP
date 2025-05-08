pi_water_sensor.py

from socket import *
import explorerhat
import time

serverName = '255.255.255.255'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

DRY_VALUE = 0.05  
WET_VALUE = 3.2     

def get_water_percentage(raw_value):
    raw_value = max(min(raw_value, WET_VALUE), DRY_VALUE)
    percent = 100 * (raw_value - DRY_VALUE) / (WET_VALUE - DRY_VALUE)
    return round(percent, 1)

print("Måler og sender vandniveau som UDP broadcast hvert 30. sekund...")

try:
    while True:
        raw = explorerhat.analog.one.read()
        percent = get_water_percentage(raw)
        message = f"waterLevel:{percent}%;raw:{raw:.2f}"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print("Sendt:", message)
        time.sleep(30)

except KeyboardInterrupt:
    print("Afslutter...")
    clientSocket.close()
