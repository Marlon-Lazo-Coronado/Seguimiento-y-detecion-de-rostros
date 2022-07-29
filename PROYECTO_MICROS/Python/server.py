# Welcome to PyShine

# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle,struct, imutils, time
import serial
from time import sleep

ser = serial.Serial('COM4', 9600, timeout=0.1)
time.sleep(1)

############## STREAM VIDEO PART #######################################
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
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Socket Accept
while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture(0)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = cv2.flip(frame, 1)  # mirror the image
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = faceClassif.detectMultiScale(gray, 1.1, 6) #detect the face

			
			for (x, y, w, h) in faces:


				# sending coordinates to Arduino
				string = 'X{0:d}Y{1:d}'.format((x + w // 2), (y + h // 2))
				print(string)
				ser.write(string.encode('utf-8'))
				# plot the center of the face
				cv2.circle(frame, (x + w // 2, y + h // 2), 2, (0, 255, 0), 2)
				# plot the roi
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)


			dim = (640, 480)
			newFrameSize = cv2.resize(frame, dim)
			cv2.imshow('frame', newFrameSize)

			frame2 = frame


			frame2 = imutils.resize(frame,width=320)
			a = pickle.dumps(frame2)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)


			#cv2.imshow('TRANSMITTING VIDEO',frame)
			key = cv2.waitKey(1) & 0xFF
			if key ==ord('q'):
				client_socket.close()



cap.release()
cv2.destroyAllWindows()
