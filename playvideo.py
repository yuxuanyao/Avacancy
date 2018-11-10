import numpy as np
import cv2

cap = cv2.VideoCapture("resources/parking480.mov")

while(cap.isOpened()):
	ret, frame = cap.read()

	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	cv2.circle(frame, (293, 96), 5, (0, 0, 255), -1)
	cv2.circle(frame, (490, 100), 5, (0, 0, 255), -1)
	cv2.circle(frame, (30, 310), 5, (0, 0, 255), -1)
	cv2.circle(frame, (560, 330), 5, (0, 0, 255), -1)

	cv2.circle(frame, (0, 0), 5, (0, 255, 0), -1)
	cv2.circle(frame, (600, 0), 5, (0, 255, 0), -1)
	cv2.circle(frame, (0, 400), 5, (0, 255, 0), -1)
	cv2.circle(frame, (600, 400), 5, (0, 255, 0), -1)

	pts1 = np.float32([[293, 96], [490, 100], [30, 310], [560, 330]])
	pts2 = np.float32([[0, 0], [600, 0], [0, 400], [600, 400]])
	
	matrix = cv2.getPerspectiveTransform(pts1, pts2)

	result = cv2.warpPerspective(frame, matrix, (600, 400))

	cv2.imshow('result',result)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#while(True):
cap.release()
	#cv2.destroyAllWindows()
