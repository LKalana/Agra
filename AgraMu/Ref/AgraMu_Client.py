"""
PROGRAM : AGRAMU CLIENT
AUTHOR  : LIYANAGE KALANA PERERA
DATE    : 2023.12.28 --> 20:14 PM


NOTE_ :- NODEHEAT CLIENT ACT AS THE CLIENT SIDE FOR THE NODEHEAT SERVER.
         SIMPLY RUN THE SCRIPT AND REMEMBER TO CHANGE THE IP ADDRESS ON LINE 19.
         ALSO THIS PROGRAM WILL CREATE A HEATMAP ACCORDING TO THE SERVER DATA.

         THIS SCRIPT WILL READ DATA FROM SERVER SIDE AND THEN STORE IT IN A FILE. BECAUSE THE
         REQUEST IS IN TEXT FORMAT. THEREFORE STORE THE DATA IN TXT FILE AND THEN CONVERT THEM 
         INTO FLOAT AND STORE THEM IN AN ARRAY. THEN PLOT IN HEATMAP.
"""

import requests # INSTALL THIS MODULE USING PIP INSTALL REQUESTS.
import time

#-------------------------------------------------------------------- INITIALIZING PART.
theRequest = None
line = 0
#-------------------------------------------------------------------- CALIBRATION DELAY PART.
print("AGRA MICRO UTILITY SYSTEM")
for count in range(5):
  a = '*' 
  print(a)
#-------------------------------------------------------------------- RECIEVING DATA PART.
# AMOUNT OF DATA TO BE RECIEVED.
while (1):
  for count in range(1):
   # YOU CAN GET THE ESP8266 IP ADDRESS AFTER UPLOADING THE ESP8266 SERVER SCKETCH TO THE 
   # BOARD AND RUN SERIAL MONITOR.
   theRequest = requests.get('http://192.168.1.156/ClientHello')
   print(theRequest.text)
   time.sleep(2)