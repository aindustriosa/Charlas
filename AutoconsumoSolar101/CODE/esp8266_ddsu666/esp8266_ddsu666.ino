//https://arduino.stackexchange.com/questions/88542/convert-from-raw-data-to-float-from-ddsu666-h

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoOTA.h>
#include <ModbusMaster.h>

#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include <ArduinoJson.h>

DynamicJsonDocument doc(1024);

long lastTime = 0;

const char* ssid = "";
const char* password = "";
//IPAddress local_IP(192, 168, 1, 111);
//IPAddress gateway(192, 168, 1, 1);
//IPAddress subnet(255, 255, 255, 0);

WiFiClient client;
HTTPClient http;

String serverURL = "http://192.168.1.111/pzem";

//RX, TX
SoftwareSerial SWSerial(12, 13);

#define MAX485_DE      14
#define MAX485_RE_NEG  16

ModbusMaster node;

void preTransmission()
{
  digitalWrite(MAX485_RE_NEG, 1);
  digitalWrite(MAX485_DE, 1);
}

void postTransmission()
{
  digitalWrite(MAX485_RE_NEG, 0);
  digitalWrite(MAX485_DE, 0);
}

void setup() {
   pinMode(MAX485_RE_NEG, OUTPUT);
   pinMode(MAX485_DE, OUTPUT);
   // Init in receive mode
   digitalWrite(MAX485_RE_NEG, 0);
   digitalWrite(MAX485_DE, 0);

  
   Serial.begin(9600);
   SWSerial.begin(9600); //AXPERT SERIAL COMS

    WiFi.mode(WIFI_STA);
    //WiFi.config(local_IP, gateway, subnet);
    WiFi.begin(ssid, password);

    // Wait for connection
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    ArduinoOTA.begin();

    // Modbus slave ID 1
    node.begin(1, SWSerial);
    // Callbacks allow us to configure the RS485 transceiver correctly
    node.preTransmission(preTransmission);
    node.postTransmission(postTransmission);
  
    
}

void loop() {
  long now = millis();
  if (now - lastTime > 2000) {
    uint8_t i, result;
    uint16_t data[2];
    union
    {
      uint32_t j;
      float f;
    } u;
  
    Serial.println("-----------------------");
    result = node.readHoldingRegisters(0x2004, 2);
    if (result == node.ku8MBSuccess)
    {
      for (i = 0; i < 2; i++)
      {
        data[i] = node.getResponseBuffer(i);
      }
      //Serial.println(data[0]); MSU
      //Serial.println(data[1]); LSU
      u.j = ((unsigned long)data[0] << 16 | data[1]);
      //-1000 pk el valor viene en Kw 
      //Enchufé el ddsu al reves y me da valores en negativo
      //así que multimplico +-1 para pasarlo a positivo

      doc["V"] = 0.0;
      doc["A"] = 0.0;
      doc["W"] = float(u.f)*-1000;
      doc["kWh"] = 0.0;
      doc["Hz"] = 0.0;
      doc["Pf"] = 0.0;

      String out = "";
      serializeJson(doc, out);

      http.begin(client, serverURL);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String httpRequestData = "data=" + out;
      Serial.println(httpRequestData);
      Serial.println(http.POST(httpRequestData));
      
    }
  }else{
     if ((WiFi.status() != WL_CONNECTED)) {
      Serial.println("Reconnecting to WiFi...");
      WiFi.disconnect();
      WiFi.reconnect();
    }
  }

  ArduinoOTA.handle();
  
}
