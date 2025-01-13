from PIL import Image
from read_ppm import read_ppm, extract_raw_data
from convert_to_ycbcr import rgb_to_ycbcr, ycbcr_to_rgb
import numpy as np


def fmm_quantization(channel, modulus):
    print(f"FMM channel {channel[0][:5]}... quantization completed.")
    return (np.round(channel / modulus) * modulus).astype(np.uint8)


# TEST
if __name__ == '__main__':
    input_file = '../../dataset/rgb8bit/nightshot_iso_1600.ppm'
    raw_file = '../data/image.raw'

    # Read PPM and extract raw data
    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)
    extract_raw_data(input_file, binary_start, raw_file)

    Y, Cb, Cr = rgb_to_ycbcr(raw_file, width, height)

    # Perform FMM quantification on each channel
    Y_quant = fmm_quantization(Y, 3)  # 亮度通道
    Cb_quant = fmm_quantization(Cb, 10)  # 色度通道 Cb
    Cr_quant = fmm_quantization(Cr, 10)  # 色度通道 Cr

    # Save quantification results
    Image.fromarray(Y_quant).save('../data/fmm/Y_channel.png')
    Image.fromarray(Cb_quant).save('../data/fmm/Cb_channel.png')
    Image.fromarray(Cr_quant).save('../data/fmm/Cr_channel.png')

    # YCbCr to RGB
    rgb_reconstructed = ycbcr_to_rgb(Y_quant, Cb_quant, Cr_quant)

    Image.fromarray(rgb_reconstructed).save('../data/fmm/reconstructed_rgb_fmm.png')
