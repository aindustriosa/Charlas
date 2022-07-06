//https://github.com/JosefKrieglstein/AxpertControl/blob/master/axpert.py
String QPIGS = "\x51\x50\x49\x47\x53\xB7\xA9\x0D"; //Lecture live data
String QPIWS = "\x51\x50\x49\x57\x53\xB4\xDA\x0D";  
String QDI = "\x51\x44\x49\x71\x1B\x0D";
String QMOD = "\x51\x4D\x4F\x44\x49\xC1\x0D"; 
String QVFW =  "\x51\x56\x46\x57\x62\x99\x0D"; 
String QVFW2 = "\x51\x56\x46\x57\x32\xC3\xF5\x0D"; 

String POP02 = "\x50\x4F\x50\x30\x32\xE2\x0B\x0D";  //SBU priority
String POP01 = "\x50\x4F\x50\x30\x32\xE2\xD2\x69";  //solar first
String POP00 = "\x50\x4F\x50\x30\x30\xC2\x48\x0D";  //utility first

//QPIGS  Lecture live data
float PIP_Grid_Voltage=0;
float PIP_Grid_frequence=0;
float PIP_output_Voltage=0;
float PIP_output_frequence=0;
int PIP_output_apparent_power=0;
int PIP_output_active_power=0;
int PIP_output_load_percent=0;
int PIP_BUS_voltage=0;
float PIP_Battery_voltage=0;
float PIP_battery_charge_current=0;
float PIP_battery_capacity=0;
float PIP_Inverter_heat_sink_temperature =0;
float PIP_PV_current=0;
float PIP_PV_voltage=0;
float PIP_Battery_voltage_from_SCC =0;
float PIP_battery_discharge_current=0;
int PIP_status;

unsigned long lastMillis=0;
long previousMillis = 0;
long interval = 5000;

void setup() {
  Serial.begin(115200);
  Serial2.begin(2400);
}
                              
void loop() {
unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > interval) {  
    previousMillis = currentMillis;    
    //----------------------------------------------------------------------------------------
    Serial2.print(QPIGS);    
    if (Serial2.find("(")) {
        Serial.println("DATA-----------------------------------------"); 
        
        PIP_Grid_Voltage=Serial2.parseFloat();
        PIP_Grid_frequence=Serial2.parseFloat();
        PIP_output_Voltage=Serial2.parseFloat();
        PIP_output_frequence=Serial2.parseFloat();
        PIP_output_apparent_power=Serial2.parseInt();
        PIP_output_active_power=Serial2.parseInt();
        PIP_output_load_percent=Serial2.parseInt();
        PIP_BUS_voltage=Serial2.parseFloat();
        PIP_Battery_voltage=Serial2.parseFloat();
        PIP_battery_charge_current=Serial2.parseFloat();
        PIP_battery_capacity=Serial2.parseInt();
        PIP_Inverter_heat_sink_temperature =Serial2.parseInt();
        PIP_PV_current=Serial2.parseFloat();
        PIP_PV_voltage=Serial2.parseFloat();
        PIP_Battery_voltage_from_SCC =Serial2.parseFloat();
        PIP_battery_discharge_current=Serial2.parseFloat();
        PIP_status=Serial2.parseInt();
      
        Serial.println("Grid voltage: " + String(PIP_Grid_Voltage));        //QPIGS.1 Grid voltage      
        Serial.println("Grid frequency: " + String(PIP_Grid_frequence));        //QPIGS.2 Grid frequency
        Serial.println("Out voltage: " + String(PIP_output_Voltage));       //QPIGS.3 Out voltage  
        Serial.println("Out frequency: " + String(PIP_output_frequence));       //QPIGS.4 Out frequency
        Serial.println("output apparent power: " + String(PIP_output_apparent_power));     //QPIGS.5 AC output apparent power
        Serial.println("output active power: " + String(PIP_output_active_power));      //QPIGS.6 AC output active power
        Serial.println("Output load percent:  " + String(PIP_output_load_percent));   //QPIGS.7 Output load percent 
        Serial.println("PIP_BUS_voltage: " + String(PIP_BUS_voltage));                             //skip
        Serial.println("Battery voltage: " + String(PIP_Battery_voltage));    //QPIGS.9 Battery voltage 
        Serial.println("Battery charging current: " + String(PIP_battery_charge_current));     //QPIGS.10 Battery charging current
        Serial.println("Battery capacity: " + String(PIP_battery_capacity)); //QPIGS.11 Battery capacity 
        Serial.println("PIP_Inverter_heat_sink_temperature: " + String(PIP_Inverter_heat_sink_temperature));                             //skip
        Serial.println("PIP_PV_current: " + String(PIP_PV_current));                             //skip
        Serial.println("PV Input voltage:  " + String(PIP_PV_voltage));     //QPIGS.14 PV Input voltage 
        Serial.println("PIP_Battery_voltage_from_SCC: " + String(PIP_Battery_voltage_from_SCC));                             //skip
        Serial.println("Battery discharge current: " + String(PIP_battery_discharge_current));    //QPIGS.16 Battery discharge current
        Serial.println("PIP_status: " + String(PIP_status));    //QPIGS.17 PIP_status
  

     }else{
      Serial.println(".");
     }
  }
}
