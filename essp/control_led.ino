#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DPIN 4        // GPIO ket noi cam bien DHT (D2)
#define DTYPE DHT11 

DHT dht(DPIN, DTYPE);

// Cau hinh cam bien
#define ANALOG_INPUT_PIN A0  // Chan analog (A0 tren ESP8266)
#define DIGITAL_INPUT_PIN 5  // Chan digital (D1 tren ESP8266 tuong ung voi GPIO5)


#define D5 14
#define D6 12


// Update these with values suitable for your network.

const char* ssid = "Tooj";
const char* password = "5lopvaoviec";
const char* mqtt_server = "172.20.10.3";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(100)
char msg[MSG_BUFFER_SIZE];



void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];

  }
  Serial.println(message);


  if (message == "led1_off") {
    digitalWrite(D5, LOW);   // Tắt LED1
  } else if (message == "led1_on") {
    digitalWrite(D5, HIGH);  // Bật LED1
  } else if (message == "led2_off") {
    digitalWrite(D6, LOW);   // Tắt LED2
  } else if (message == "led2_on") {
    digitalWrite(D6, HIGH);  // Bật LED2
  } else if (message == "led_off") {
    digitalWrite(D5, LOW);
    digitalWrite(D6, LOW);// Tắt tất cả các LED
  } else if (message == "led_on") {
    digitalWrite(D5, HIGH);
    digitalWrite(D6, HIGH);// Bật tất cả các LED
  }


}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(),"jul","123")) {
      Serial.println("connected");
      client.subscribe("control");

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);  // Khoi tao chan LED
  pinMode(D5, OUTPUT); //led1
  pinMode(D6, OUTPUT); //led2
  pinMode(DIGITAL_INPUT_PIN, INPUT);  // digital
  
  dht.begin();

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1999);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;
  
    // Doc du lieu tu cam bien DHT
    float temp = dht.readTemperature(false);  // Doc nhiet do (°C)
    float humi = dht.readHumidity();          // Doc do am

    // Doc gia tri tu cac chan     analog va digital
    int analogValue = analogRead(ANALOG_INPUT_PIN); // Doc gia tri tu chan A0 (cam bien anh sang)
    int digitalValue = digitalRead(DIGITAL_INPUT_PIN); // Doc gia tri tu GPIO5 (chan digital)

    // Kiem tra loi doc cam bien DHT
    if (isnan(temp) || isnan(humi)) {
      Serial.println("Failed to read from DHT sensor!");
    }else{
        //temperature  //humidity
     snprintf(msg, MSG_BUFFER_SIZE, "Temperature: %.2f C, Humility: %.0f%%, Light: %d Lux", temp, humi, analogValue);
    }

    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("data", msg);
    delay(50);
  }
}
