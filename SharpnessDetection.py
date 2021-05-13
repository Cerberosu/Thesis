import cv2 as cv
from imutils import paths
import os
import time
import array as arr

directory = os.getcwd() + "\data/"


# elements = [[], []]
def laplacianSharpest():
    global spMaxImagePath

    def variance_of_laplacian(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv.Laplacian(image, cv.CV_64F).var()

    for path in os.listdir(".\data"):
        elements = [[], []]
        # képeken megy végig
        for imagePath in paths.list_images(directory + str(path)):
            image = cv.imread(imagePath)
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            sp = variance_of_laplacian(gray)
            elements[0].append(imagePath)
            elements[1].append(sp)

            spMaxIndex = elements[1].index(max(elements[1]))
            spMaxImagePath = elements[0][spMaxIndex]

        try:
            os.rename(spMaxImagePath, directory + str(path) + "/legelesebb.jpg")
        except:
            pass


def badSizeRemove():
    for path in os.listdir(directory):
        for imagePath in paths.list_images(directory + str(path)):
            img = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)
            h, w = img.shape
            if not (h == 120 and w == 120):
                os.remove(imagePath)


def rmEmpty():
    for item in os.listdir(directory):
        if len(os.listdir(os.path.join(directory + item))) == 0:
            os.rmdir(directory + item)


def sharpest():
    rmEmpty()
    badSizeRemove()
    laplacianSharpest()
