from socket import *
import requests

# Din API-endpoint
API_URL = "https://plantejuicing-a9hfcaf3fhgccdgw.canadacentral-01.azurewebsites.net/"

# Setup UDP
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("Serveren modtager og sender videre til REST API...")

try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        decoded = message.decode()
        print("Modtaget:", decoded)

        try:
            # Eksempel: "moisture:74.3%;raw:3.21"
            parts = decoded.split(";")
            moisture = float(parts[0].split(":")[1].replace("%", ""))
            raw = float(parts[1].split(":")[1])

            # Send til REST API som JSON
            payload = {
                "moisture": moisture,
                "raw": raw
            }

            response = requests.post(API_URL, json=payload)
            print(f"→ POST status: {response.status_code}")

        except Exception as e:
            print("❌ Fejl i parsing eller POST:", e)

except KeyboardInterrupt:
    print("Stopper server...")
    serverSocket.close()
