# Welcome to PyShine

# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle,struct, time

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	print("starting new")
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture(0)
		vid.set(cv2.CAP_PROP_FRAME_WIDTH,80)			#configures resolution of camera capture
		vid.set(cv2.CAP_PROP_FRAME_HEIGHT,100)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			try:
				client_socket.sendall(message)
				#cv2.imshow('TRANSMITTING VIDEO',frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					client_socket.close()
			except:
				print("Connection Lost...")
				client_socket.close()
				vid.release()
				cv2.destroyAllWindows()
	
