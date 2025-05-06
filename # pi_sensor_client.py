# pi_sensor_client.py
from socket import *
import explorerhat
import time

# Server (din computer) IP og port
serverName = '255.255.255.255'     # ← Broadcaster
serverPort = 12000

# Opret UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Kalibrering (juster efter behov)
DRY_VALUE = 3.0
WET_VALUE = 0.5

def get_moisture_percentage(raw_value):
    raw_value = max(min(raw_value, DRY_VALUE), WET_VALUE)
    percentage = 100 * (DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE)
    return round(percentage, 1)

print("Måler og sender data til server hvert minut...")

try:
    while True:
        raw_value = explorerhat.analog.one.read()
        moisture = get_moisture_percentage(raw_value)

        message = f"moisture:{moisture}%;raw:{raw_value:.2f}"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(f"Sendt: {message}")
        time.sleep(60)  # Vent 1 minut

except KeyboardInterrupt:
    print("Afslutter...")
    clientSocket.close()
