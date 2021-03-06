#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pydevd


from SIM808 import SIM808

#Raspberry Serial Connection
import serial
from time import sleep
Serial_Port='/dev/ttyS0'
Serial = serial.Serial(port=Serial_Port, baudrate=9600, bytesize=serial.EIGHTBITS, 
               parity=serial.PARITY_NONE, 
               stopbits=serial.STOPBITS_ONE, timeout=10, 
               xonxoff=False, rtscts=False, 
               writeTimeout=None, dsrdtr=True, 
               interCharTimeout=None)


if __name__ == "__main__":
    
    pydevd.settrace("192.168.0.14", port=5678,stdoutToServer=True, stderrToServer=True)
    
    Modem = SIM808.TCP_IP(Serial)
    
    MQTT = SIM808.MQTT(Modem)
    
    try:
        #Open a GRPS Network
        assert Modem.Connect_GPRS()
    except:
        print('Modem Fail')
        exit()                        
        
    try:
        
        #MQTT host and port
        assert Modem.Service_Connect('179.190.169.78','1883')
    except:
        print('TCP Connection Fail')
        exit()  
        
    try:
                
        if MQTT.ping() == False:
            while MQTT.connect("qwertyuiopzzbr", 0, 0, "", "", 1, 0, 0, 0, "", "") == False:
                pass
            
        MQTT.ping()
        
    except:
        print('MQTT Connection Fail')
        
    
    msg_ID=0    
    try:        
        while(True):
            msg_ID = msg_ID + 1
            MQTT.publish(0, 1, 0, msg_ID, "Teste", "Hello "+ str(msg_ID))
            sleep(10)
        
        
        
    except KeyboardInterrupt:
        print "Program finished\n"
        Modem.Close_All()
    
    except:
        Modem.Close_All()
        pass
    
        
