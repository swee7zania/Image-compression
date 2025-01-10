import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tools.read_ppm import read_ppm
from tools.fmm_quantization import fmm_quantization
from tools.convert_to_ycbcr import rgb_to_ycbcr_pillow


def rle_compress(channel):
    """
    对图像通道进行 RLE 压缩。

    Args:
        channel (np.ndarray): 输入图像通道数据。

    Returns:
        list: 压缩后的数据，包含值和连续次数。
    """
    flat_channel = channel.flatten()  # 扁平化图像数据
    compressed = []
    count = 1
    for i in range(1, len(flat_channel)):
        if flat_channel[i] == flat_channel[i - 1]:
            count += 1
        else:
            compressed.append((flat_channel[i - 1], count))
            count = 1
    compressed.append((flat_channel[-1], count))  # 添加最后的值
    return compressed


def save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y_shape, filename):
    """
    使用 NumPy 压缩格式保存压缩数据。

    Args:
        Y_compressed (list): Y 通道的压缩数据。
        Cb_compressed (list): Cb 通道的压缩数据。
        Cr_compressed (list): Cr 通道的压缩数据。
        Y_shape (tuple): 图像的尺寸 (height, width)。
        filename (str): 输出文件路径。
    """
    # 将压缩数据和图像尺寸保存为 .npz 格式
    np.savez_compressed(filename, Y=Y_compressed, Cb=Cb_compressed, Cr=Cr_compressed, shape=Y_shape)


# 测试函数
if __name__ == '__main__':
    img = read_ppm('../dataset/rgb8bit/nightshot_iso_1600.ppm')
    Y, Cb, Cr = rgb_to_ycbcr_pillow(img)

    # 对各通道进行 FMM 量化
    Y_quant = fmm_quantization(Y, 4)  # 对亮度通道，模数为 3
    Cb_quant = fmm_quantization(Cb, 7)  # 对色度通道 Cb，模数为 7
    Cr_quant = fmm_quantization(Cr, 7)  # 对色度通道 Cr，模数为 7

    # 对各通道进行 RLE 压缩
    Y_compressed = rle_compress(Y_quant)
    Cb_compressed = rle_compress(Cb_quant)
    Cr_compressed = rle_compress(Cr_quant)

    # 保存为 .npz 格式，并保存图像尺寸信息
    save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y.shape, 'data/compressed_data.npz')
    print("压缩数据已保存为 .npz 格式")
