try:
    import usocket as socket
except:
    import socket
from machine import Pin
from network import WLAN,STA_IF
import esp
from time import sleep
esp.osdebug(None)
import gc
gc.collect()
import ubinascii
from websocket import get_connect
try:
    station = WLAN(STA_IF)
    led=Pin(2,Pin.OUT)
    led_blink=Pin(12,Pin.OUT)
    if station.isconnected():
        print(station.ifconfig())
        wlan_mac = station.config('mac')
        devId = ubinascii.hexlify(wlan_mac).decode()
        print(devId)
        led.value(1)
        led_blink.value(1)
        print("Already connected")
    else:
        with open('wifi.conf') as f:
            creds = f.readlines()
        cred= creds[0].split(':')
        station.active(True)
        station.connect(cred[0], cred[1])
        for _ in range(20):
            if not station.isconnected():
                led.value(1)
                led_blink.value(1)
                sleep(0.3)
                led.value(0)
                led_blink.value(0)
                print('connecting...')
                sleep(0.3)
            else:
                print("Connection successful")
                print(station.ifconfig())
                wlan_mac = station.config('mac')
                print(ubinascii.hexlify(wlan_mac).decode())
                led.value(1)
                led_blink.value(1)
                break
        if not station.isconnected():
            led.value(0)
            led_blink.value(0)
            print("WLAN is not connetinggg...Give credentials to connect WiFi")
            get_connect()
            
except Exception as e:
    print(e)
    get_connect()
    



