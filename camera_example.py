# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
haar_cascade = cv2.CascadeClassifier("haar_face.xml")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=camera.resolution)
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	image = cv2.rotate(image, cv2.ROTATE_180)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rect = haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=8)
	cadr_x = 320
	cadr_y = 240
	for num, (x,y,w,h) in enumerate(rect):
		cx = x + w//2
		cy = y + h//2
		cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,255), thickness = 2)
		cv2.circle(image, (cx,cy), radius=2, color=(255,255,255), thickness=-1)
		cv2.putText(image, f"face {num}", (x-10,y-10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
		print([abs(cx-cadr_x), abs(cy-cadr_y)], end = "\t")
		if num == len(rect)-1:
			print("\n")

	cv2.circle(image, (cadr_x,cadr_y), radius=3, color=(255,255, 255), thickness=-1)
	# show the frame
	cv2.imshow("Frame", image)
 	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	

# out.release()
cv2.destroyAllWindows()