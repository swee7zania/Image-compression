from PIL import Image
from read_ppm import read_ppm
from convert_to_ycbcr import rgb_to_ycbcr_pillow, ycbcr_to_rgb_pillow
import numpy as np


def fmm_quantization(channel, modulus):
    return (np.round(channel / modulus) * modulus).astype(np.uint8)


if __name__ == '__main__':
    img = read_ppm('../../dataset/rgb8bit/nightshot_iso_1600.ppm')
    Y, Cb, Cr = rgb_to_ycbcr_pillow(img)

    # Perform FMM quantification on each channel
    Y_quant = fmm_quantization(Y, 3)  # 亮度通道
    Cb_quant = fmm_quantization(Cb, 10)  # 色度通道 Cb
    Cr_quant = fmm_quantization(Cr, 10)  # 色度通道 Cr

    # Save quantification results
    Image.fromarray(Y_quant).save('../data/fmm/Y_channel.png')
    Image.fromarray(Cb_quant).save('../data/fmm/Cb_channel.png')
    Image.fromarray(Cr_quant).save('../data/fmm/Cr_channel.png')
    print("FMM quantization completed.")

    # YCbCr to RGB
    rgb_reconstructed = ycbcr_to_rgb_pillow(Y_quant, Cb_quant, Cr_quant)

    Image.fromarray(rgb_reconstructed).save('../data/fmm/reconstructed_rgb_fmm.png')
    print("RGB recovery complete.")
