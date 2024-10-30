#### **1\. Control Device**

* **Endpoint**: **`/control-device`**  
* **Method**: POST  
* **Description**: Gửi lệnh điều khiển đến thiết bị thông qua MQTT.  
  * **Input (JSON):**

{

   "device": "device\_name",

   "action": "on/off"

}

* **Output (JSON):**

* **Thành công:**

  {

    "message": "Successfully sent device\_action to device\_name"

  }

* **Lỗi:**

  {

    "message": "Error: error\_message"

  }

#### **2\. Get Data (Latest Sensor Data)**

* **Endpoint: `/get_data`**  
* **Method: GET**  
* **Description:** Lấy dữ liệu mới nhất từ bảng `datass` bao gồm nhiệt độ, độ ẩm, ánh sáng, và ngày giờ.  
  * **Output (JSON):**

	{

 	 "temperature": 25.5,

 	 "humidity": 60,

  	"light": 300,

 	 "date": "dd/mm/yyyy"

	}

#### **3\. Get Data for Chart**

* **Endpoint: `/get_data1`**  
* **Method:** GET  
* **Description:** Lấy dữ liệu nhiệt độ, độ ẩm, ánh sáng từ bảng `datass` để hiển thị trong biểu đồ.  
  * **Output (JSON Array):**

\[

  { "temperature": 25.5, "humidity": 60, "light": 300 },

  { "temperature": 24.0, "humidity": 55, "light": 280 }

\]

#### **4\. Search Devices**

* **Endpoint: `/get_data3`**  
* **Method:** GET  
* **Description:** Tìm kiếm dữ liệu thiết bị dựa trên các tùy chọn và từ khóa tìm kiếm.  
  * **Parameters:**  
    * **`query`:** Từ khóa tìm kiếm (string).  
    * **`option`:** Trường để tìm kiếm, như `device, action` hoặc `timestamp` (string).  
    * **`page`:** Số trang kết quả (integer).  
  * **Output (JSON):**

	{

 	 "data": \[

 	   { "id": 1, "device": "Lamp", "actions": "on", "times": "timestamp" }

  	\],

  	"total\_pages": 5,

 	 "current\_page": 1

	}

#### **5\. Get Sensor Data with Pagination**

* **Endpoint: `/get_data2`**  
* **Method:** GET  
* **Description:** Lấy dữ liệu cảm biến từ bảng `datass` với phân trang.  
  * **Parameters:**  
    * **`query`:** Từ khóa tìm kiếm (string).  
    * **`option`:** Trường để tìm kiếm, như `temperature, humidity, light` hoặc `timestamp` (string).  
    * **`page`:** Số trang kết quả (integer).  
  * **Output (JSON):**

	{

 	 "data": \[

 	   { "id": 1, "temperature": 25.5, "humidity": 60, "light": 300, "times": "timestamp" }

 	 \],

 	 "total\_pages": 10,

 	 "current\_page": 1

	}

#### **6\. Control LED**

* **Topic:** **`control`**  
* **Description:** Nhận các lệnh từ MQTT broker để điều khiển trạng thái của đèn LED và các thiết bị khác.

#### **7\. Save Sensor Data**

* **Function: `save_data_to_datass`**  
* **Description:** Lưu dữ liệu cảm biến (nhiệt độ, độ ẩm, ánh sáng) vào bảng `datass`.  
  * **Parameters:**  
    * **`temperature`:** Nhiệt độ (float)  
    * **`humidity`:** Độ ẩm (float)  
    * **`light`:** Độ sáng (integer)

#### **8\. Save Device State**

* **Function: `save_data_to_devices`**  
* **Description:** Lưu trạng thái bật/tắt của các thiết bị vào bảng `devices`.  
  * **Parameters:**  
    * **`device`:** Tên thiết bị (string, ví dụ: `Lamp`, `Fan`)  
    * **`actions`:** Hành động (string, `on` hoặc `off`)

