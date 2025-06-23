import socket,cv2, pickle, struct, time		
import RPi.GPIO as GPIO			#library to work with GPIO pins of Respberry PI

GPIO.setmode(GPIO.BCM)			#Configure Respberry PI PINS in Broadcom chip-specific pin numbers
GPIO.setwarnings(False)

data = b""
payload_size = struct.calcsize("Q")			#8 bit

Trig = 23		#Trig pin of UltraSonic Sensor
Echo = 24		#Echo pin of UltraSonic Sensor

dis_cnt = 0
dis_cnt_threshold = 3		#to set Connect Time Threshold
disconnect_cnt = 0
disconnect_cnt_threshold = 2		#to set Dis-Connect Time Threshold
dis = 0				#Distance btw vehicles
temp = 0

print("\n Sensor is acivated")
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

def getDis(delay):				#to calculate Distance by UltraSonic Sensor
	GPIO.output(Trig, False)
	time.sleep(delay)
	GPIO.output(Trig, True)
	time.sleep(0.00001) #100 micro sec
	GPIO.output(Trig, False)
	
	while GPIO.input(Echo) == 0:
		pulse_start = time.time()
	while GPIO.input(Echo) == 1:
		pulse_end = time.time()
		
	return float(round(((pulse_end - pulse_start) * 17150),2))
	
	
# prev_time = 0
# new_time = 0
# totalfps = 0
# count = 0
# FPS = 0

# create socket
host_ip = '10.42.0.1' # paste your server ip address here
port = 9999			#paste  your server Host Port here

while True:
	while True:
		dis = getDis(1)			#get Distance with delay of 1 sec
		
		if 0.1<dis<30:								#Count upto Connect Threshold if distance maintained within rage
			if dis_cnt == dis_cnt_threshold:
				dis_cnt = 0
				break
			else:
				dis_cnt += 1
				print("Distance : ", dis, "      dis_cnt : ", dis_cnt)
		else:
			dis_cnt = 0

	client_socket = None				#clears the Client Socket to establish new connection
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)			#configures client socket with TCP protocol
	client_socket.connect((host_ip,port)) 			#wait here untill connect
	data = b""

	while True:
		if temp == 20:
			dis = getDis(0.01)			#get Distance with delay of 0.001 sec
			temp = 0
			
			if not 0.1<dis<30:				#count upto Dis-Connect Threshold if distance does not maintained within rage
				disconnect_cnt += 1
				#print("Distance : ", dis, "      dis_cnt : ", disconnect_cnt)
		else:
			temp += 1
			
			
		if disconnect_cnt == disconnect_cnt_threshold:
			disconnect_cnt = 0
			print("Disconnected...")		
			client_socket.close()			#disconnect Client Socket
			cv2.destroyAllWindows()			#closes all windows
			break
		else:
			#fetch data and displays
			while len(data) < payload_size:
				packet = client_socket.recv(10*1024) 		#receive data with buffer of 10KB
				if not packet: break
				data+=packet
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q",packed_msg_size)[0]
			
			while len(data) < msg_size:
				data += client_socket.recv(10*1024)			#receive data with buffer of 10KB
			frame_data = data[:msg_size]
			data  = data[msg_size:]
			frame = pickle.loads(frame_data)


			# try:
				# new_time = time.time()
				# fps = 1/(new_time-prev_time)
				# fps = int(fps)
				# prev_time = new_time
				# if(count != 1):
					# totalfps += fps
					# count += 1
				# else:
					# FPS = totalfps/1
					# totalfps = 0
					# count = 0
			# except:
				# FPS = 0
			# finally:
				# prev_time = new_time

			# coordinates = (10,35)
			# font = cv2.FONT_HERSHEY_SIMPLEX
			# fontScale = 1
			# color = (3,66,10)
			# thickness = 2
			# image = cv2.putText(cv2.flip(frame, 1), str(FPS), coordinates, font, fontScale, color, thickness, cv2.LINE_AA)

			cv2.namedWindow("Receiving Video",cv2.WINDOW_NORMAL)
			cv2.setWindowProperty("Receiving Video",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
			try:
				cv2.imshow("Receiving Video",frame)			#displays frame
			except:
				disconnect_cnt = 0
				print("Disconnected...")		
				client_socket.close()			#disconnect Client Socket
				cv2.destroyAllWindows()			#closes all windows
				break
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				client_socket.close()		#close client socket when key 'Q' pressed
				break
