#include <WiFi.h>
#include <PubSubClient.h>
#include <ESPmDNS.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <HX711.h>

//Net Setup
#define NET_SSID "YOUR_SSID_HERE"
#define NET_PASSWORD "YOUR_PASSWORD_HERE"

//MQTT Setup
#define MQTT_ID "YOUR_MQTT_ID_HERE"
#define MQTT_BROKER "YOUR_MQTT_BROKER_HERE"
#define MQTT_PORT 69420
#define MQTT_DIST_TOPIC "dist_topic"
#define MQTT_PESO_TOPIC "weight_topic"
#define MQTT_VELZ_TOPIC "velocity_topic"

#define VELOCIDADE_DO_SOM 0.034
#define CM_PARA_POLEGADA 0.393701

WiFiClient espClient; //Cliente de rede
PubSubClient MQTT(espClient); //Cliente MQTT

Adafruit_MPU6050 mpu;
HX711 scale;

const int trigPin = 5;
const int echoPin = 18; //definir a velocidade do som em cm/uS

const int DT_PIN = 19;
const int SCK_PIN = 23;

char dist_str[10] = "";
char z_str[10] = "";
char peso_str[10] = "";
long duracao;
float distancCm;
float distancInch;

void setupWifi() {
//Configura a conexão à rede sem fio
 if (WiFi.status() == WL_CONNECTED)
 return;
 Serial.println();
 Serial.print("Connecting to " );
 Serial.println(NET_SSID);
 WiFi.begin(NET_SSID, NET_PASSWORD );
while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
}
 Serial.println("");
 Serial.println("WiFi connected" );
 Serial.println("IP address: " );
 Serial.println(WiFi.localIP());
}

void setupMQTT() {
 MQTT.setServer(MQTT_BROKER, MQTT_PORT );//informa qual broker e porta deve ser conectado

 while (!MQTT.connected())
 {
 Serial. print("*Tentando se conectar ao Broker MQTT: " );
 Serial. println(MQTT_BROKER);
 if (MQTT.connect(MQTT_ID))
 {
 Serial. println("Conectado com sucesso ao broker MQTT!" );
 }
 else
 {
 Serial.println("Falha ao reconectar no broker.");
 Serial. println("Havera nova tentativa de conexao em 2s" );
 delay (2000);
 }
 }
}

void setup(void) {

//Configura o baudrate da comunicação serial
  Serial.begin(115200);
  setupWifi();
  setupMQTT();

  scale.begin(DT_PIN, SCK_PIN);
  scale.set_scale(-10000.00);
  scale.tare();

  pinMode(trigPin, OUTPUT); // Define o trigPin como uma saída
  pinMode(echoPin, INPUT); // Define o echoPin como uma entrada

  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);
}

void loop() {
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2); // Define o trigPin no estado ALTO por 10 microssegundos
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW); // Lê o echoPin, retorna o tempo de viagem da onda sonora em microssegundos

  duracao = pulseIn(echoPin, HIGH); // Calcule a distância

  distancCm = duracao * VELOCIDADE_DO_SOM / 2; // Converter para centimetros
  distancInch = distancCm * CM_PARA_POLEGADA;  // Converter para polegadas

  Serial.print("Distancia (cm): "); // Imprime a distância no Serial Monitor
  Serial.println(distancCm);

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  sprintf(dist_str, "%f", distancCm);
  MQTT.publish(MQTT_DIST_TOPIC, dist_str);

  sprintf(z_str, "%f", a.acceleration.z);
  MQTT.publish(MQTT_VELZ_TOPIC, z_str);

  sprintf(peso_str, "%f", scale.get_units(10));
  MQTT.publish(MQTT_PESO_TOPIC, peso_str);

  setupWifi();
  setupMQTT();
  delay(2000);

}
