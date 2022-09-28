Installation procedure of ESP32

Requirements:

Nodemcu
Mfrc522
Card readers/tags
Jumper wires
Bread board
Power cable
Buzzer
Small Led lights



Install the thonny using below link: 
    https://thonny.org/
Then click on windows, download latest version

![thonney](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/thonney.png?raw=true)

After that download firmware file to configure the thonny using micropython(ESP32) with nodemcu.

To download micropython firmware file use link:
                        https://micropython.org/download/esp32/
Select the latest version of firmware file

![firmware](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/firmware.png?raw=true)


Open Tools  in thonny click on options then click on interpreter then choose  MicroPython(ESP32) .

![module](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/module.png?raw=true)


Here we have only COM1 port ,but we don’t want it
![port](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/port.png?raw=true)
 have to select the port Silicon Labs CP210x USB to UART Bridge (COM3). 
Here we can get any port like COM4…COM8 etc 
On the above picture only COM1 port is available
If we don't have the Silicon labs port ,go to start menu and open device manager.
Click on ports  to check whether the port is available or not.
If the Silicon port is not available, Connect the nodemcu device to cpu
On device manager other device option will display.click on the other device 
It shows device name like CP2102 USB-to-Serial Bridge Driver

Click on the below link to install Driver
           https://www.usb-drivers.org/cp2102-usb-to-uart-bridge-driver.html
After opening this link ,scroll down and click on  
          CP2102 USB-to-Serial Bridge Driver - windows option for download                                                   
After completion of downloading the Driver, Double click on the downloaded zip file
Select Wizard option ,select the destination where we want to extract the file ,click on finish
Double click on the  extracted file 
Double click on CP210xVCPInstaller_x64
Click on install option,click on close
Open device manager
Select port,here the new port is available 

Open thonny,click on tools, select options 
Click on interpreter
Select micropython(ESP32)
Select the port which we added in port (Silicon Labs com3)
Click on install or update micropython 
Here again select Silicon Labs COM3 port and  Browse the firmware file (esp8266-1m-20220618-v1.19.1.bin)  along with path to install the micropython(in the starting  we gave link to download the firmware file)
Select erase flash before installing
Click on Install button

![firmware_upgrade](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/firmware_upgrade.png?raw=true)



 After that Clone the below program files boot.py,     main.py,   mfrc522.py,   websocket.py    
Click the below link it shows code, copy the code and paste in the notepad save the code with name boot.py
boot.py file:

https://gist.githubusercontent.com/vdattu/818aaded9577d11fbffbe2659c1fef48/raw/e72969156fc6daef03aaf279886bd4a84f871266/ESP_32_boot.py 

Click on the below link it shows code, copy and paste the code in notepad ,save the code with name main.py



main.py file :

https://gist.githubusercontent.com/vdattu/298a5aa759b42d03c457971af83a31af/raw/25619d8739f070c9bf414b93af333eaa34c34e9b/ESP_32_main.py 


wifi.conf file:

proxy@!v!s_2.4GHz !v!s@proxy 

Click on the below link it shows code, copy and paste the code in notepad ,save the code with name mfrc522.py

mfrc522.py file:

https://gist.githubusercontent.com/vdattu/e579cd35683b042829bf023c820d5500/raw/b4b4e6d8ad2a1cc435b3cc6543a9bf6af8ab30bb/esp32_mfrc522.py

Click on the below link it shows code, copy and paste the code in notepad ,save the code with name websocket.py

websocket.py file:

https://gist.githubusercontent.com/vdattu/45a2ef4ece49213f3e8f7ff231a31a77/raw/7df6f1405b6b069f3b65d82c1a23b19dbd0997f1/ESP_32_websocket.py 

Open thonny IDE to run program file
IN Thonny click on Files then click on open ,  open the files which file we extract from zip for micropython programming files


![program](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/program.png?raw=true)

First time when we connect the nodemcu device to cpu,if the device connects to wifi, on nodemcu the led light will turn on only for 10 to15 sec
If the device doesn't connect to wifi ,the led light will not turn on and the light blinks on and off.
To connect the wifi,turn on your wifi connection and connect to AP_ESP32 with password:1234567890
Now we connected to wifi ,”connected but no internet”
Now open the web page with the ip 192.168.4.1 and it shows available networks 
Select your wifi network and enter credentials  
It will take some time to connect to device
Reboot the device
Connect the nodemcu  device again ,now the led light  should be turn on the device
Now the device connected to network
The passive RFID  card tag frequency range must be 125KHz to 13.56 MHz 
Then scan the card on the mfrc522 device
The device data will store on the database 
By calling an API we can get the device data from database








Connect the nodemcu device to 12v charger adapter
On the device the led light must be blink for 10 to 15 sec
Later the led light will off  because the device did  not connect to the  internet
Wait for 10 sec ,later open wifi on your mobile
Connect to AP_ESP32 with password 1234567890
If the device connected to wifi(AP_ESP32) it shows the message  “connected, no internet”
Open chrome/web browser on your mobile
Enter the ip 192.168.4.1 and wait for 5-10 sec 
It will take some time to connect to device
It shows available Access points(networks) with security type shown as in below image

![access_page](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/access_page.png?raw=true)


Select your access point ,enter password click on submit
Now your device connected to internet

![success_page](https://github.com/ChVeerababu/MFRC522_ESP32/blob/main/success_page.png?raw=true)

Reboot the device
Connect the nodemcu  device again ,now the blue light  should be turn on the device
Now the led light blinks on the device continuously that means the device connected to network
Scan the tag/card on mfrc522 device
When we scan the tag/card,the green light should be blink on the device and the device plays  buzzer sound
The device data and tag data will store in database
By calling an API we will get all the data
 





