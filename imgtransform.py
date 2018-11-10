import cv2
import numpy as np 

def transform_img(path):
    # read image with opencv
    img = cv2.imread(path)

    # get height and width
    height, width, _ = img.shape

    # convert to grayscale 
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('color_image',img)             

    # subtract asphalt color and take absolute value
    absimg = cv2.absdiff(gray_image, 145)
    #cv2.imshow('absimg',absimg) 
    
    # Otsu binarization 
    ret, bimg = cv2.threshold(absimg, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow('bimg',bimg)
    print(ret)

    # define kernel for convolution 
    kernel = np.ones((5,5),np.uint8)

    # morphological operations to reduce noise
    opening = cv2.morphologyEx(bimg, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    #erosion = cv2.erode(closing,kernel,iterations = 3)
    dilation = cv2.dilate(closing,kernel,iterations = 5)


    #cv2.imshow("opening", opening)
    #cv2.imshow("closing", closing)
    #cv2.imshow("erosion", erosion) 
    #cv2.imshow("dilation", dilation) 
    #k = cv2.waitKey(0)


    for i in range(170, 880, 115):
        for j in range(90, 380, 250):
            if(checkvacancy(i, j, i + 115, j + 250, dilation)):
                cv2.rectangle(img, (i+5, j+5), (i+110, j+245), (0,0,255), 2)
            else:
                cv2.rectangle(img, (i+5, j+5), (i+110, j+245), (0,255,0), 2)
            j += 3
        i += 5


    cv2.imshow("result", img)  


    k = cv2.waitKey(0) # 0==wait forever

    

# top left corner and bottom right corner
# takes in grayscale image 
def checkvacancy(x, y, row, col, img):
    white = 0
    total = 0

    for i in range(x, row, 1):
        for j in range(y, col, 1):
            if(img[j][i] == 255):
                white += 1
            total += 1


    print(white)
    print(total)
    print((white/total) > 0.2)
    print(white/total)


    return ((white/total) > 0.2)





# filepath = input("Enter filename: ")
#
# transform_img("resources/" + filepath)



'''
source = cv2.imread(filepath)


cv2.rectangle(result, (290, 90), (410, 325), (255), 2)
cv2.imwrite("1.png",result)


source = drawbox(290, 90, 410, 325, result, source)


cv2.imshow('result',result)
cv2.imshow('source',source)
k = cv2.waitKey(0) # 0==wait forever
'''









