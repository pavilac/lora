#!/usr/bin/python
"""
Python Code for Sending Data from the RN2903 Mote
for Microchip LoRaMOTE USA Version
Created by; Pablo E. Avila C - Ucuenca
"""

import serial
import time
import sys
import RPi.GPIO as GPIO
LedPin = 11    # pin11


BAUD_RATE = 57600

class LoRaSerial(object):
    def __init__(self,_serial_port):
        '''
            configures serial connection
        '''
        self._ser = serial.Serial(_serial_port, BAUD_RATE)

        # timeout block read
        self._ser.timeout = 8

        # disable software flow control
        self._ser.xonxoff = False

        # disable hardware (RTS/CTS) flow control
        self._ser.rtscts = False

        # disable hardware (DSR/DTR) flow control
        self._ser.dsrdtr = False

        # timeout for write
        self._ser.writeTimeout = 0

        #print "Resetting LoRa Tranceiver..."
        self.write_command('sys reset',False)
        #print "Configuring Tranceiver..."
        #Mac Configuration
        self.write_command('mac set devaddr 001AD314')
        self.write_command('mac set appskey 3C8F262739BFE3B7BC0826991AD0504D')
        self.write_command('mac set nwkskey 2B7E151628AED2A6ABF7158809CF4F3C')
        self.write_command('mac set adr off')
        self.write_command('mac set sync 34')
        self.write_command('mac set pwridx 5')
        self.write_command('mac set dr 3')
        self.write_command('mac save')


        # Configure sub-bands
        for ch in range(0,63):
          self.write_command('mac set ch status %d %s'%(ch,
            'on' if ch in range(0,7) else 'off'))

        # join the network
        #print "Attempting to Join Network..."
        self.write_command('mac join abp')
        response = self.read()
        if response == 'accepted':
          print "LoRa Tranceiver Configured. Joined (ABP)"
        else:
          print "ERROR: mac join returned unexpected response: ", response



    def read(self):
        '''
            reads serial input
        '''
        return self._ser.readline().strip()

    def write(self, str):
        '''
            writes out string to serial connection, returns response
        '''
        self._ser.write(str + '\r\n')
        return self.read()
    
    def write_command(self, config_str, check_resp=True):
        '''
            writes out a command
        '''
        #print "Command: '%s'"%config_str
        response = self.write(config_str)
        if check_resp and response != 'ok':
          print "Command: '%s'"%config_str
          print "Response: '%s'"%response
        
    def send_message(self, data):
        '''
            sends a message to gateway
        '''
        # print "Sending message... "
        # send packet (returns 'ok' immediately)
        self.write_command('mac tx uncnf 5 %s'%data)
        # wait for success message
        response = self.read()
        if response == 'mac_tx_ok':
          print "Message sent successfully!"
        else:
          print "ERROR: mac tx command returned unexpected response: ", response 

    def receive_message(self):
        '''
            waits for a message
        '''
        pass


if __name__ == "__main__":

  port = '/dev/ttyACM0'
  packets = 10
  #Configure indicator LED  
  GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
  GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
  #Configure Module
  loramote = LoRaSerial(port)
  #Send Data
  GPIO.output(LedPin, GPIO.HIGH)
  for i in range(1,packets+1):
      loramote.send_message(i)
      time.sleep(1)
  GPIO.output(LedPin, GPIO.LOW)
  GPIO.cleanup()

