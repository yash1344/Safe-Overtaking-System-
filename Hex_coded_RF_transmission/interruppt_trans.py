import RPi.GPIO as GPIO
import signal
import sys
from binascii import hexlify

i = 0
intrpt = 16         #interupt pin
credentials = "<ssid>Yash</ssid><pass>Yash@123</pass><ip>192.168.1.3</ip><port>9999</port>"     #credentials
data = ""           #binery data

pwm_pin = 18        #pwm pin
data_trans_pin = 23     #transmiting pin


#convert data into ASCII HEX
def data2Hex(data):
    temp = data.encode()
    temp = hexlify(temp).decode()

    return temp


#convert ASCII HEX into custom Binery
def hex2bin(hex_data):
    bin_data = ""
    dic = ["z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    for element in hex_data:
        for j in range(dic.index(element)):
            bin_data += "10"
        bin_data += "0000000"

    return bin_data


#to terminate transmission
def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)


#jump here when got interupt
def got_intrpt(channel):
	global i
	GPIO.output(data_trans_pin, int(data[i]))
	print(data[i])
	i += 1
	
	if(i== len(data)):
		i = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin,GPIO.OUT)        #output PWM pin
pwm_sig = GPIO.PWM(pwm_pin, 300)        #set PWM freq

data = hex2bin(data2Hex(credentials))       #convert credentials into custom binery
print(data)

GPIO.setup(data_trans_pin,GPIO.OUT)         #output transmiting pin

GPIO.setup(intrpt, GPIO.IN, pull_up_down = GPIO.PUD_UP)             #set edge trigure
GPIO.add_event_detect(intrpt, GPIO.FALLING, callback = got_intrpt, bouncetime = 2)             #setup for interupt

pwm_sig.start(50)           #sets duty cycle of PWM

signal.signal(signal.SIGINT, signal_handler)            #wait for keyboard press 'CTRL + C'
signal.pause()
