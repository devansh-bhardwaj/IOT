import paho.mqtt.client as mqtt
import json
import warnings
warnings.filterwarnings("ignore")

from analysis import detect_anomaly, check_rainfall, ph_warning, temperature_warning
from preprocessing import preprocess
from sql import send_sensor_data

def publish_message(client, topic, message):
    client.publish(topic, json.dumps(message))

def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode())
    message = preprocess(message)
    print(f"Recieved: {message}")

    ## Sending the recieved data to a SQL database 
    send_sensor_data(message)

    ## Performing Analysis on the recieved data
    anomaly = detect_anomaly(message)
    ph_warn = ph_warning(message)
    temp_warn = temperature_warning(message)
    rainfall = check_rainfall(message)

    ## Sending the analysis back to the device
    response = {"anomaly": anomaly, "ph": ph_warn, "temp": temp_warn, "rain": rainfall}
    device = message['DeviceID']
    publish_message(client, f"IOT/project/{device}", response)


def on_connect(client, userdata, flags, rc):
    client.subscribe("IOT/project/data")
 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("192.168.137.1", 1883, 60)

client.loop_forever()


