import numpy as np
import cv2
import imgtransform as ti
from threading import Thread

frame_duration = 25
fps = 1000/frame_duration

def transform_img(img, availability= [[0] * 5 for i in range(4)]):
	# get height and width
	height, width, _ = img.shape

	# convert to grayscale
	gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('gray_image', gray_image)

	# subtract asphalt color and take absolute value
	absimg = cv2.absdiff(gray_image, 80)

	# Otsu binarization
	ret, bimg = cv2.threshold(absimg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# cv2.imshow('bimg',bimg)

	# define kernel for convolution
	kernel = np.ones((5, 5), np.uint8)

	# morphological operations to reduce noise
	opening = cv2.morphologyEx(bimg, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
	# erosion = cv2.erode(closing,kernel,iterations = 3)
	dilation = cv2.dilate(closing, kernel, iterations=3)
	# cv2.imshow("dilation", dilation)

	y = 0
	for i in range(0, width, int(width/5)):
		x = 0
		for block in range(2):
			j = 0
			while j < int(height/2):
				j_ = int(block*height/2) + j
				if i<width and j_<height:
					if (ti.checkoccupancy(i, j_, i + int(width/5), j_ + int(height*0.13), dilation)
							or (i > 2.5/5*width)):
						colour = (0, 0, 255)
						# cv2.rectangle(img, (i + 5, j_ + 5), (i + int(width/5)-5, j_ + int(height*0.13)-5), (0, 0, 255), 2)
					else:
						colour = (0, 255, 0)
						availability[x][y] = 1
						# cv2.rectangle(img, (i + 5, j_ + 5), (i + int(width/5)-5, j_ + int(height*0.13)-5), (0, 255, 0), 2)
					cv2.rectangle(img, (i + 5, j_ + 5), (i + int(width / 5) - 5, j_ + int(height * 0.13) - 5), colour, 2)
					j_ += int(height * (0.22 + 0.13))
					j = j_ - int(block*height/2)
				x += 1
		y += 1
		i += 5

	cv2.imshow("Label", img)
	print(availability)
	return img

while True:
	cap = cv2.VideoCapture("resources/parking480.mov")

	ret, frame = cap.read()
	frame_count = 0
	file_i = 0
	while(ret):
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# top left
		tl = (293, 96)
		# top right
		tr = (490, 100)
		#bottom left
		bl = (30, 310)
		#bottom right
		br = (560, 330)

		# max width
		# widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
		# widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
		# maxWidth = max(int(widthA), int(widthB))

		# max height
		# heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
		# heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
		# maxHeight = max(int(heightA), int(heightB))

		t1 = (0, 0)
		t2 = (300, 0)
		t3 = (0, 500)
		t4 = (300, 500)

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

		# result = cv2.warpPerspective(frame, matrix, (maxWidth, maxHeight))
		result = cv2.warpPerspective(frame, matrix, (300, 500))

		frame_count += 1
		if frame_count > fps:
			# if __name__ == '__main__':
			# 	Thread(target=transform_img, args=(result, )).start()
			transform_img(result)
			file_i += 1
			frame_count = 0

		cv2.imshow('Pre-label', result)
		cv2.imshow('frame', frame)

		ret, frame = cap.read()

		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

	cap.release()
cap.release()
cv2.destroyAllWindows()






