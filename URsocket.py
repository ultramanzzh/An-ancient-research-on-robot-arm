import socket
import struct
import numpy as np


class UrSocket(object):
    def __init__(self, HOST="10.110.52.88", PORT=30003):
        self.HOST = HOST
        self.PORT = PORT
        self.doSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.data = bytes(self.doSocket.recv(1200))
        self.pose = self.get_pose()

    def connect(self):
       """
       connect your PC to the UR
       :return:
       """

       self.doSocket.connect((self.HOST, self.PORT))

    def receive(self):
        """
         receive current data of the position and pose of the TCP
        :return:  the data is saved in self.data, and the data is in the format of bytes
        """
        self.data = bytes(self.doSocket.recv(1200))

    def get_pose(self):
        """
        decode the data message, and get the current x, y, z, rx, ry, rz, the last three is the Rotating vector
        :return: x, y, z, rx, ry, rz
        """
        x, y, z = struct.unpack('!ddd', self.data[444:468])
        rx, ry, rz = struct.unpack('!ddd', self.data[468:492])
        return x, y, z, rx, ry, rz

    def change_pose(self, newPose):
        """

        :param newPose: [x, y, z, rx, ry, rz]
        :return:
        """
        self.pose = tuple(newPose)

    def send(self, a=0.05, v=0.3, pattern='p'):
        """
        :param a: Acceleration
        :param v: Velocity
        :param pattern: the moving pattern, 'p' or 'l'
        :return: send the pose in class to the UR
        """
        if not(pattern == 'p' or pattern == 'l'):
            print('the pattern is not supported')
            return
        pose = self.pose
        pose = str(pose).replace('(', '').replace(')', '')
        message = 'move' + pattern + '(p[' + pose +'],a=' + str(a) + ',v=' +str(v) +')'+'\n'
        print(message)
        self.doSocket.sendall(message.encode())

    # def get_rotation_mat(self):
    #     """
    #     from the current pose, get the rotation vec and trans it to the rotation mat (3*3)
    #     :return: rotation mat (3*3)
    #     """
    #     rotation_vec = np.expand_dims(np.array(self.pose[3:6]), 0)
    #     theta = np.linalg.norm(rotation_vec, 2)
    #     out_operator = np.array([
    #         [0, -theta[2], theta[1]],
    #         [theta[2], 0, -theta[0]],
    #         [-theta[1], theta[0], 0]
    #     ])
    #     rotation_mat = np.cos(theta)*np.eye(3) + (1 - np.cos(theta))*theta.T.dot(theta) + np.sin(theta)*out_operator
    #     return rotation_mat


if __name__ == '__main__':
    def main():
        Ur = UrSocket()
        pose = np.array(Ur.get_pose())
        print(pose)
        pose += np.array([0, 0.1, 0, 0, 0, 0])
        Ur.change_pose(pose)
        Ur.send()
        Ur.doSocket.close()

    main()









