import mfrc522
from machine import Pin,SPI
import urequests
import boot
from time import localtime,sleep

buz = Pin(15, Pin.OUT)

def do_post(uid,devId,timestamp):
    
    url = "http://usmgmt.iviscloud.net:777/RfIds/addRFidData_1_0"

    payload='rfModuleId={}&rfTagId={}&DateTime={}'.format(devId,uid,timestamp)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    req = urequests.request("POST", url, headers=headers, data=payload)
    
    print(req.text)

def create_datetime():
    timestring = [str(t) for t in localtime()[:6]]
    return '-'.join(timestring[:3]) + ' ' + ':'.join(timestring[3:])


def do_write():
    spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
    spi.init()
    rdr = mfrc522.MFRC522(spi=spi, gpioRst=4, gpioCs=5)
    print("")
    print("Place card before reader to write address 0x08")
    print("")
    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                buz.value(1)
                Pin(13,Pin.OUT).value(1)
                sleep(0.1)
                buz.value(0)
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                timestamp = create_datetime()
                print(timestamp)
                print(card_id)
                
                do_post(card_id,boot.devId,timestamp)
        else:
            Pin(13,Pin.OUT).value(0)


    
    
do_write()




