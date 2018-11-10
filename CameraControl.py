import cv2
import imgtransform

camera_port = 0
ramp_frames = 30
frame_duration = 25
fps = 1000/frame_duration

cv2.namedWindow("preview")
vc = cv2.VideoCapture(camera_port)

# camera_capture = get_image()
# file = "./screenshots/1.png"
# cv2.imwrite(file, camera_capture)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

frame_count = 0
file_i = 0
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(frame_duration)
    frame_count += 1

    if frame_count == 4*fps:
        frame_count = 0
        file = "./screenshots/" + str(file_i) + ".png"
        cv2.imwrite(file, frame)
        file_i += 1
        imgtransform.transform_img(file)

    if key == 27: # exit on ESC
        break

del(vc)
cv2.destroyWindow("preview")