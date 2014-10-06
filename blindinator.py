# The Blindinator v1.0 by Ivan Cooper & Meena Shah
# created for San Francisco Science Hack Day 2014

from SimpleCV import *
import usb, sys
from arduino.usbdevice import ArduinoUsbDevice
from collections import deque
 
try:
        USBlindinator = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
except:
        sys.exit("Blindinator Not Found")

# "calibration" given in servo values
pleft=66
pright=141
ptop=59
pbottom=111

class point(object):
  def __init__(self,x,y):
     self.x=x
     self.y=y

def aim_and_fire():
        if lit:
                s="*"
        else:
                s="."
        s = s+(chr(ord('0')+(180-servo_pos.x)))+(chr(ord('0')+(180-servo_pos.y)))
        for c in s:
                try:
                        USBlindinator.write(ord(c))
                except:
                        print "warning: device write error"

def laser(isOn):
        global lit
        lit=isOn
        aim_and_fire()

def up():
        global servo_pos
        if(servo_pos.y>0):
                servo_pos.y-=1
        aim_and_fire()
def down():
        global servo_pos
        if(servo_pos.y<180):
                servo_pos.y+=1
        aim_and_fire()
def left():
        global servo_pos
        if(servo_pos.x>0):
                servo_pos.x-=1
        aim_and_fire()
def right():
        global servo_pos
        if(servo_pos.x<180):
                servo_pos.x+=1
        aim_and_fire()
def center():
        global servo_pos
        servo_pos.x=90
        servo_pos.y=90
        aim_and_fire()

def process_point(pos):
        queue.append(pos)
        qlen = len(queue)
        if qlen > 5:
                queue.popleft()
                qlen-=1
        xsum=ysum=0.0
        for pt in queue:
                xsum += pt.x
                ysum += pt.y
        return point(int(xsum/qlen),int(ysum/qlen))

def update_target(find_list):
        global has_eye
        # todo: examine second/third found point; discard outliers
        if find_list:
                result = process_point(find_list[0])
                if not has_eye:
                        has_eye = True
                        print "found eye"
                #result = find_list[0]
        else:
                if has_eye:
                        print "lost eye" #ow
                        has_eye = False
                result = None
        return result

def reset_target():
        queue.clear()

def blindinate(cameraPoint):
        global servo_pos,lit
        px = pleft + (cameraPoint.x*(pright-pleft)/640)
        py = ptop + (cameraPoint.y*(pbottom-ptop)/480)
        lit=not safety
        servo_pos.x=px
        servo_pos.y=py
        aim_and_fire();
        #print "blindinating ("+str(cameraPoint.x)+","+str(cameraPoint.y)+") by tracking to ("+str(servo_pos.x)+","+str(servo_pos.y)+")"        

def Look():
        global safety # this is not a thing
        quitting = False
        track = False
        preview = True
        cam = Camera()
        disp = Display()
        print cam.getImage().listHaarFeatures()
        while not quitting:
                img = cam.getImage()#.colorDistance(Color.ORANGE)

                #somewhat promising for laser dot finding
        #        blobs = img.findBlobs(minsize=10,maxsize=250) # get the largest blob on the screen
        #        if blobs:
        #                for b in blobs:
        #                       if b.isCircle(tolerance=0.5):
        #                               b.draw()                      
                                        #avgcolor = np.mean(blobs[-1].meanColor()) #get the average color of the blob

                #sucks with many different parameters
        #        circs = img.findCircle(canny=200,thresh=350,distance=10)
        #        if circs:
        #                for c in circs:
        #                        c.draw()
                                
                found_features = img.findHaarFeatures(segment)
                target = update_target(found_features)
                if target:
                        if track:
                                blindinate(target)
                        if preview:
                                #found_features.draw() # show multiple matches
                                found_features[-1].draw() # show first match
                                # todo: preview actual target
                elif track:
                        reset_target() # if we lost eye, reset tracking
                        laser(False)
                
                if preview:
                        img.save(disp)

                # handle keypresses and mouse events
                disp.checkEvents()
                if disp.pressed[ord('q')]:
                        quitting=True
                elif disp.pressed[ord('w')]:
                        up()
                elif disp.pressed[ord('a')]:
                        left()
                elif disp.pressed[ord('s')]:
                        right()
                elif disp.pressed[ord('z')]:
                        down()
                elif disp.pressed[ord('c')]:
                        center()
                elif disp.pressed[ord('0')]:
                        laser(False)
                elif disp.pressed[ord('1')]:
                        laser(True)
                elif disp.pressed[ord('u')]:
                        safety=False
                elif disp.pressed[ord('y')]:
                        safety=True
                elif disp.pressed[ord('v')]:
                        preview=True
                elif disp.pressed[ord('o')]:
                        if track: # if track is off, preview forced on
                                preview=False
                elif disp.pressed[ord('t')]:
                        track=True
                        laser(False)
                elif disp.pressed[ord('k')]:
                        track=False
                        preview=True
                        laser(False)
                elif disp.pressed[ord('p')]:
                        print "x="+str(servo_pos.x)+", y="+str(servo_pos.y)


# main

#segment = HaarCascade("nose.xml") #eh. slow
#segment = HaarCascade("eye.xml") #pretty good
#segment = HaarCascade("lefteye.xml") #frequently gets right eye
#segment = HaarCascade("left_eye2.xml") #slow/inaccurate
segment = HaarCascade("right_eye.xml")

queue = deque()
servo_pos = point(90,90)
lit=False
safety=True
has_eye=False

center()
aim_and_fire()
Look()
exit()
