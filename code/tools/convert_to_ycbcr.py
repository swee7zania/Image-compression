from PIL import Image
import numpy as np
from read_ppm import read_ppm, extract_raw_data


# RGB to YCbCr conversion function
def rgb_to_ycbcr(raw_file, width, height):
    # Read raw binary data
    with open(raw_file, 'rb') as file:
        raw_data = np.frombuffer(file.read(), dtype=np.uint8)

    # Reshape to (height, width, 3) for RGB format
    img = raw_data.reshape((height, width, 3))

    pil_img = Image.fromarray(img, mode='RGB')
    ycbcr_img = pil_img.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_img)

    Y = ycbcr_array[..., 0]
    Cb = ycbcr_array[..., 1]
    Cr = ycbcr_array[..., 2]

    print("RGB to YCbCr complete.")
    return Y, Cb, Cr


# YCbCr to RGB conversion function
def ycbcr_to_rgb(Y, Cb, Cr):
    ycbcr_array = np.stack([Y, Cb, Cr], axis=-1)
    ycbcr_img = Image.fromarray(ycbcr_array, mode='YCbCr')
    rgb_img = ycbcr_img.convert('RGB')

    print("YCbCr to RGB complete.")
    return np.array(rgb_img)


# TEST
if __name__ == '__main__':
    input_file = '../../dataset/rgb8bit/nightshot_iso_1600.ppm'
    raw_file = '../data/image.raw'

    # Read PPM and extract raw data
    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)
    extract_raw_data(input_file, binary_start, raw_file)

    # RGB to YCbCr
    Y, Cb, Cr = rgb_to_ycbcr(raw_file, width, height)

    Image.fromarray(Y).save('../data/ycbcr/Y_channel.png')
    Image.fromarray(Cb).save('../data/ycbcr/Cb_channel.png')
    Image.fromarray(Cr).save('../data/ycbcr/Cr_channel.png')
    print("YCbCr conversion is complete.")

    # YCbCr to RGB
    rgb_reconstructed = ycbcr_to_rgb(Y, Cb, Cr)

    Image.fromarray(rgb_reconstructed).save('../data/ycbcr/recover_rgb_pillow.png')
