import cv2 as cv

image = cv.imread("./SotetLila/tanito_7.jpg")

originalGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
orignalLapimage = cv.Laplacian(originalGray, cv.CV_64F)
originalLap = cv.Laplacian(originalGray, cv.CV_64F).var()
print(originalLap)

blur = cv.GaussianBlur(image, (3, 3), 0)
blurGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
blurLapimage = cv.Laplacian(blurGray, cv.CV_64F)
blurLap = cv.Laplacian(blurLapimage, cv.CV_64F).var()

print(blurLap)
cv.imshow("Eredeti", image)
cv.imshow("OriginalLap", originalGray)
#cv.imshow("Laplacian", orignalLapimage)
#cv.imshow("Laplacian2", blurLapimage)
cv.imshow("BlurLap", blurGray)

cv.waitKey(100000)