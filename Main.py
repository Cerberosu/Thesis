import cv2 as cv
import numpy as np
import os
import uuid
import SharpnessDetection
from pyimagesearch.centroidtracker import CentroidTracker
import Results


cap = cv.VideoCapture("./InputVideos/targylemez20180614.wmv")
font = cv.FONT_HERSHEY_COMPLEX
path = os.getcwd()
cwd = "/Data/"
ct = CentroidTracker()
crop_imgs = []
totalFrames = 0

'''
minHSV1 = 0, 5, 40
maxHSV1 = 12, 160, 193

minHSV2 = 120, 5, 40
maxHSV2 = 179, 160, 193
'''

'''Data mappa letrehozasa'''
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

'''Kivágott képek lemezre írása'''
def WriteCroppedToDisk():
    for (objectID, crop_img) in crop_imgs:
        createFolder(path + cwd + str(objectID))
        fileName = '%s.jpg' % (str(objectID) + str(uuid.uuid4()))
        try:
            cv.imwrite(os.path.join(path + cwd + str(objectID), fileName), crop_img)
        except:
            pass


'''Előfeldolgozas, zajszures binarisra vagas'''
def PreProcessing():
    blur = cv.GaussianBlur(frame, (3, 3), 0)

    OriginalhsvFrame = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    hsvFrame = OriginalhsvFrame

    minHSV1 = 0, 16, 32
    maxHSV1 = 13, 178, 181

    minHSV2 = 129, 16, 32
    maxHSV2 = 179, 178, 181

    mask1 = cv.inRange(hsvFrame, minHSV1, maxHSV1)
    mask2 = cv.inRange(hsvFrame, minHSV2, maxHSV2)

    mask = cv.bitwise_or(mask1, mask2)
    kernel = np.ones((5, 5), np.uint8)
    erode = cv.erode(mask, kernel, iterations=1)
    dilatation = cv.dilate(erode, kernel, iterations=1)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv.morphologyEx(dilatation, cv.MORPH_CLOSE, kernel)

    return closing


'''kontur kereses, objektum kovetes, objektum keretezese'''
while cap.isOpened():

    ret, frame = cap.read()

    if ret:
        totalFrames += 1
        combinedMask = PreProcessing()
        ######################### Finding contours ##################
        contours, hierarchy = cv.findContours(combinedMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            area = cv.contourArea(contour)
            X, Y, H, W = cv.boundingRect(contour)
            endX = X + H
            endY = Y + W

            if 10000 > area > 1000:
                # bounding box
                #cv.rectangle(frame, (X, Y), (X + H, Y + W), (0, 255, 0), 2)
                # cutting and saving
                box = ([X, Y, endX, endY])
                rects.append(box)


        objects = ct.update(rects)

        for (objectID, centroid) in objects.items():
            ##################### ObjectID#######################
            #text = "ID {}".format(objectID)
            #cv.putText(frame, text, (centroid[0], centroid[1] - 20),
                       #cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            #cv.circle(frame, (centroid[0], centroid[1]), 2, (255, 0, 0), -1)

            # coordinates for cropping
            ext_left = centroid[0] - 60
            ext_right = centroid[0] + 60
            ext_top = centroid[1] - 60
            ext_bot = centroid[1] + 60

            crop_img = frame[ext_top:ext_bot, ext_left:ext_right]
            crop_imgs.append((objectID, crop_img))

        # outputs
        cv.imshow("Frame", frame)
        cv.imshow("Mask", combinedMask)


        # 1000/43= 30fps
        key = cv.waitKey(30)
        if key == 27:
            break

    else:
        break
print('Összes feldogozott kép: {0}'.format(totalFrames))

cap.release()
cv.destroyAllWindows()
WriteCroppedToDisk()
SharpnessDetection.sharpest()
Results.FindingSharpestImgPath()
Results.ShowingSharpestImg()
