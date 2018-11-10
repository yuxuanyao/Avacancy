import cv2

def transform_img(path):
    # read image with opencv
    img = cv2.imread(path)

    # get height and width
    height, width, _ = img.shape

    # convert to grayscale 
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('color_image',img)             
    


    absimg = cv2.absdiff(gray_image, 145)
    cv2.imshow('absimg',absimg) 
    k = cv2.waitKey(0) # 0==wait forever


transform_img("resources/parkinglot.jpg")



