import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

temp_min = 15
temp_max = 21

def detect_anomaly(data):
    selected_features = ['Radiation', 'Temperature',
                         'Humidity', 'WindDirection(Degrees)', 'Speed']
    selected_data = [data[feature] for feature in selected_features]

    with open('data_and_weights/scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    data_scaled = scaler.transform([selected_data])
    with open('data_and_weights/isolation_forest_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    prediction = model.predict(data_scaled)
    if prediction[0] == 1:
        return 1
    else:
        return 0
    
def check_rainfall(message):
    water_depth_threshold = 5
    temperature_threshold = 2
    moisture_threshold = 5
    soil_moisture_threshold = 10

    air_temperature = message['Temperature']
    air_moisture = message['Humidity']
    water_depth = message['WaterDepth']
    soil_moisture = message['SoilMoisture']

    if (water_depth > water_depth_threshold) and \
       (air_temperature < temperature_threshold) and \
       (air_moisture > moisture_threshold) and \
       (soil_moisture > soil_moisture_threshold):
        return 1
    else:
        return 0


def ph_warning(message):
    ph_min = 5.5
    ph_max = 6.5
    ph = message['SoilPH']

    ph_warning = 0

    if ph < ph_min:
        ph_warning = -1
    elif ph > ph_max:
        ph_warning = 1

    return ph_warning


def temperature_warning(message):
    temp_min = 25
    temp_max = 35
    temp = message['Temperature']

    temp_warning = 0

    if temp < temp_min:
        temp_warning = -1
    elif temp > temp_max:
        temp_warning = 1

    return temp_warning



