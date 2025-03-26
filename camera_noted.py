import sys
from cv2 import imshow, destroyAllWindows, waitKey
from numpy import asanyarray, array
import pyrealsense2 as rs



class RS():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 创建数据管道以配置摄像头并开启相机
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, 30)

        # 开始函数的返回值是用于打开设施的管道配置文件
        self.profile = self.pipeline.start(self.config)

        # 获取深度像素对应长度单位转换
        self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()

        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)
        self.frames = self.pipeline.wait_for_frames()
        self.aligned_frames = self.align.process(self.frames)

        # 跳过启动时的绿屏
        color_frame = self.frames.get_color_frame()
        color_image = asanyarray(color_frame.get_data())
        imshow('start', color_image)
        waitKey(500)
        destroyAllWindows()

    def get_img(self):
        """
        update the frame and align it, then get the depth and the RGB image
        :return: (depth, color)
        """
        self.frames = self.pipeline.wait_for_frames()
        self.aligned_frames = self.align.process(self.frames)
        depth_frame = self.aligned_frames.get_depth_frame()
        color_frame = self.aligned_frames.get_color_frame()

        depth_image = asanyarray(depth_frame.get_data())
        color_image = asanyarray(color_frame.get_data())

        return depth_image, color_image

    def get_coordinate(self, x, y):
        """
        :param x: target position in the cv coordinate system, in pixel
        :param y:
        :return:(x, y, z) in meters in the camera coordinate system
        """
        pc = rs.pointcloud()
        points = rs.points()
        pc.map_to(self.aligned_frames.get_color_frame())
        points = pc.calculate(self.aligned_frames.get_depth_frame())
        vtx = array(points.get_vertices())

        central_point = int(y) * self.width + int(x)
        return float(vtx[central_point][0]), float(vtx[central_point][1]), float(vtx[central_point][2])

    def stop(self):
        self.pipeline.stop()


if __name__ == '__main__':
    import cv2
    cam = RS(640, 480)
    depth_image, color_image = cam.get_img()
    cv2.imshow('depth', depth_image)
    cv2.imshow('color', color_image)
    cv2.waitKey(0)









