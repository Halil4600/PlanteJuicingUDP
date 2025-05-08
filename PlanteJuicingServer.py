from socket import *
import requests
import json

# Din API-endpoint
API_URLMoisture = "https://plantejuicingrest20250506131910.azurewebsites.net/api/SoilMoisture"
API_URLTemperature = "https://plantejuicingrest20250506131910.azurewebsites.net/api/Temp"
API_URLWaterLevel = "https://plantejuicingrest20250506131910.azurewebsites.net/api/WaterLevel"

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

        # Identificer datatypen og opbyg payload
        if decoded.startswith("moisture:") and ";" in decoded:
            # Håndter jordfugtighedsdata
            try:
                parts = decoded.split(";")
                moisture = float(parts[0].split(":")[1].replace("%", "").strip())
                raw = float(parts[1].split(":")[1].strip())

                payload = {
                    "Id": 1,
                    "SoilMoistureValue": round(moisture)  # Runder til nærmeste heltal
                }

                # Send data til API
                response = requests.post(API_URLMoisture, json=payload, headers={"Content-Type": "application/json"})
                print(f"📤 Payload sendt: {payload}")
                print(f"📥 API-svar: Statuskode {response.status_code}, Indhold: {response.text}")

            except (ValueError, IndexError) as e:
                print(f"❌ Fejl ved parsing af jordfugtighedsdata: {e}")

        elif decoded.startswith("Temp"):
            # Håndter temperaturdata
            try:
                # Hvis beskeden indeholder ";", parse begge værdier
                if ";" in decoded:
                    parts = decoded.split(";")
                    temperature = float(parts[0].split(":")[1].strip())
                    raw = float(parts[1].split(":")[1].strip())
                else:
                    # Hvis beskeden kun indeholder én værdi (f.eks. "Temp3")
                    temperature = float(decoded.split("Temp")[1].strip())
                    raw = None  # Ingen raw-værdi i dette tilfælde

                payload = {
                    "Id": 2,
                    "TempValue": round(temperature),  # Runder til én decimal
                }

                # Send data til API
                response = requests.post(API_URLTemperature, json=payload, headers={"Content-Type": "application/json"})
                print(f"📤 Payload sendt: {payload}")
                print(f"📥 API-svar: Statuskode {response.status_code}, Indhold: {response.text}")

            except (ValueError, IndexError) as e:
                print(f"❌ Fejl ved parsing af temperaturdata: {e}")

        elif decoded.startswith("water:") and ";" in decoded:
            # Håndter lysdata
            try:
                parts = decoded.split(";")
                waterLevel = int(parts[0].split(":")[1].strip())
                raw = float(parts[1].split(":")[1].strip())

                payload = {
                    "id": 3,
                    "WaterLevel": round(waterLevel),  # Runder til nærmeste heltal
                }

                # Send data til API
                response = requests.post(API_URLWaterLevel, json=payload, headers={"Content-Type": "application/json"})
                print(f"📤 Payload sendt: {payload}")
                print(f"📥 API-svar: Statuskode {response.status_code}, Indhold: {response.text}")

            except (ValueError, IndexError) as e:
                print(f"❌ Fejl ved parsing af waterData: {e}")

        else:
            print("⚠️ Modtaget data i ukendt format, ignoreret.")

except KeyboardInterrupt:
    print("🛑 Serveren stoppes...")
    serverSocket.close()
