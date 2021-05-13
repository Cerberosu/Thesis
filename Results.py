import os
import matplotlib.pyplot as plt
from imutils import paths
import cv2 as cv

directory = os.getcwd() + "\data/"
fileNames = []
fig = plt.figure(figsize=(16, 9))
foundImgNumber = 0


def FindingSharpestImgPath():
    global foundImgNumber
    for path in os.listdir(".\data"):
        for imagePath in paths.list_images(directory + str(path)):
            wantedImgPath = directory + str(path) + "\legelesebb.jpg"
            if imagePath == wantedImgPath:
                fileNames.append(imagePath)
                foundImgNumber += 1


def ShowingSharpestImg():
    global foundImgNumber
    columns = int(foundImgNumber / 5 + 1)
    rows = 5
    for i in range(1, columns * rows + 1):
        if i <= foundImgNumber:
            img = cv.imread(fileNames[i-1]) # range nem lehet 0 emaattt átugorja a 0-ás objektet
            fig.add_subplot(rows, columns, i)
            plt.imshow(img[:, :, ::-1])  # RGB-->BGR
    plt.show()

# FindingSharpestImgPath()
# ShowingSharpestImg()
