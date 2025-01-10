import numpy as np
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tools.convert_to_ycbcr import ycbcr_to_rgb_pillow


def rle_decompress(compressed_data, shape):
    # 创建一个形状为 `shape` 的空数组来存放解压后的数据
    decompressed = np.zeros(shape, dtype=np.uint8)

    # 初始化当前索引
    idx = 0

    for value, count in compressed_data:
        # 对每个压缩数据 (value, count)，将其解压到指定的位置
        end_idx = idx + count

        # 将压缩数据填充到解压数组中
        decompressed.ravel()[idx:end_idx] = value

        # 更新索引
        idx = end_idx

    return decompressed


def restore_image_from_npz(npz_filename):
    # 加载 .npz 文件
    data = np.load(npz_filename)

    # 获取解压后的数据
    Y_compressed = data['Y']
    Cb_compressed = data['Cb']
    Cr_compressed = data['Cr']
    height, width = data['shape']

    # 解压 RLE 数据
    Y = rle_decompress(Y_compressed, (height, width))
    Cb = rle_decompress(Cb_compressed, (height, width))
    Cr = rle_decompress(Cr_compressed, (height, width))

    # 将 YCbCr 转换为 RGB
    rgb = ycbcr_to_rgb_pillow(Y, Cb, Cr)

    # 保存恢复的图像
    Image.fromarray(rgb).save('data/restored_image.png')
    print("图像恢复完成，已保存")


# 示例代码
if __name__ == '__main__':
    restore_image_from_npz('data/compressed_data.npz')
