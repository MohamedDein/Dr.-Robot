# import the necessary packages for camera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
#import necessary libraries for raspberry pi and servo control
import RPi.GPIO as GPIO
from time import sleep
#import the experience file for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#initialize the settings of raspberry pi:
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    src = frame.array
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    image = cv2.ximgproc.anisotropicDiffusion(gray,0.02,2,10)
    hight, width = image.shape
    # convert image to gray


    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    # start to detect face and draw rectangle around it
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        center = (x + (w // 2), y + (h // 2))  # calculate the center point of the face
        angle = remap(0, width, 0, 180, center[0])  # convert pixels of center point to angle
        SetAngle(angle)
        # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)

def remap(minPix, maxPix, minAng, maxAng, newPixVal):
    newAngVal= minAng + ((newPixVal - minPix) * (maxAng - minAng) / (maxPix - minPix))
    return newAngVal
