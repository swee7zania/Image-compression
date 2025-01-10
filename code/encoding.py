import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tools.read_ppm import read_ppm
from tools.fmm_quantization import fmm_quantization
from tools.convert_to_ycbcr import rgb_to_ycbcr_pillow


def rle_compress(channel):
    flat_channel = channel.flatten()
    compressed = []
    count = 1
    for i in range(1, len(flat_channel)):
        if flat_channel[i] == flat_channel[i - 1]:
            count += 1
        else:
            compressed.append((flat_channel[i - 1], count))
            count = 1
    compressed.append((flat_channel[-1], count))
    return compressed


def save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y_shape, filename):
    np.savez_compressed(filename, Y=Y_compressed, Cb=Cb_compressed, Cr=Cr_compressed, shape=Y_shape)


if __name__ == '__main__':
    img = read_ppm('../dataset/rgb8bit/nightshot_iso_1600.ppm')
    Y, Cb, Cr = rgb_to_ycbcr_pillow(img)

    # Perform FMM quantification on each channel
    Y_quant = fmm_quantization(Y, 4)  # 亮度通道 Y
    Cb_quant = fmm_quantization(Cb, 7)  # 色度通道 Cb
    Cr_quant = fmm_quantization(Cr, 7)  # 色度通道 Cr

    # RLE compression for each channel
    Y_compressed = rle_compress(Y_quant)
    Cb_compressed = rle_compress(Cb_quant)
    Cr_compressed = rle_compress(Cr_quant)

    # Save compression value and image shape info as binary
    save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y.shape, 'data/compressed_data.npz')
    print("Compressed data is saved in .npz format")
