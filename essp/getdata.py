import paho.mqtt.client as mqtt
import mysql.connector
import json

# Cấu hình kết nối tới MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",   # thay bằng user MySQL
    password="123456",  # thay bằng mật khẩu MySQL
    database="demo"   # thay bằng tên database
)

cursor = db.cursor()

# Hàm lưu dữ liệu vào bảng 'datass'
def save_data_to_datass(temperature, humidity, light, AQI):
    try:
        sql = "INSERT INTO datass (temperature, humidity, AQI, light) VALUES (%s, %s, %s, %s)"
        values = (temperature, humidity, AQI, light)
        cursor.execute(sql, values)
        db.commit()
        print(f"Data saved to datass: Temp={temperature}, Hum={humidity}, Light={light}, AQI={AQI}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Hàm lưu trạng thái LED vào bảng 'devices'
def save_data_to_devices(led, ledact):
    try:
        sql = "INSERT INTO devices (device, actions) VALUES (%s, %s)"
        values = (led, ledact)
        cursor.execute(sql, values)
        db.commit()
        print(f"Data saved to devices: device={led}, actions={ledact}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Hàm lưu trạng thái cả 3 LED cùng một lúc vào bảng 'devices'
def save_data(check):
    ledact = "on" if check == 1 else "off"
    
    # Lưu trạng thái từng LED
    for led in ["led1", "led2", "led3"]:
        try:
            sql = "INSERT INTO devices (device, actions) VALUES (%s, %s)"
            values = (led, ledact)
            cursor.execute(sql, values)
            db.commit()
            print(f"Data saved to devices: device={led}, actions={ledact}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

# Hàm callback khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message from topic `{topic}`: {payload}")

    if topic == "data":
        try:
            # Nhận dữ liệu cảm biến từ ESP8266 và lưu vào bảng 'datass'
            received_data = msg.payload.decode()
            # Tách chuỗi và lấy các giá trị
            data_parts = received_data.split(', ')
            temperature = None
            humidity = None
            light = None

            for part in data_parts:
                key, value = part.split(': ')
                if key == 'Temperature':
                    temperature = float(value.replace(' C', '').strip())  
                elif key == 'Humility':
                    humidity = float(value.replace('%', '').strip())  
                elif key == 'Light':
                    light = int(value.replace(' Lux', '').strip())
                elif key == 'AQI':
                    AQI = int(value.replace('', '').strip())      

            # Lưu dữ liệu vào bảng 'datass'
            save_data_to_datass(temperature, humidity, light, AQI)

        except Exception as e:
            print(f"Error processing data message: {e}")

    elif topic == "control":
        # Kiểm tra trạng thái LED nhận được và lưu vào bảng 'devices'
        if payload == "led1_on":
            save_data_to_devices("Lamp", "on")
        elif payload == "led1_off":
            save_data_to_devices("Lamp", "off")
        elif payload == "led2_on":
            save_data_to_devices("Fan", "on")
        elif payload == "led2_off":
            save_data_to_devices("Fan", "off")
        elif payload == "ledw_off":
            save_data_to_devices("WARNING", "off")
        elif payload == "ledw_on":
            save_data_to_devices("WARNING", "on")
        elif payload == "led_on":
            save_data(1)
        elif payload == "led_off":
            save_data(0)

# Hàm callback khi kết nối tới MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe("data")  # Subscribe vào topic 'data' cho dữ liệu cảm biến
        client.subscribe("control")  # Subscribe vào topic 'control' cho trạng thái LED
    else:
        print(f"Failed to connect, return code {rc}")

# Cấu hình MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set("jul", "123")  # Thêm username và password

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Kết nối tới MQTT broker
mqtt_client.connect("172.20.10.3", 1999, 60)

# Chạy vòng lặp chính để lắng nghe dữ liệu từ broker
mqtt_client.loop_forever()
