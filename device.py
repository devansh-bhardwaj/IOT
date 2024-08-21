import network
import time
import ubinascii
import random
import machine
import uasyncio as asyncio
from umqtt.simple import MQTTClient
import json
import M5
from M5 import Widgets

SERVER = "0.0.0.0"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
DEVICE_ID = CLIENT_ID.decode("utf-8")
PUBLISH_TOPIC = f"IOT/project/data"
SUBSCRIBE_TOPIC = f"IOT/project/{DEVICE_ID}"

sampling_time = 2000
transmission_time = 4000

# Queue to store data
data_queue = json.loads('[]')

def getInternetTime():
    ntptime.timeout = 30  
    ntptime.settime()
    t = utime.localtime(utime.mktime(utime.localtime()) + 19800)  
    machine.RTC().datetime((t[0], t[1], t[2], 0, t[3], t[4], t[5], 0))

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())
    return wlan

def subscribe_callback(topic, msg):
    M5.Display.clear()
    msg = json.loads(msg)
    print(f"Recieved: {msg}")

    if msg['temp'] == 1:
        Widgets.fillScreen(0xff0000)
        label = Widgets.Label("High Temperature:", 10, 100, 1.3, 0x000000, 0xff0000, Widgets.FONTS.DejaVu12) 
        label.setVisible(True)

    elif msg['temp'] == -1:
        Widgets.fillScreen(0x8b8000)
        label = Widgets.Label("Low Temperature", 10, 100, 1.3, 0x000000, 0x8b8000, Widgets.FONTS.DejaVu12) 
        label.setVisible(True)

    elif msg['ph'] == 1:
        Widgets.fillScreen(0xff0000)
        label = Widgets.Label("High PH Value", 10, 100, 1.3, 0x000000, 0xff0000, Widgets.FONTS.DejaVu12) 
        label.setVisible(True)

    elif msg['ph'] == -1:
        Widgets.fillScreen(0x8b8000)
        label = Widgets.Label("Low PH Value", 10, 100, 1.3, 0x000000, 0x8b8000, Widgets.FONTS.DejaVu12) 
        label.setVisible(True)

    elif msg['anomaly'] == 1:
        Widgets.fillScreen(0x222222)
        label = Widgets.Label("Anomaly Detcted", 10, 100, 1.3, 0xffffff, 0x222222, Widgets.FONTS.DejaVu12) 
        label.setVisible(True)

    if msg['rain'] == 1:
        M5.Speaker.tone(5000, 50)  


async def getSensorData():
    global data_queue
  
    while True:
        T = utime.localtime()
        S = f"{T[3]:02d}:{T[4]:02d}:{T[5]:02d} {T[2]}/{T[1]}/{T[0]}"
        data = {
            "DeviceID": DEVICE_ID,
            "TimeStamp": S,
            "AirTemperature": random.randint(15, 45),
            "AirMoisture": random.randint(70, 80),
            "WaterDepth": random.randint(40, 60),
            "SoilMoisture": random.randint(23, 27),
            "SoilPH": random.randint(3, 4),
            "SolarRadiation": random.randint(180, 220),
            "WindSpeed": random.randint(5, 10),
            "WindDirection": random.randint(0, 360)
        }

        data_dict = '{{"DeviceID": "{}", "TimeStamp": "{}", "Temperature": {}, "Humidity": {}, "WaterDepth": {}, "SoilMoisture": {}, "SoilPH": {}, "Radiation": {}, "Speed": {}, "WindDirection(Degrees)": {}}}'.format(
        data['DeviceID'], data["TimeStamp"], data['AirTemperature'], data['AirMoisture'], data['WaterDepth'], data['SoilMoisture'], data['SoilPH'], data['SolarRadiation'], data['WindSpeed'], data['WindDirection'])
        data_queue.append(data_dict)
        await asyncio.sleep_ms(sampling_time)

async def transmitData(client):
    global data_queue
    while True:
        client.publish(PUBLISH_TOPIC, json.dumps(data_queue))
        data_queue = json.loads('[]')
        await asyncio.sleep_ms(transmission_time)

async def check(client):
    while True:
        client.check_msg()
        await asyncio.sleep_ms(1000)

async def loop(client):
    try:
        
        task1 = asyncio.create_task(getSensorData())
        task2 = asyncio.create_task(transmitData(client))
        task0 = asyncio.create_task(check(client))
      
        await asyncio.gather(task1, task2, task0)
         
  
    except Exception as e:
        print(e)
            

if __name__ == '__main__':
    try:
        wlan = connect_to_wifi('devansh', 'devansh123')
        if SERVER == "0.0.0.0":
            SERVER = wlan.ifconfig()[2]
        client = MQTTClient(CLIENT_ID, SERVER)
        client.connect()
        print("Connected to %s" % SERVER)
    
        client.set_callback(subscribe_callback)
        client.subscribe(SUBSCRIBE_TOPIC)
    
        asyncio.run(loop(client))
    
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("Unable to import utility module")
    finally:
        client.disconnect()
   
