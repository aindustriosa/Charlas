import serial
import time
import paho.mqtt.client as paho
import json


class Inverter:
    def __init__(self, serialport):

        self.ser = serial.Serial()
        self.ser.port = serialport
        self.ser.baudrate = 2400
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout = 1  # non-block read
        self.ser.xonxoff = False  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2  # timeout for write

        try:
            self.ser.open()
            print("Conexion")
        except Exception as e:
            print("Error opening serial port: " + str(e))
            exit()

        if self.ser.isOpen():
            try:
                self.ser.flushInput()  # flush input buffer, discarding all its contents
                self.ser.flushOutput()  # flush output buffer, aborting current output
                # and discard all that is in buffer
            except Exception as e1:
                # print ("error communicating...: " )
                print("error communicating...: " + str(e1))
        else:
            print("cannot open serial port ")

    def QueryCMD(self, CMD):
        try:
            self.ser.write(CMD)
            time.sleep(1)  # give the serial port sometime to receive the data
            return str(self.ser.readline())
        except Exception as e:
            print(e)

    def chargePercent(self,val):
        #20=0, 24=10, 25.76=20, 26,24=50, 26,48=80, 27,68=95, 29.2=100
        #Las pendiente de la recta las he calculado en excel con datos de biblia
        
        if(val <25.76): #Menor de 20% devuelvo 0
            return 0
        elif(val >=25.76 and val <=26.48):
            return 83.333 * (val-25.76) + 20
        elif(val >26.48 and val <=29.2):
            return 7.353* (val-26.48) + 80
        else:
            return 100

    def ParseQPIGS(self):
        response = self.QueryCMD(b'\x51\x50\x49\x47\x53\xB7\xA9\x0D')
        all = str.split(response)
        #grid_voltage = float(all[0])
        #grid_frequency = float(all[1])
        #ac_output_voltage = float(all[2])
        #ac_output_frequency = float(all[3])
        #ac_output_apparent_power = int(all[4])
        ac_output_active_power = int(all[5])
        output_load_percent = int(all[6])
        #bus_voltage = float(all[7])
        battery_voltage = float(all[8])
        battery_charging_current = int(all[9])
        #battery_capacity = int(all[10])
        heatsink_temperature = int(all[11])
        pv_current = float(all[12])
        pv_voltage = float(all[13])
        battery_voltage_scc = float(all[14])
        battery_discharge_current = int(all[15])
        pv_power = int(all[19])
        #line_power = ac_output_active_power - pv_power

        data = {"ac_output_active_power": ac_output_active_power,
                "output_load_percent": output_load_percent,
                "pv_current": pv_current,
                "pv_voltage": pv_voltage,
                "pv_power": pv_power,
                "battery_charging_current": battery_charging_current,
                "battery_capacity": self.chargePercent(battery_voltage),
                "battery_voltage": battery_voltage,
                "battery_voltage_scc": battery_voltage_scc,
                "battery_discharge_current": battery_discharge_current
                }
        print(data)
        return data


# -------------------MQTT----------------------
broker = "192.168.1.110"
port = 1883

# def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
#    print("subscribed with qos",granted_qos, "\n")
#    pass
# def on_message(client, userdata, message):
#     print("message received  "  ,str(message.payload.decode("utf-8")))
# def on_publish(client,userdata,mid):   #create function for callback
#    print("data published mid=",mid, "\n")
#    pass


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: ")
    client.subscribe(sub_topic)


client = paho.Client("Axpert")  # create client object
print("created")

# client.on_subscribe = on_subscribe
# client.on_publish = on_publish
# client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.username_pw_set("s1", "Todobi77.")
client.connect(broker, port)  # establish connection

print("-------------Connected--------")


# -------------------------MAIN-------------------
AxpertVMIII = Inverter("/dev/ttyS1")

while True:
    data = AxpertVMIII.ParseQPIGS()
    client.publish("heserral/voltronic", json.dumps(data))
    time.sleep(3)

'''


[Unit]
Description=Axpert RS232
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /opt/VOLTRONIC/rs232_voltronic.py

[Install]
WantedBy=multi-user.target

--------------------------------------------------

sudo systemctl daemon-reload
sudo systemctl start axpert.service
sudo systemctl tatus axpert.service
sudo systemctl enable axpert.service

'''
