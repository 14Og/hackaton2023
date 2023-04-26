import cv2
import numpy as np


class Camera_Tracker:
    def __init__(self,camera=cv2.VideoCapture(0),resolution=(640, 480),roi_side=200):
        # initializing camera, in rpi case will be Picamera()
        self.camera = camera
        # initializing camera resolution, in rpi case will be also a framerate param
        self.width = resolution[0]
        self.height = resolution[1]
        # center of frame
        self.cx = self.width//2
        self.cy = self.height//2
        self.detector = cv2.createBackgroundSubtractorMOG2(history=120,
                                                           varThreshold=50)
        # initializng region of object detector interest: in this case will be square 200x200 in center of frame
        self.roi_list = [self.cx-roi_side, self.cx+roi_side, self.cy-roi_side, self.cy+roi_side]
     
    def detect_roi(self,frame):  # this methos returns slice of frame, on which we are interested the most
        return frame[self.roi_list[0]:self.roi_list[1], self.roi_list[2]:self.roi_list[3]]
    
    def process_frame(self):
        color_mask_max = np.array([255,111,61])
        color_mask_min = np.array([120, 30, 20])
        ret, self.frame = self.camera.read()
        if not ret:
            return "No video found, quit"
        self.frame = cv2.resize(self.frame, (self.width, self.height), cv2.INTER_CUBIC)
        cv2.circle(self.frame, (self.cx, self.cy), 3, (255,255,255), thickness=-1)
        self.roi = self.detect_roi(self.frame)
        self.mask = cv2.inRange(self.roi, color_mask_min, color_mask_max)
        _, mask = cv2.threshold(self.mask, 220, 255, cv2.THRESH_BINARY)
        # finding countours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        # sorting list of contours by area parameter:
        # first element of sorted list is coordinates of contour with highest area rate
        cnt = list(sorted(contours, key=lambda f: cv2.contourArea(f), reverse=True))
        if len(cnt) > 0:
            x, y, w, h = cv2.boundingRect(cnt[0])
            self.contour_cx = x + w//2
            self.contour_cy = y + h//2
            # putting rectangle to your contour
            cv2.rectangle(self.roi, (x,y), (x+w,y+h), (0,255,0), thickness=2)
            return f"X difference:{abs(self.cx - self.contour_cx)}\t Y difference: {abs(self.cy - self.contour_cy)}"

    def processed_video(self):
        while True:
            print(self.process_frame())
            cv2.imshow("Frame",self.frame)
            cv2.imshow("Mask", self.mask)
            if cv2.waitKey(1) == ord("q"):
                break
        cv2.destroyAllWindows()
            

if __name__ == "__main__":      
    cam = Camera_Tracker()
    cam.processed_video()
