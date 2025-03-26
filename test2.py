import camera
import cv2

cam = camera.RS(640, 480)
depth_image, color_image = cam.get_img()
cv2.waitKey(1000)
depth_image, color_image = cam.get_img()

cv2.imshow('depth', depth_image)
cv2.imshow('color', color_image)
cv2.waitKey(0)

