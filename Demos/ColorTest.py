import cv2
import numpy as np


def nothing():
    pass


b = 0
g = 0
r = 0
bgr = [b, g, r]
thresh = 40

originalIMG = cv2.imread('./VilagosLila/tanito_1.jpg')
originalIMG = cv2.resize(originalIMG, (500, 500))



def ColorFinder(event, x, y, flags, param):
    global bgr
    if event == cv2.EVENT_MOUSEMOVE:  # checks mouse moves
        colorsBGR = originalIMG[y, x]
        bgr = np.array([colorsBGR[0], colorsBGR[1], colorsBGR[2]])
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        print("HSV Value at ({},{}):{} ".format(x, y, hsv))
        print("BGR Value at ({},{}):{} ".format(x, y, colorsBGR))


def ColorCuc():
    while True:
        global bgr

        kernel = np.ones((5, 5), np.uint8)
        blur = cv2.blur(originalIMG, (10, 10))

        ResultOriginal = cv2.erode(originalIMG, kernel)
        brightHSV = cv2.cvtColor(ResultOriginal, cv2.COLOR_BGR2HSV)
        # HSV
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        minHSV = np.array([hsv[0] - 10, hsv[1] - thresh, hsv[2] - thresh])
        maxHSV = np.array([hsv[0] + 10, hsv[1] + thresh, hsv[2] + thresh])
        maskHSV = cv2.inRange(brightHSV, minHSV, maxHSV)

        # BitwiseHSV
        # resultHSV = cv2.bitwise_and(brightHSV, brightHSV, mask=maskHSV)
        # mask = cv2.erode(mask, kernel)

        resultHSV = maskHSV

        cv2.imshow("Mask Bitwise nelkul", resultHSV)
        cv2.imshow("Original", originalIMG)
        cv2.imshow("Result Original", ResultOriginal)
        cv2.setMouseCallback('Result Original', ColorFinder)
        cv2.setMouseCallback('Original', ColorFinder)

        key = cv2.waitKey(1)
        if key == 27:
            break


ColorCuc()
