import cv2
import numpy as np

# Camera Setting
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def nothing() :
  pass

cv2.namedWindow('HSV track Bar')
cv2.createTrackbar('Value low value', 'HSV track Bar', 0, 255, nothing)
cv2.createTrackbar('Value high value', 'HSV track Bar', 0, 255, nothing)

cv2.setTrackbarPos('Value low value', 'HSV track Bar', 20)
cv2.setTrackbarPos('Value high value', 'HSV track Bar', 255)


# Running part
while cv2.waitKey(33) < 0 :
  ret, frame = capture.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  lvalue = np.array([42, 103, cv2.getTrackbarPos('Value low value', 'HSV track Bar')])   
  rvalue = np.array([61, 255, cv2.getTrackbarPos('Value high value', 'HSV track Bar')])

  mask_green = cv2.inRange(hsv, lvalue, rvalue)
  kernel = np.ones((7,7),np.uint8)

  mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
  mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

  seg_cone = cv2.bitwise_and(hsv, hsv, mask=mask_green)
  contours, hier = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  output = cv2.drawContours(seg_cone, contours, -1, (0,0,255), 3)


  cv2.imshow("VideoFrame", frame)
  cv2.imshow("HSV track Bar", output)
