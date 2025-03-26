import serial


class Gripper():
    def __init__(self):
        self.ser = serial.Serial("/dev/tty.usbmodem00000000050C1", 115200)

    def gripper_initial(self):  # 初始化
        self.ser.write('FFFEFDFC 01 0802 0100 00000000 FB'.encode())
        # 写入的命令总共有14字节，前4字节是帧头保持不变，第五位字节是夹爪ID默认为1，
        # 然后是功能标志2字节，前1字节表示主功能，后一字节表示主功能下划分的子功能。
        # 然后一字节的读写，01为写，00为读，之后一位为保留字00
        # 四字节的数据，最后1字节为帧尾。
        data = self.ser.read(42)
        print(data)
        # 设置主动反馈后返回FF FE FD FC 01 08 02 00 00 01 00 00 00 FB
        return

    def gripper_force(self, force):  # 设置夹持力，数值范围为20~100,，
        f = hex(force)
        e = f[2:4]
        s = 'FFFEFDFC0105020100' + e + '000000FB'
        self.ser.write(s.encode())
        return

    def gripper_position(self, positon):  # 设置夹爪的张开程度，数值范围0~100
        p = hex(positon)
        e = p[2:4]
        s = 'FFFEFDFC0106020100' + e + '000000FB'
        self.ser.write(s.encode())
        return


if __name__ == '__main__':
    g = Gripper()
    g.gripper_initial()
    # g.gripper_force(50)
    # g.gripper_position(20)



