from PIL import Image
import numpy as np


# RGB 到 YCbCr 转换函数
def rgb_to_ycbcr_pillow(img):
    pil_img = Image.fromarray(img, mode='RGB')
    ycbcr_img = pil_img.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_img)

    Y = ycbcr_array[..., 0]
    Cb = ycbcr_array[..., 1]
    Cr = ycbcr_array[..., 2]
    return Y, Cb, Cr


# YCbCr 到 RGB 转换函数，使用 PIL 内建转换
def ycbcr_to_rgb_pillow(Y, Cb, Cr):
    ycbcr_array = np.stack([Y, Cb, Cr], axis=-1)
    ycbcr_img = Image.fromarray(ycbcr_array, mode='YCbCr')
    rgb_img = ycbcr_img.convert('RGB')
    return np.array(rgb_img)


# 测试函数
if __name__ == '__main__':
    img = np.array(Image.open('../../dataset/rgb8bit/nightshot_iso_1600.ppm'))

    # RGB 到 YCbCr
    Y, Cb, Cr = rgb_to_ycbcr_pillow(img)

    Image.fromarray(Y).save('../data/ycbcr/Y_channel.png')
    Image.fromarray(Cb).save('../data/ycbcr/Cb_channel.png')
    Image.fromarray(Cr).save('../data/ycbcr/Cr_channel.png')
    print("YCbCr 转换完成（Pillow）")

    # YCbCr 到 RGB 使用 PIL 内建转换
    rgb_reconstructed = ycbcr_to_rgb_pillow(Y, Cb, Cr)

    Image.fromarray(rgb_reconstructed).save('../data/ycbcr/reconstructed_rgb_pillow.png')
    print("RGB 重建完成（Pillow）")
