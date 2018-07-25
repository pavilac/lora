# loraWAN
Raspbian code for sending packets with different data rates using the Microchips development kit 900.

Start.py must be set as a startup code in the Raspberry Pi. This code waits for an external button to be pushed to activate lm.py and lm2.py.


lm.py Send 10 packets turning on a LED while is sending, with data rate 0.


lm2.py Send 10 packets turning on a LED while is sending, with data rate 3.


Decoder.py Decode LoRaWAN packets captured with Wireshark, using LoRaWAN 1.0.x packet decoder and saves them in a .csv file
