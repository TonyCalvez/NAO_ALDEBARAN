import sys
import time
import cv2
from naoqi import ALProxy
import numpy as np
import random
import math
import os
import signal

# specific to my laptop version (do not exist on Centos Students PCs)
#import Image
try:
   from PIL import Image
except:
   import Image


def cleanKillNao(signal, frame):
   global postureProxy,motionProxy
   print "pgm interrupted, put NAO is safe pose ..."
   postureProxy.goToPosture("Crouch", 0.5)
   time.sleep(0.5)
   stiffnesses  = 0.0
   motionProxy.setStiffnesses(["Body"], stiffnesses)
   exit()


def check_constant_green_image (img,width,height):
   tstpix = []
   tstpix.append (cvImg[0,0])
   tstpix.append (cvImg[0,width-1])
   tstpix.append (cvImg[height-1,0])
   tstpix.append (cvImg[height-1,width-1])
   cstgreen = True
   for pix in tstpix:
      if pix[0] != 0:
         cstgreen = False
         break
      if (pix[1] != 154) and (pix[1] != 135):
         cstgreen = False
         break
      if pix[2] != 0:
         cstgreen = False
         break
   return cstgreen


debug=False
#debug=True

# save images for image processing setup
#saveImgs=True
saveImgs=False
imgCount=0

IP = "localhost"  # NaoQi's IP address.
PORT = 11212  # NaoQi's port
# if one NAO in the scene PORT is 11212
# if two NAOs in the scene PORT is 11212 for the first and 11216 for the second 

# Read IP address and PORT form arguments if any.
print "%3d arguments"%(len(sys.argv))
if len(sys.argv) > 1:
   IP = sys.argv[1]
if len(sys.argv) > 2:
   PORT = int(sys.argv[2])


# get image from vrep simulator
# set the pass to vnao to the correct path on your computer
#vnao_path = "/home/newubu/MyApps/Nao/v-rep/nao-new-model/tmp/vnao"
vnao_path = "/home/newubu/Robotics/nao/vnao/plugin-v2"
# set vnao image name 
vnao_image = "imgs/out_%5.5d.ppm"%(PORT)
cameraImage=os.path.join(vnao_path,vnao_image)

# init motion
try:
   motionProxy = ALProxy("ALMotion", IP, PORT)
except Exception, e:
   print "Could not create proxy to ALMotion"
   print "Error was: ", e
   exit(1)

# init posture
try:
   postureProxy = ALProxy("ALRobotPosture", IP, PORT)
except Exception, e:
   print "Could not create proxy to ALPosture"
   print "Error was: ", e
   exit(1)


# work ! set current to servos
stiffnesses  = 1.0
motionProxy.wakeUp()
postureProxy.goToPosture("Crouch", 0.5)
#time.sleep(0.5)

# relax all servos by removing current (prevent over heating)
stiffnesses  = 0.0
motionProxy.setStiffnesses(["Body"], stiffnesses)
#time.sleep(0.5)

names  = ["HeadYaw", "HeadPitch"]
stiffnesses  = 1.0   # only activate head pitch and yaw servos
motionProxy.setStiffnesses(names, stiffnesses)
angles  = [0.0, 0.0]
fractionMaxSpeed  = 1.0
motionProxy.setAngles(names, angles, fractionMaxSpeed)

signal.signal(signal.SIGINT, cleanKillNao)

# init video
cameraProxy = ALProxy("ALVideoDevice", IP, PORT)
resolution = 1    # 0 : QQVGA, 1 : QVGA, 2 : VGA
colorSpace = 11   # RGB
camNum = 0 # 0:top cam, 1: bottom cam
fps = 4; # frame Per Second
dtLoop = 1./fps
cameraProxy.setParam(18, camNum)
try:
   lSubs=cameraProxy.getSubscribers()
   for subs in lSubs:
      if subs.startswith("python_client"):
         cameraProxy.unsubscribe(subs)
except:
   print "cannot unsubscribe"
   pass
try:
   videoClient = cameraProxy.subscribeCamera("python_client",camNum, 
                                       resolution, colorSpace, fps)
except:
   print "pb with subscribe"
   lSubs=cameraProxy.getSubscribers()
   for subs in lSubs:
      if subs.startswith("python_client"):
         cameraProxy.unsubscribe(subs)
   videoClient = cameraProxy.subscribeCamera("python_client",camNum,
                                       resolution, colorSpace, fps)
print cameraProxy.getSubscribers()
print "videoClient ",videoClient
# Get a camera image.
# image[6] contains the image data passed as an array of ASCII chars.
naoImage = cameraProxy.getImageRemote(videoClient)
imageWidth = naoImage[0]
imageHeight = naoImage[1]
array = naoImage[6]
# print imageWidth,"x",imageHeight
# Create a PIL Image from our pixel array.
#pilImg = Image.fromstring("RGB", (imageWidth, imageHeight), array)
pilImg = Image.frombytes("RGB", (imageWidth, imageHeight), array)
# Convert Image to OpenCV
cvImg = np.array(pilImg)
# Convert RGB to BGR 
cvImg = cvImg[:, :, ::-1].copy()

# define display window
cv2.namedWindow("proc")
cv2.resizeWindow("proc",imageWidth,imageHeight)
cv2.moveWindow("proc",0,0)
cv2.imshow("proc",cvImg)
cv2.waitKey(1)

# if image is constant green, then we are on the simulator (no actual video frame)
cstGreen = check_constant_green_image (cvImg,imageWidth,imageHeight)
if cstGreen:
   print "run on simulated NAO, no video frame, use still images"
else:
   print "run on real NAO"

# Test getting a virtual camera image.
imgok=False
while not imgok:
   if cstGreen:
      try:
         cvImg = cv2.imread(cameraImage)
         imageHeight, imageWidth, imageChannels = cvImg.shape
         imgok=True
      except Exception, e:
         print "Can't read image %s, retry ..."%(cameraImage)
         imgok=False
         time.sleep(0.25)
   else:
      imgok=True

print "Image Size",imageWidth,imageHeight

missed = 0

while missed < 30: 
   t0=time.time()
   # Get current image (top cam)
   imgok=False
   found=False
   while not imgok:
      if cstGreen:
         try:
            cvImg = cv2.imread(cameraImage)
            imgok=True
         except Exception, e:
            print "Can't read image %s, retry ..."%(cameraImage)
            imgok=False
            time.sleep(0.25)
         cvImg = cv2.flip(cvImg,0)
         # Save it (just to check)
         if debug:
            cv2.imwrite ("naosimimg.png",cvImg)
      else:
         naoImage = cameraProxy.getImageRemote(videoClient)
         array = naoImage[6]
         # Create a PIL Image from our pixel array.
         pilImg = Image.frombytes("RGB", (imageWidth, imageHeight), array)
         cvImg = np.array(pilImg) # Convert Image to OpenCV
         cvImg = cvImg[:, :, ::-1].copy() # Convert RGB to BGR
         imgok=True
   if saveImgs:
      if cstGreen:
         cv2.imwrite ("naosimu_%4.4d.png"%(imgCount),cvImg)
      else:
         cv2.imwrite ("naoreal_%4.4d.png"%(imgCount),cvImg)
      imgCount+=1
   cv2.imshow("proc",cvImg)
   cv2.waitKey(1)

   #
   # insert detection function here
   #
   
   if (found):
      missed = 0

      #
      # insert head control here
      #

   else:
      missed += 1
   dt = time.time()-t0
   tSleep = dtLoop-dt
   if tSleep>0:
      time.sleep(tSleep)
   print "dtLoop = ",dtLoop,"tSleep = ",tSleep,"dt = ",dt,"frame rate = ",1./dt


# relax !  no current in servos
print postureProxy.getPostureList()
postureProxy.goToPosture("Crouch", 0.5)
stiffnesses  = 0.0
motionProxy.setStiffnesses(["Body"], stiffnesses)

sys.exit(0)
