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
    cursor.execute("SELECT  temperature, humidity, light, DATE_FORMAT(Tgian, '%Y-%m-%d %H:%i:%s') AS formatted_date FROM datass ORDER BY Tgian DESC LIMIT 1")
    sensor_data = cursor.fetchone()   
    # Đóng kết nối
    cursor.close()
    conn.close()
    return render_template('mainpro.html', sensor_data=sensor_data)


#Lấy dữ liệu vào biểu đồ
@app.route('/get_data1')
def get_data1():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT temperature, humidity, light FROM datass ORDER BY Tgian DESC LIMIT 10")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.route('/chart')
def index_chart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT  temperature, humidity, light, DATE_FORMAT(Tgian, '%Y-%m-%d %H:%i:%s') AS formatted_date FROM datass ORDER BY Tgian DESC LIMIT 1")
    sensor_data = cursor.fetchone()    
    cursor.close()
    conn.close()
    return render_template('chart.html', sensor_data=sensor_data)

@app.route('/get_data3')
def get_data3():
    search_query = request.args.get('query', '')
    search_option = request.args.get('option', 'device')  
    page = int(request.args.get('page', 1))  
    limit = 20
    offset = (page - 1) * limit  

    conn = get_db_connection()
    cursor = conn.cursor()

    # Truy vấn SQL động theo tùy chọn tìm kiếm
    if search_query:
        if search_option == 'timestamp':
            sql_query = """
                SELECT id, device,actions,times 
                FROM devices 
                WHERE Tgian LIKE %s
                ORDER BY Tgian DESC 
                LIMIT %s OFFSET %s
            """
        else:
            sql_query = f"""
                SELECT id, device,actions,times 
                FROM devices  
                WHERE {search_option} LIKE %s
                ORDER BY Tgian DESC 
                LIMIT %s OFFSET %s
            """
        search_term = f"%{search_query}%"
        cursor.execute(sql_query, (search_term, limit, offset))
    else:
        cursor.execute("""
            SELECT id, device,actions,times 
                FROM devices 
            ORDER BY Tgian DESC 
            LIMIT %s OFFSET %s
        """, (limit, offset))

    rows = cursor.fetchall()

    # Tính tổng số bản ghi để tính số trang
    if search_query:
        if search_option == 'timestamp':
            count_query = "SELECT COUNT(*) FROM devices WHERE Tgian LIKE %s"
        else:
            count_query = f"SELECT COUNT(*) FROM devices WHERE {search_option} LIKE %s"
        cursor.execute(count_query, (search_term,))
    else:
        cursor.execute("SELECT COUNT(*) FROM devices")
    
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + limit - 1) // limit  #tổng số trang

    cursor.close()
    conn.close()

    return jsonify({
        'data': rows,
        'total_pages': total_pages,
        'current_page': page
    })
   
@app.route('/info')
def index_info():
    return render_template('info.html')

#Lấy dữ liệu vào data
@app.route('/data')
def index_data():
    return render_template('data.html')

# API lấy dữ liệu từ MySQL
@app.route('/get_data2')
def get_data2():
    search_query = request.args.get('query', '')
    search_option = request.args.get('option', 'temperature')  
    page = int(request.args.get('page', 1))  
    limit = 20
    offset = (page - 1) * limit  

    conn = get_db_connection()
    cursor = conn.cursor()

    # Truy vấn SQL động theo tùy chọn tìm kiếm
    if search_query:
        if search_option == 'timestamp':
            sql_query = """
                SELECT id, temperature, humidity, light, times 
                FROM datass 
                WHERE Tgian LIKE %s
                ORDER BY Tgian DESC 
                LIMIT %s OFFSET %s
            """
        else:
            sql_query = f"""
                SELECT id, temperature, humidity, light, times 
                FROM datass 
                WHERE {search_option} LIKE %s
                ORDER BY Tgian DESC 
                LIMIT %s OFFSET %s
            """
        search_term = f"%{search_query}%"
        cursor.execute(sql_query, (search_term, limit, offset))
    else:
        cursor.execute("""
            SELECT id, temperature, humidity,  light, times
            FROM datass 
            ORDER BY Tgian DESC 
            LIMIT %s OFFSET %s
        """, (limit, offset))

    rows = cursor.fetchall()

    # Tính tổng số bản ghi để tính số trang
    if search_query:
        if search_option == 'timestamp':
            count_query = "SELECT COUNT(*) FROM datass WHERE Tgian LIKE %s"
        else:
            count_query = f"SELECT COUNT(*) FROM datass WHERE {search_option} LIKE %s"
        cursor.execute(count_query, (search_term,))
    else:
        cursor.execute("SELECT COUNT(*) FROM datass")
    
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + limit - 1) // limit  #tổng số trang

    cursor.close()
    conn.close()

    return jsonify({
        'data': rows,
        'total_pages': total_pages,
        'current_page': page
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
