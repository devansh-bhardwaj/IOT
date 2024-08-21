import mysql.connector


def send_sensor_data(data):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="b_devansh",
            password="sql1234",
            database="iot"
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO sensor_data (Temperature, Humidity, WaterDepth, SoilMoisture, SoilPH, Radiation, Speed, TimeStamp, WindDirectionDegrees, DeviceID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['Temperature'], data['Humidity'], data['WaterDepth'], data['SoilMoisture'], data['SoilPH'], data['Radiation'], data['Speed'], data['TimeStamp'], data['WindDirection(Degrees)'], data['DeviceID'])
        mycursor.execute(sql, values)
        mydb.commit()

        print("Sensor data successfully sent to the database!")

    except mysql.connector.Error as error:
        print(f"Error sending sensor data: {error}")

    finally:
        mycursor.close()
        mydb.close()