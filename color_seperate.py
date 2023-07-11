import cv2

# Camera Setting
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# TrackBar Create
def nothing() :
  pass

cv2.namedWindow('Hue track Bar')
cv2.createTrackbar('Hue low value', 'Hue track Bar', 0, 179, nothing)
cv2.createTrackbar('Hue high value', 'Hue track Bar', 0, 179, nothing)

cv2.setTrackbarPos('Hue low value', 'Hue track Bar', 32)
cv2.setTrackbarPos('Hue high value', 'Hue track Bar', 60)

# Running part

while cv2.waitKey(33) < 0 :
  lvalue = cv2.getTrackbarPos('Hue low value', 'Hue track Bar')
  rvalue = cv2.getTrackbarPos('Hue high value', 'Hue track Bar')

  ret, frame = capture.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsv)
  h = cv2.inRange(h, lvalue, rvalue)

  cone = cv2.bitwise_and(hsv, hsv, mask=h)
  cone = cv2.cvtColor(cone, cv2.COLOR_HSV2BGR)

  cv2.imshow("VideoFrame", frame)
  cv2.imshow("Hue track Bar", cone)
