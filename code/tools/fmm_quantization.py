from PIL import Image
from read_ppm import read_ppm
from convert_to_ycbcr import rgb_to_ycbcr_pillow, ycbcr_to_rgb_pillow
import numpy as np


def fmm_quantization(channel, modulus):
    """
    对图像通道进行 FMM 量化（模运算）。

    Args:
        channel (np.ndarray): 输入图像通道数据。
        modulus (int): 模数，控制量化程度。

    Returns:
        np.ndarray: 量化后的通道数据。
    """
    return (np.round(channel / modulus) * modulus).astype(np.uint8)


# 测试函数
if __name__ == '__main__':
    # 读取 ppm 图像并转换为 YCbCr
    img = read_ppm('../../dataset/rgb8bit/nightshot_iso_1600.ppm')
    Y, Cb, Cr = rgb_to_ycbcr_pillow(img)

    # 对各通道进行 FMM 量化
    Y_quant = fmm_quantization(Y, 3)  # 对亮度通道
    Cb_quant = fmm_quantization(Cb, 10)  # 对色度通道 Cb
    Cr_quant = fmm_quantization(Cr, 10)  # 对色度通道 Cr

    # 保存量化结果
    Image.fromarray(Y_quant).save('../data/fmm/Y_channel.png')
    Image.fromarray(Cb_quant).save('../data/fmm/Cb_channel.png')
    Image.fromarray(Cr_quant).save('../data/fmm/Cr_channel.png')
    print("FMM 量化完成并保存为 PNG 文件")

    # YCbCr 到 RGB 使用 PIL 内建转换
    rgb_reconstructed = ycbcr_to_rgb_pillow(Y_quant, Cb_quant, Cr_quant)

    Image.fromarray(rgb_reconstructed).save('../data/fmm/reconstructed_rgb_fmm.png')
    print("RGB 重建完成（Pillow）")
