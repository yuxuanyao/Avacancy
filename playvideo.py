import numpy as np
import cv2

cap = cv2.VideoCapture("resources/parking480.mov")

while(cap.isOpened()):
	ret, frame = cap.read()

	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# top left
	tl = (293, 96)
	# top right
	tr = (490, 100)
	#bottom left
	bl = (30, 310)
	#bottom right
	br = (560, 330)

	# max width
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# max height
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	t1 = (0, 0)
	t2 = (maxWidth, 0)
	t3 = (0, maxHeight)
	t4 = (maxWidth, maxHeight)

	'''
	cv2.circle(frame, tl, 5, (0, 0, 255), -1)
	cv2.circle(frame, tr, 5, (0, 0, 255), -1)
	cv2.circle(frame, bl, 5, (0, 0, 255), -1)
	cv2.circle(frame, br, 5, (0, 0, 255), -1)

	cv2.circle(frame, t1, 5, (0, 255, 0), -1)
	cv2.circle(frame, t2, 5, (0, 255, 0), -1)
	cv2.circle(frame, t3, 5, (0, 255, 0), -1)
	cv2.circle(frame, t4, 5, (0, 255, 0), -1)
	'''

	pts1 = np.float32([list(tl), list(tr), list(bl), list(br)])
	pts2 = np.float32([list(t1), list(t2), list(t3), list(t4)])
	
	matrix = cv2.getPerspectiveTransform(pts1, pts2)

	result = cv2.warpPerspective(frame, matrix, (maxWidth, maxHeight))

	cv2.imshow('result',result)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#while(True):
cap.release()
cv2.destroyAllWindows()






