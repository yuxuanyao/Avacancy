#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import sys
import numpy
import playvideo

def preprocessing(img):
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

        pts1 = np.float32([list(tl), list(tr), list(bl), list(br)])
        pts2 = np.float32([list(t1), list(t2), list(t3), list(t4)])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        result = cv2.warpPerspective(img, matrix, (maxWidth, maxHeight))
        return result

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
'''
def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1
'''
def get_frame():

    src="resources/parking480.mov"

    ramp_frames=100

    camera=cv2.VideoCapture(src) #this makes a web cam object

    retval, im = camera.read()
    #i=1
    frame_count = 0
    
    while retval:
        
        if(frame_count > 1000/25):
            im = preprocessing(im)
            im = playvideo.transform_img(im)
            imgencode = cv2.imencode('.jpg', im)[1]
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
            frame_count = 0
        frame_count += 1
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        #i+=1
        retval, im = camera.read()

    del(camera)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
