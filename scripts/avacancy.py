#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2


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
vc = cv2.VideoCapture("resources/parking480.mov")

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        #frame = preprocessing(frame)
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
