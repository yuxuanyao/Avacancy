import cv2

camera_port = 0
ramp_frames = 30

cv2.namedWindow("preview")
vc = cv2.VideoCapture(camera_port)

# camera_capture = get_image()
# file = "./screenshots/1.png"
# cv2.imwrite(file, camera_capture)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break

del(vc)
cv2.destroyWindow("preview")