from centroidtracker import CentroidTracker


import cv2

import imutils

import time

import sys

model_path = "Model/age-gender-recognition-retail-0013.xml"

pbtxt_path = "Model/age-gender-recognition-retail-0013.bin"

print("Load Model .....")

net = cv2.dnn.readNet(model_path, pbtxt_path)

face_cascade = cv2.CascadeClassifier('Model/haarcascade_frontalface_default.xml')

cascade_scale = 1.2

cascade_neighbors = 6

minFaceSize = (50,50)

gender = ['Women','Man']

net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()

# loop over the frames from the video stream
person = 0

print("Detecting .....")

def getFaces(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(

        gray,

        scaleFactor= cascade_scale,

        minNeighbors=cascade_neighbors,

        minSize=minFaceSize,

        flags=cv2.CASCADE_SCALE_IMAGE

    )

    bboxes = []

    for (x,y,w,h) in faces:

        if(w>minFaceSize[0] and h>minFaceSize[1]):

            bboxes.append((x, y, w, h))
          
            

    return bboxes

camera = cv2.VideoCapture(0)

frameID = 0

grabbed = True

start_time = time.time()

while grabbed:

    (grabbed, img) = camera.read()

    img = cv2.resize(img, (550,400))

    out = []
    
    rects = []

    frame = img.copy()

    faces= getFaces(frame)

    x, y, w, h = 0, 0, 0, 0

    i = 0
    
    

    for (x,y,w,h) in faces:

        cv2.rectangle( frame,(x,y),(x+w,y+h),(0,255,0),2)
        

        if(w>0 and h>0):

            facearea = frame[y:y+h, x:x+w]

            blob = cv2.dnn.blobFromImage(facearea, size=(62, 62), ddepth=cv2.CV_8U)

            net.setInput(blob)

            out = net.forward()
            predict_gender = out[0][1][0][0]
            
            gd=gender[int(predict_gender +0.5)]
            rects.append((x, y, w, h,gd))
            txt = "{}".format(gd)
          
            if(i % 2 == 0):
                cv2.putText(frame,txt,(int(x), int(y)),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 255, 0), 2)

            else:
                cv2.putText(frame,txt,(int(x), int(y+h)),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 255, 0), 2)

            i += 1

    objects , nMan , nWomen  = ct.update(rects)
    

	# loop over the tracked objects
    for (objectID, centroid ) in objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
        #text = "ID {}".format(objectID)
        if(objectID>person):
            person = person+1
            
        #cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    frameID += 1

    fps = frameID / (time.time() - start_time)
    FPS = "FPS: {:.2f}".format(fps)
    Pcount = "All:{}".format(person)
    Mcount = "Man:{}".format(nMan)
    Fcount = "Women:{}".format(nWomen)
    cv2.putText(frame, FPS,(0,15), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (51,153,255), 2, cv2.LINE_AA)
    cv2.putText(frame, Pcount,(0,35), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (51,153,255), 2, cv2.LINE_AA)
    cv2.putText(frame, Mcount,(0,55), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (51,153,255), 2, cv2.LINE_AA)
    cv2.putText(frame, Fcount,(0,75), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (51,153,255), 2, cv2.LINE_AA)
    cv2.imshow("FRAME", frame)

    if cv2.waitKey(1)&0xFF == ord('q'):
        print("All Man = ",nMan )
        print("All Women = ",nWomen)
        print("All pleplo = ",person)
        print("Finish.! Bye")
        sys.exit(0)
