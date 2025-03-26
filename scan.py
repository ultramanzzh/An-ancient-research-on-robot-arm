import cv2
import numpy as np
from camera import RS
cam = RS(640, 480)
# depth_image, color_image = cam.get_img()
# cv2.imshow('depth', depth_image)
# cv2.imshow('color', color_image)
# cv2.waitKey(0)


class Scan:
    def __init__(self, img):
        self.img = img
# 读取图片
#        self.img = cv2.imread(self.img, 1)
# 高斯滤波
        self.dst = cv2.GaussianBlur(self.img, (5, 5), 1.5)
# 灰度处理
        self.gray = cv2.cvtColor(self.dst, cv2.COLOR_BGR2GRAY)
# 反二值化
        self.ret, self.binary = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)
#       print("threshold value %s" % self.ret)
#       cv2.imshow('threshold', self.binary)
# 开运算操作
        self.kernel = np.ones((6, 6), np.uint8)
        self.opening = cv2.morphologyEx(self.binary, cv2.MORPH_OPEN, self.kernel, iterations=6)  # iterations进行6次操作
# 轮廓拟合
        contours, hierarchy = cv2.findContours(self.opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]  # 得到第一个的轮廓
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(self.img, [box], 0, (0, 0, 255), 3)  # 画矩形框

        # 图像轮廓及中心点坐标
        m = cv2.moments(cnt)  # 计算第一条轮廓的各阶矩,字典形式
        self.center_x = int(m['m10'] / m['m00'])
        self.center_y = int(m['m01'] / m['m00'])
        cv2.circle(self.img, (self.center_x, self.center_y), 7, 128, -1)  # 绘制中心点
        str1 = '(' + str(self.center_x) + ',' + str(self.center_y) + ')'  # 把坐标转化为字符串
        cv2.putText(self.img, str1, (self.center_x - 50, self.center_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 0), 2, cv2.LINE_AA)  # 绘制坐标点位
        rect = cv2.minAreaRect(contours[0])
        self.theta = rect[2]
        cv2.imshow('open', self.opening)
        cv2.imshow('show', self.img)
        cv2.waitKey(0)
    #       print("返回值rect:\n", rect)
        self.x, self.y, self.z = RS.get_coordinate(cam, self.center_x, self.center_y)

    def back(self):
        return self.x, self.y, self.z, self.theta


if __name__ == '__main__':
    cam = RS(640,480)
    depth_image, color_image = cam.get_img()
    scan = Scan(color_image)
    x, y, z, theta = scan.back()
    print('center_x:', x)
    print('center_y:', y)
    print('angle:', theta)
