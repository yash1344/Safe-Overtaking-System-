# Team_3554-CodeUnnati-Innovation-Marathon
This is the repository of Team_3554 of Innovation Marathon of CodeUnnati Foundation supported by SAP India. 
Project Title is "Title: Safe Overtaking System: A Networked Camera Solution for Improved Road Safety".


============================    Follow procedures to operate system  ============================

Pre requisite:
    Libraries to be Installed: 
        RPi.GPIO
        Socket
        OpenCV
        Pickle
        Struct
        Time
    
    Wi-fi Hotspot module must be available

Step 1: Hotspot should be ON in server side Raspberry PI.

Step 2: Wi-fi should be connected in client side Raspberry PI to server side.

Step 3: Run Server.py into Raspberry PI which must be configured with Camera.

Step 4: Run Client.py into Raspberry PI which must be configured with Ultra Sonic Sensor & Display.

=======================================================================================================+++++++

Hex_coded_RF_transmission

This folder consists of file called "Hex_coded_data_conversion_methods.py" which has methods to convert data into custom binary and vice versa.
"interrupt_trans.py" & "interrupt_rec.py" files are programmed to transmit and receive data through RF communication.

Here we have used 433MHz RF module for radio communication.
