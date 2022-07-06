#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include <ArduinoJson.h>
#include <SoftwareSerial.h>

#include "PZEM004Tv30.h"


//-------------------WEMOS D1 R1------------------



void setup_wifi();

DynamicJsonDocument doc(1024);

const char* ssid = "";
const char* password = "";

long lastTime = 0;

//RX, TX
SoftwareSerial pzemSWSerial(12, 13);
PZEM004Tv30 pzem(pzemSWSerial);
WiFiClient client;
HTTPClient http;

String serverURL = "http://192.168.1.111/pzem";

void setup() {
  Serial.begin(115200);
  //pzem.resetEnergy();
  setup_wifi();
  ArduinoOTA.begin();

}

void loop() {
  ArduinoOTA.handle();

  long now = millis();
  if (now - lastTime > 2000) {

    if ((WiFi.status() != WL_CONNECTED)) {
      Serial.println("Reconnecting to WiFi...");
      WiFi.disconnect();
      WiFi.reconnect();
    }

    lastTime = now;

    // Print the custom address of the PZEM
    //Serial.print("Custom Address:");
    //Serial.println(pzem.readAddress(), HEX);

    // Read the data from the sensor
    float voltage = pzem.voltage();
    float current = pzem.current();
    float power = pzem.power();
    float energy = pzem.energy();
    float frequency = pzem.frequency();
    float pf = pzem.pf();

    // Check if the data is valid
    if (isnan(voltage)) {
      Serial.println("{\"err\":\"Error reading voltage\"}");
    } else if (isnan(current)) {
      Serial.println("{\"err\":\"Error reading current\"}");
    } else if (isnan(power)) {
      Serial.println("{\"err\":\"Error reading power\"}");
    } else if (isnan(energy)) {
      Serial.println("{\"err\":\"Error reading energy\"}");
    } else if (isnan(frequency)) {
      Serial.println("{\"err\":\"Error reading frequency\"}");
    } else if (isnan(pf)) {
      Serial.println("{\"err\":\"Error reading power factor\"}");
    } else {

      /*
        Serial.print("Voltage: ");      Serial.print(voltage);      Serial.println("V");
        Serial.print("Current: ");      Serial.print(current);      Serial.println("A");
        Serial.print("Power: ");        Serial.print(power);        Serial.println("W");
        Serial.print("Energy: ");       Serial.print(energy,3);     Serial.println("kWh");
        Serial.print("Frequency: ");    Serial.print(frequency, 1); Serial.println("Hz");
        Serial.print("PF: ");           Serial.println(pf);
      */

      doc["V"] = voltage;
      doc["A"] = current;
      doc["W"] = power;
      doc["kWh"] = energy;
      doc["Hz"] = frequency;
      doc["Pf"] = pf;

      String out = "";
      serializeJson(doc, out);

      http.begin(client, serverURL);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String httpRequestData = "data=" + out;
      Serial.println(httpRequestData);
      Serial.println(http.POST(httpRequestData));
    }
  }
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

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
