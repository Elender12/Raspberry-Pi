from picamera import PiCamera
from time import sleep
camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/image4.jpg')
camera.stop_preview()
