import numpy as np
import cv2

tm_cam2end = np.array([[0.99770124, -0.06726973, -0.00818663, -0.02744465],
                       [0.06610884, 0.99272747, -0.10060715, -0.10060833],
                       [0.01489491, 0.09983467, 0.99489255, -0.15038112],
                       [0., 0., 0., 1.]])
# tm_end2cam = np.linalg.inv(tm_cam2end)


tm_end2cam = np.array([[0.99770124, 0.06610884, 0.01489491, 0.03627257],
                       [-0.06726973, 0.99272746, 0.09983467, 0.11304371],
                       [-0.00818663, -0.10060715, 0.99489254, 0.13926646],
                       [0., 0., 0., 1.]])

rm_obj2end = np.array([[1., 0., 0.],
                       [0., 1., 0.],
                       [0., 0., 1.]])

rm_end2cam = np.array([[0.99770124, 0.06610884, 0.01489491],
                       [-0.06726973, 0.99272746, 0.09983467],
                       [-0.00818663, -0.10060715, 0.99489254]])

rm_obj2cam = rm_end2cam @ rm_obj2end

tm_obj2cam = np.array([[0.99770124, 0.06610884, 0.01489491, -0.00789639],
                       [-0.06726973, 0.99272746, 0.09983467, 0.00366265],
                       [-0.00818663, -0.10060715, 0.99489254, 0.2],
                       [0., 0., 0., 1.]])

tm_obj2end = tm_cam2end @ tm_obj2cam
print(tm_obj2end)

end_position = np.array([-0.42845176, -0.23693528, 0.37647894, 2.06404853, 2.32751964, 0.04782686])

pv = np.array([[-3.72065996e-02],
               [-1.17615768e-01],
               [4.88454334e-02],
               [1.00000000e+00]])

rm_end2base = np.array([[-0.11950968, 0.99189792, 0.04308066],
                        [0.99283038, 0.11949722, 0.00287368],
                        [-0.00229762, 0.04311522, -0.99906746]])

tm_end2base = np.array([[-0.11950968, 0.99189792, 0.04308066, -0.42845176],
                        [0.99283038, 0.11949722, 0.00287368, -0.23693528],
                        [-0.00229762, 0.04311522, -0.99906746, 0.37647894],
                        [0., 0., 0., 1.]])

pv_obj2base = tm_end2base @ pv
print(pv_obj2base)
rm_obj2base = rm_end2base @ rm_obj2end

rv = cv2.Rodrigues(rm_obj2base)[0]
print(rv)