Đo nhiệt độ, độ ẩm, ánh sáng bằng ESP8266
Mô tả dự án
Dự án này sử dụng ESP8266 để đo nhiệt độ, độ ẩm và cường độ ánh sáng, sau đó gửi dữ liệu lên một trang web để hiển thị theo thời gian thực. Thiết bị cảm biến kết nối với ESP8266 sẽ liên tục thu thập dữ liệu và cập nhật lên giao diện người dùng thông qua một máy chủ web đơn giản.
Thành phần sử dụng
* ESP8266: giao tiếp với cảm biến và đưa dữ liệu lên cơ sở dữ liệu.
* Cảm biến nhiệt độ (DHT11): Đo nhiệt độ và độ ẩm.
* Cảm biến ánh sáng: Đo cường độ ánh sáng.
* Điện trở.
* Dây kết nối.
* Nguồn cấp: 5V hoặc 3.3V từ cổng USB hoặc pin.
* Giao diện web: hiển thị các dữ liệu từ cảm biến.
Phần mềm
* Arduino IDE: lập trình và nạp code cho ESP8266.
* Thư viện: thư viện cho DHT, ESP8266.
* Visual studio code: lập trình giao diện web.
Kết nối mạch
* Cảm biến nhiệt độ:
* Chân VCC nối với 3.3V.
* Chân GND nối với GND.
* Chân Data nối với chân D1 của ESP8266.
* Cảm biến ánh sáng:
* Chân VCC nối với 3.3V.
* Chân GND nối với GND.
* Chân A0 nối với chân A0 của ESP8266.
Cài đặt
1. Cài đặt Arduino IDE và thêm board ESP8266.
2. Cài đặt các thư viện cần thiết: DHT Sensor Library, Adafruit Sensor Library, ESP8266WiFi, ESP8266WebServer.
3. Kết nối ESP8266 với máy tính qua cổng USB, chọn board ESP8266.
4. Nạp code cho ESP8266.
Cấu hình WIFI và MQTT
        Cấu hình lại Wifi cho phù hợp.
                const char* ssid = "Tên WiFi";
				const char* password = "Mật Khẩu WiFi";
				const char* mqtt_server = "Địa chỉ IP";
        Thay đổi user, password và port.
Hiển thị dữ liệu trên web
1. Ghi dữ liệu được gửi từ ESP vào database: sử dụng code để ghi dữ liệu (getdata.py).
2. Giao diện web:
* Cấu trúc thư mục mẫu:
/project_folder│
├── /static
│ ├── folder (ảnh, icon,...)
│ ├── chart.js
│ └── style.css
├── /templates
│   ├── page1.html
│   ├── page2.html
│   ├── main.html
│   └── …
└── get_data.py
* Khởi chạy file code get_data.py để cập nhật dữ liệu trang web liên tục. Sau khi chạy, mở địa chỉ có trong terminal để mở giao diện trang web.