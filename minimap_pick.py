import cv2
import numpy as np

img = cv2.imread("NTU_minimap.png")
cv2.imshow("Minimap", img)
cv2.waitKey(0)