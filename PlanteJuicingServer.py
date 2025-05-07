from socket import *
import requests
import json  # Tilføj import for json

# Din API-endpoint
API_URL = "https://plantejuicingrest20250506131910.azurewebsites.net/api/SoilMoisture"

# Setup UDP-server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("✅ Serveren er klar til at modtage og sende til REST API...")

try:
    while True:
        # Modtag besked fra klient
        message, clientAddress = serverSocket.recvfrom(2048)
        decoded = message.decode().strip()
        print("📥 Modtaget:", decoded)

        # Forventet format: "moisture:74.3%;raw:3.21"
        if decoded.startswith("moisture:") and ";" in decoded:
            try:
                # Parse data
                parts = decoded.split(";")
                moisture = float(parts[0].split(":")[1].replace("%", "").strip())
                raw = float(parts[1].split(":")[1].strip())

                # Forbered payload
                payload = {
                    "id": 1,  # ID kan være dynamisk eller fast, afhængig af din API
                    "soilMoistureValue": round(moisture),  # Runder værdien til nærmeste heltal
                }

                # Konverter payload til JSON-streng med dobbelt anførselstegn
                json_payload = json.dumps(payload)

                # Send data til API
                response = requests.post(API_URL, data=json_payload, headers={"Content-Type": "application/json"})
                print(f"📤 Payload sendt: {json_payload}")
                print(f"📥 API-svar: Statuskode {response.status_code}, Indhold: {response.text}")

            except (ValueError, IndexError) as e:
                print(f"❌ Fejl ved parsing af data: {e}")
            except requests.RequestException as e:
                print(f"❌ Fejl ved kommunikation med API: {e}")
        else:
            print("⚠️ Modtaget data i forkert format, ignoreret.")

except KeyboardInterrupt:
    print("🛑 Serveren stoppes...")
    serverSocket.close()
