from PIL import Image


def rgb2grey(img):
    grey = img.convert('L')
    grey.save('C:/Users/admin/Pictures/新建文件夹/grey.png')


pic = Image.open(r'C:\Users\admin\Pictures\新建文件夹\wallhaven-x8lp7z_1920x1080.png')
rgb2grey(pic)
