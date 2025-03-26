import cv2
import camera
import Ursocket
import gripper
import numpy as np
import grasping
import scan
import time

pose0 = np.array([-0.18603966, -0.10870721, 0.37465309, 2.15071847, 2.20156684, 0.16325944])
g = gripper.Gripper()
g.gripper_initial()
cam = camera.RS(640, 480)
depth_image, color_image = cam.get_img()
cv2.imshow('depth', depth_image)
cv2.imshow('color', color_image)
cv2.waitKey(0)

scan = scan.Scan(color_image)
point = np.array(scan.back())
x = point[0]
y = point[1]
z = point[2]
theta = point[3]
grasp = grasping.Grasping(x, y, z, theta)
pose1 = grasp.back()


Ur = Ursocket.UrSocket()
Ur.change_pose(pose0)
time.sleep(10)
ini_position = np.array(Ur.get_pose())
Ur.change_pose(pose1)
Ur.send()
time.sleep(10)
pose2 = ini_position
Ur.change_pose(pose2)
Ur.send()
time.sleep(10)
pose3 = pose2
pose3[2] = pose1[2]
Ur.change_pose(pose3)
Ur.send()


# g.gripper_force(50)
g.gripper_position(20)
Ur.doSocket.close()

