import numpy as np
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tools.read_ppm import read_ppm, extract_raw_data
from tools.fmm_quantization import fmm_quantization
from tools.convert_to_ycbcr import rgb_to_ycbcr
from tools.entropy_calculation import calculate_entropy


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


def compress_data(input_file, raw_file):
    # Calculation program time
    start_time = time.time()

    # Read PPM and extract raw data
    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)
    extract_raw_data(input_file, binary_start, raw_file)

    calculate_entropy(raw_file)

    Y, Cb, Cr = rgb_to_ycbcr(raw_file, width, height)

    # Perform FMM quantification on each channel
    Y_quant = fmm_quantization(Y, 4)  # 亮度通道 Y
    Cb_quant = fmm_quantization(Cb, 8)  # 色度通道 Cb
    Cr_quant = fmm_quantization(Cr, 8)  # 色度通道 Cr

    # RLE compression for each channel
    Y_compressed = rle_compress(Y_quant)
    Cb_compressed = rle_compress(Cb_quant)
    Cr_compressed = rle_compress(Cr_quant)

    # Save compression value and image shape info as binary
    save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y.shape, 'data/compressed_data.npz')
    print("Compressed data is saved: data/compressed_data.npz")

    end_time = time.time()
    print(f"\nTotal Compression Time: {end_time - start_time:.2f} seconds")


def save_compressed_data_npz(Y_compressed, Cb_compressed, Cr_compressed, Y_shape, filename):
    np.savez_compressed(filename, Y=Y_compressed, Cb=Cb_compressed, Cr=Cr_compressed, shape=Y_shape)


def calculate_limit(raw_file):
    original_size = os.path.getsize(raw_file)
    compressed_size = os.path.getsize('data/compressed_data.npz')

    compression_ratio = (compressed_size / original_size) * 100

    bandwidth = 10 * 10 ** 6  # 10 Mbps in bits per second
    transmission_time = (compressed_size * 8) / bandwidth

    print(f"\nOriginal File Size: {original_size / 1024:.2f} KB")
    print(f"Compressed File Size: {compressed_size / 1024:.2f} KB")
    print(f"Compression Ratio: {100 - compression_ratio:.2f}%")
    print(f"Estimated Transmission Time: {transmission_time:.2f} seconds")


if __name__ == '__main__':
    # Change to the image path that needs to be compressed
    input_file = '../dataset/rgb8bit/flower_foveon.ppm'
    raw_file = 'data/image.raw'

    compress_data(input_file, raw_file)
    calculate_limit(raw_file)
