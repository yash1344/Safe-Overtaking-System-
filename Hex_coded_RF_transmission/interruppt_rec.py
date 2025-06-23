import RPi.GPIO as GPIO
import time
import signal
import sys
import codecs

data = ""       #received binery data
raw_credentials = ""        #raw data
credentials_list = []       #final credentials
i = 0
intrpt = 16                 #interupt pin
pwm_pin = 18                #PWM genrate pin
data_recv_pin = 24          #receive data from RF receiver


#get perticuler tag value
def getvalueof(data, tag):
    if "<"+tag+">" in data:
        temp = data.split("<"+tag+">")[1]
        if "</"+tag+">" in data:
            temp = temp.split("</"+tag+">")[0]
        else:
            temp = "null"
    else:
        temp = "null"
    return temp


#set all credentials
def set_credentials(data):
    ssid1 = getvalueof(data,"ssid")
    password1 = getvalueof(data,"pass")
    ip1 = getvalueof(data,"ip")
    port1 = getvalueof(data,"port")

    return [ssid1,password1,ip1,port1]


#make sures that all credentials are ready or not
def check_credentials(list):
    try:
        list.index("null")
        time.sleep(2)
        print("Checking again")
        check_credentials(set_credentials(raw_credentials))
    except ValueError:
        print("Got The Credentials")
        return list 


#convert binery data into ASCII HEX
def bin2Hex(bin_data):
    hex_data = ""
    temp_data_list = bin_data.split("0000000")
    dic = ["z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    #Clear the Unwanted Data
    for j in range(len(temp_data_list)):
        for i in range(len(temp_data_list[j])):
            if (temp_data_list[j])[i] == "1":
                temp_data_list[j] = (temp_data_list[j])[i:]
                break

    #Convert bin into Hex
    for temp in temp_data_list:
        if temp.count('1') != 0:
            hex_data += dic[temp.count('1')]
        
    return hex_data


#convert ASCII HEX into corresponding data
def hex2Data(hex_data):
    if len(hex_data) % 2 == 1:
        temp = hex_data[:-1]
    else:
        temp = hex_data

    return codecs.decode(temp, "hex").decode('utf-8')


#to terminate transmission
def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)
	

#jump here when got interupt
def got_intrpt(channel):
    global i
    global data, raw_credentials, credentials_list
    
    #print("recv: ",i)
    data += str(GPIO.input(data_recv_pin))
    i += 1
    
    if(i == 10000):
        pwm_pin.ChangeDutyCycle(0)
        raw_Hex_data = bin2Hex(data)
        Hex_data = raw_Hex_data[raw_Hex_data.find("3c"):]
        raw_credentials = hex2Data(Hex_data)
        credentials_list = check_credentials(set_credentials(raw_credentials))
        GPIO.cleanup()
        sys.exit(0)
        signal.pause()
		
		
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin,GPIO.OUT)        #output PWM pin

pwm_sig = GPIO.PWM(pwm_pin,300)     #set PWM freq

GPIO.setup(data_recv_pin,GPIO.IN)       #input data receiving pin

GPIO.setup(intrpt,GPIO.IN, pull_up_down = GPIO.PUD_UP)          #set edge trigure
GPIO.add_event_detect(intrpt, GPIO.FALLING, callback= got_intrpt, bouncetime=2)     #setup for interupt

pwm_sig.start(50)           #sets duty cycle of PWM

signal.signal(signal.SIGINT, signal_handler)        #wait for keyboard press 'CTRL + C'
signal.pause()
