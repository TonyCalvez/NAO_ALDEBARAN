import sys
import motion
import time
from naoqi import ALProxy
import math


robotIp="172.20.26.29"
robotIp="betanao"
robotIp="172.20.11.241"
robotPort=9559

robotIp="localhost"
robotPort=11212

x=0.0
y=0.0
theta=0.0
if len(sys.argv) == 6:
    robotIp = sys.argv[1]
    robotPort = int(sys.argv[2])
    x = float(sys.argv[3])
    y = float(sys.argv[4])
    theta = float(sys.argv[5])*math.pi/180.0
if len(sys.argv) == 3:
    robotIp = sys.argv[1]
    robotPort = int(sys.argv[2])

print robotIp,robotPort,x,y,theta

try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

# Set NAO in Stiffness On 
# using wakeUp (new feature in 1.14.1)
motionProxy.wakeUp()


# Send NAO to Pose Init : it not standing then standing up
#postureProxy.goToPosture("StandInit", 0.5)

# Enable arms control by Walk algorithm
motionProxy.setWalkArmsEnabled(True, True)

# allow to stop motion when losing ground contact, NAO stops walking
# when lifted  (True is default)
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

motionProxy.moveTo (x, y, theta)

# End Walk (putting NAO at rest position to save power)
if (x == 0.0) and (y == 0.0) and (theta==0.0):
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest()
