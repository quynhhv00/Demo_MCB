from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Cấu hình MQTT client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set("jul", "123")
mqtt_client.connect("172.20.10.3", 1999, 60)  


# Kết nối tới cơ sở dữ liệu MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="demo"
    )
    return connection


# Route để nhận yêu cầu điều khiển từ giao diện
@app.route('/control-device', methods=['POST'])
def control_device():
    try:
        data = request.get_json()
        device = data['device']
        action = data['action']

        # Gửi lệnh điều khiển tới MQTT broker
        topic = "control"
        message = f"{device}_{action}"
        mqtt_client.publish(topic, message)

        return jsonify({'message': f'Successfully sent {message} to {device}'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# API để trả về dữ liệu JSON
@app.route('/get_data')
def get_data():
    conn = get_db_connection()  # Thêm kết nối ở đây
    cursor = conn.cursor()

    cursor.execute("SELECT temperature, humidity, light, DATE_FORMAT(Tgian, '%d/%m/%Y') AS formatted_date FROM datass ORDER BY Tgian DESC LIMIT 1")
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    data = {
        'temperature': row[0],
        'humidity': row[1],
        'light': row[2],
        'date': row[3]
    }
    
    return jsonify(data)

# Lấy thông số cảm biến và timestamp từ database
@app.route('/control')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Lấy dữ liệu cảm biến
    cursor.execute('SELECT temperature, humidity, light, Tgian FROM datass ORDER BY Tgian DESC LIMIT 1')
    sensor_data = cursor.fetchone()
    
    # Đóng kết nối
    cursor.close()
    conn.close()
    
    # Chuyển đổi timestamp thành định dạng ngày tháng năm
    if sensor_data and sensor_data['Tgian']:
        if isinstance(sensor_data['Tgian'], datetime):
            timestamp = int(sensor_data['Tgian'].timestamp())
        else:
            timestamp = int(sensor_data['Tgian'])

        formatted_date = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
    else:
        formatted_date = "Không có dữ liệu"

    return render_template('mainpro.html', sensor_data=sensor_data, date=formatted_date)

#Lấy dữ liệu vào data
@app.route('/get_data2')
def get_data2():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, temperature, humidity, light, DATE_FORMAT(Tgian, '%Y-%m-%d %H:%i:%s') AS formatted_date FROM datass ORDER BY Tgian DESC LIMIT 20")
    row = cursor.fetchall()
    return jsonify(row)


@app.route('/data')
def index_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, temperature, humidity, light, Tgian FROM datass ORDER BY Tgian DESC LIMIT 20")
    row = cursor.fetchall()
    return render_template('data.html', data=row)

#Lấy dữ liệu vào biểu đồ
@app.route('/get_data1')
def get_data1():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT temperature, humidity, light FROM datass ORDER BY Tgian DESC LIMIT 10")
    rows = cursor.fetchall()
    # for item in rows:
    #     item['light'] = item['light'] / 10  # Chia giá trị ánh sáng cho 10
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.route('/chart')
def index_chart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT temperature, humidity, light, Tgian FROM datass ORDER BY Tgian DESC LIMIT 1')
    sensor_data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if sensor_data and sensor_data['Tgian']:
        if isinstance(sensor_data['Tgian'], datetime):
            timestamp = int(sensor_data['Tgian'].timestamp())
        else:
            timestamp = int(sensor_data['Tgian'])

        formatted_date = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
    else:
        formatted_date = "Không có dữ liệu"

    return render_template('chart.html', sensor_data=sensor_data, date=formatted_date)

@app.route('/get_data3')
def get_data3():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, device, actions, DATE_FORMAT(Tgian, '%Y-%m-%d %H:%i:%s') AS formatted_date FROM devices ORDER BY Tgian DESC LIMIT 20")
    row = cursor.fetchall()
    return jsonify(row)

@app.route('/info')
def index_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, device, actions, Tgian FROM devices ORDER BY Tgian DESC LIMIT 20")
    row = cursor.fetchall()
    return render_template('info.html', data=row)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
