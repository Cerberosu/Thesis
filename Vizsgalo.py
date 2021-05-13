import matplotlib.pyplot as plt
import numpy as np
import cv2
import os


directory = os.getcwd() + "\Demos/SotetLila"
total_hue_hist = np.zeros((180,))
total_sat_hist = np.zeros((256,))
total_val_hist = np.zeros((256,))

img = cv2.imread("Demos/VilagosLila/tanito_3.jpg")
kernel = np.ones((5, 5), np.uint8)
blur = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
hsv_image = hsv

hue, sat, val = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]

hue_hist, bin_hue = np.histogram(hue, bins=range(181))
total_hue_hist += hue_hist

sat_hist, bin_sat = np.histogram(sat, bins=range(257))
total_sat_hist += sat_hist

val_hist, bin_val = np.histogram(val, bins=range(257))
total_val_hist += val_hist


def filter_values(values, v_min, v_max):
    flat = np.asanyarray(values).flatten()
    return flat[np.logical_and(flat >= v_min, flat < v_max)]


#filtered_hue = filter_values(hue, v_min=0, v_max=179)

filtered_mu = np.mean(sat)
filtered_std = np.std(sat)

print(filtered_mu, filtered_std)
#mu, std = norm.fit(val)
#print(mu, std)
#plt.bar(list(range(180)), total_hue_hist)
plt.bar(list(range(256)), total_sat_hist)
#plt.bar(list(range(256)), total_val_hist)
plt.show()
