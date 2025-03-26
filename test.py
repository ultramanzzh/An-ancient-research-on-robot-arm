import cv2
import camera
import Ursocket
import gripper
import numpy as np

obj_position = np.array([-0.00789639, 0.00366265, 0.2])
print(obj_position)
theta = 1.5

rv1 = np.array([0., 0., theta])
rm_obj2end = cv2.Rodrigues(rv1)[0]

tm_cam2end = np.array([[0.99770124, -0.06726973, -0.00818663, -0.02744465],
                       [0.06610884, 0.99272747, -0.10060715, -0.10060833],
                       [0.01489491, 0.09983467, 0.99489255, -0.15038112],
                       [0., 0., 0., 1.]])
tm_end2cam = np.linalg.inv(tm_cam2end)
shape = np.shape(tm_end2cam)
temp0 = []
for i in np.arange(shape[0]):
    for j in np.arange(shape[1]):
        if i < 3 and j < 3:
            temp0.append(tm_end2cam[i, j])
rm_end2cam = np.array(temp0)
rm_end2cam.resize((3, 3))

rm_obj2cam = rm_end2cam @ rm_obj2end

temp1 = rm_obj2cam.flatten()
temp2 = temp1.tolist()
temp2.insert(3, obj_position[0])
temp2.insert(7, obj_position[1])
temp2.insert(11, obj_position[2])
for i in np.arange(3):
    temp2.append(0)
temp2.append(1)
tm_obj2cam = np.array(temp2)
tm_obj2cam.resize((4, 4))

tm_obj2end = tm_cam2end @ tm_obj2cam

Ur = Ursocket.UrSocket()
end_position = np.array(Ur.get_pose())

rv2 = np.array(end_position[3:6])
rm_end2base = cv2.Rodrigues(rv2)[0]
temp3 = rm_end2base.flatten()
temp4 = temp3.tolist()
temp4.insert(3, end_position[0])
temp4.insert(7, end_position[1])
temp4.insert(11, end_position[2])
for i in np.arange(3):
    temp4.append(0)
temp4.append(1)
tm_end2base = np.array(temp4)
tm_end2base.resize((4, 4))

rm_obj2base = rm_end2base @ rm_obj2end

pv_obj2end = np.array([tm_obj2end[0][3], tm_obj2end[1][3], tm_obj2end[2][3], 1])
pv_obj2end.resize((4, 1))
pv_obj2base = tm_end2base @ pv_obj2end

rv_f = cv2.Rodrigues(rm_obj2base)[0]
newPose = np.array([pv_obj2base[0][0], pv_obj2base[1][0], pv_obj2base[2][0], rv_f[0][0], rv_f[1][0], rv_f[2][0]])
print(end_position, type(end_position))
print(newPose, type(newPose))
Ur.change_pose(newPose)
Ur.send()
Ur.doSocket.close()