#pip3 install pyusb pyserial crcmod OPi.GPIO influxdb

#https://github.com/JosefKrieglstein/AxpertControl/blob/master/axpert.py

import os
import serial, time, sys, string
import usb.core
import usb.util
import re
import crcmod
from binascii import unhexlify, hexlify
import paho.mqtt.client as paho
import time
#import ssl
import json

import OPi.GPIO as GPIO


connection = "USB"

try:
    usb0 = os.open('/dev/hidraw0', os.O_RDWR | os.O_NONBLOCK)

except Exception as e:
    print ("error open USB port: " + str(e))
    exit()


def serial_command(command,device):
    try:
        response = ""
        xmodem_crc_func = crcmod.predefined.mkCrcFun('xmodem')
	    # wierd mistake in Axpert firmware - correct CRC is: 0xE2 0x0A
        # if command == "POP02": 
        #     #POP02
        #     command_crc = '\x50\x4f\x50\x30\x32\xe2\x0b\x0d\r'
        # else: 
        #     #QPGS0
        #     #command_crc = '\x51\x50\x47\x53\x30\x3f\xda\r'.encode()
        command_crc = (command.encode() + unhexlify(hex(xmodem_crc_func(command.encode())).replace('0x','',1)) )+ '\r'.encode()

        if len (command_crc) < 9:
            time.sleep (0.35)
            os.write(device, command_crc)
         
        else:
            cmd1 = command_crc[:8]
            cmd2 = command_crc[8:]
            time.sleep (0.35)
            os.write(device, cmd1)
            time.sleep (0.35)
            os.write(device, cmd2)
            time.sleep (0.25)
        while True:
            try:
                time.sleep (0.15)
                r = os.read(device, 256)
                r=r.decode(errors="ignore")
                response +=r
                if '\r' in r: break
            except Exception as e:
                print(e)

    except Exception as e:
        print ("error reading inverter...: " + str(e) + "Response :" + response)
        data = ""

    return response


def get_data(command,inverter):
    device = usb0
    try:
        response = serial_command(command,device)
        if "NAKss" in response or response == '':
            return ''
        else:
  
            response_num = re.sub ('[^0-9. ]','',response)

            if command == "QPIGS":
                response.rstrip()
                response_num.rstrip()
                nums = response_num.split(' ', 99)
                print(nums)

                data={
                        "measurement": "voltronic_data",
                        "tags": {
                            "host": "voltronic",
                        },
                        "fields": {
                            "AC_grid_voltage":float(nums[0]),
                            "AC_grid_frequency":float(nums[1]),
                            "AC_out_voltage": float(nums[2]),
                            "AC_out_frequency":float(nums[3]),
                            "Wa_out":float(nums[4]),
                            "W_out":float(nums[5]),
                            "Work_percent":float(nums[6]),
                            "PV_in_watts":float(nums[19]),
                            "Battery_voltage":float(nums[8]),
                            "Battery_discharge_current":float(nums[12]),
                            "Battery_charge_current":float(nums[9]),
                            "Battery_capacity":float(nums[10]),
                            "Heatsink_temperature":float(nums[11]),
                            "PV_in_voltage":float(nums[13]),
                            "Load_status":int(nums[16][3:4]),
                            "Battery_status":int(nums[16][4:6]),
                            "Inv_direction":int(nums[16][6:7]),
                            "Line_direction":int(nums[16][7:])
                        }
                }

                client.publish("heserral/voltronic",json.dumps(data))
                print(data)

#nums[16] = 00010000 [x,x,x,load_status,b1,b2,inv_direction,line_detection]
#b2b1: 00: Do nothing,01: Charging,10: Discharging
#Line direction 00 means unsteady 01 means Line input 10 means Line output



    except Exception as e:
        print ("error parsing inverter data...: " + str(e))
	    #print ("problem command: " + command +": " + response)


broker="192.168.1.110"
port = 1883
sub_topic='#'

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   pass
def on_message(client, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))
def on_publish(client,userdata,mid):   #create function for callback
   print("data published mid=",mid, "\n")
   pass
def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
 
def on_connect(client, userdata, flags, rc):
   print("Connection returned result: ")
   client.subscribe(sub_topic)

client= paho.Client("PyJerbas")       #create client object
print("created")

client.on_subscribe = on_subscribe       #assign function to callback
client.on_publish = on_publish        #assign function to callback
client.on_message = on_message        #assign function to callback
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.username_pw_set("s1", "Todobi77.")
client.connect(broker,port)           #establish connection

print("-------------Connected--------")


if __name__ == '__main__':
#    client.loop_start()
#    while 1:
     data = get_data('QPIGS', 0)
     time.sleep(1)

#crontab -e
#* * * * * python3 /root/vm3.py


#QPIRI      Device Rating Information inquiry 
#QPIGS      Device general status parameters inquiry 
#QMOD       Device Mode inquiry
#QPIWS      Device Warning Status inquiry
#QT         Time inquiry
#QTYYMMDDHHMM y derivados
#QDI        The default setting value information


#   "Inverter_mode":2,
#   "AC_grid_voltage":244.6,
#   "AC_grid_frequency":49.9,
#   "AC_out_voltage":0.0,
#   "AC_out_frequency":0.0,
#   "PV_in_voltage":0.0,
#   "PV_in_current":0.0,
#   "PV_in_watts":0.0,
#   "PV_in_watthour":0.0000,
#   "SCC_voltage":0.0000,
#   "Load_pct":0,
#   "Load_watt":0,
#   "Load_watthour":0.0000,
#   "Load_va":0,
#   "Bus_voltage":421,
#   "Heatsink_temperature":37,
#   "Battery_capacity":100,
#   "Battery_voltage":57.30,
#   "Battery_charge_current":0,
#   "Battery_discharge_current":0,
#   "Load_status_on":0,
#   "SCC_charge_on":0,
#   "AC_charge_on":1,
#   "Battery_recharge_voltage":49.0,
#   "Battery_under_voltage":46.2,
#   "Battery_bulk_voltage":57.4,
#   "Battery_float_voltage":57.3,
#   "Max_grid_charge_current":60,
#   "Max_charge_current":60,
#   "Out_source_priority":2,
#   "Charger_source_priority":1,
#   "Battery_redischarge_voltage":2479072725932077545527213289373696.0,
#   "Warnings":"00000000000000000000000000000000"
