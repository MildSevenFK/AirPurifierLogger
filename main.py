from miio import AirPurifier
import time

ip_address = "192.168.1.141"
token = ""

purifier = AirPurifier(ip_address, token)

while True:
    try:
        status = purifier.status()
        air_quality = status.aqi
        temperature = status.temperature
        humidity = status.humidity

        print("Air Quality: {}  Temperature: {}°C  Humidity: {}%".format(air_quality, temperature, humidity))

    except Exception as e:
        print("Error occurred: ", e)

    time.sleep(3)