## IOT COURSE PROJECT

The project utilized the MQTT protocol to establish a system in which each IoT node generates data and sends it to a server. The server then analyzes the received data and sends the analysis (based on a secondary dataset) back to the node, which displays warnings on its screen based on the analysis. The data is also added to an SQL database hosted locally on the server. This system can be utilized in **Precision Agricultire** to enable monitoring, maintenance, and automation of farms and farming activities to increase agricultural sustainability. 

For running the system, these steps need to be followed:

1. Start a Mosquitto MQTT message broker.
2. Run the file `device.py` on the ESP32 device after changing the ssid and password of the wifi connection.
```bash
wlan = connect_to_wifi('devansh', 'devansh123')
```
3. The folder named server should be copied the sever which is recieving the data. 
4. Host a MySQL server on the server, and set appropriate host, username, password and database name in the file `sql.py`
```bash
mydb = mysql.connector.connect(
            host="localhost",
            user="b_devansh",
            password="sql1234",
            database="iot"
        )
```
5. Finally, run the file `server.py` on the server.





