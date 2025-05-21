pi_temp_Client.py

from socket import *
import explorerhat
import time

serverName = '255.255.255.255'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

def read_temperature_from_analog2():
    while True:
        voltage = explorerhat.analog.two.read()
        temperature_c = int((voltage - 0.5) * 100)  # Convert to integer
        message = f"Temp{temperature_c}"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(f"Sent: {message}")
        time.sleep(30)  # Send data every 30 seconds

try:
    print("Reading temperature from Analog 2 on Explorer HAT and sending as UDP broadcast...")
    read_temperature_from_analog2()

except KeyboardInterrupt:
    print("\nStopped by user.")
    clientSocket.close()

except Exception as e:
    print(f"An error occurred: {e}")
