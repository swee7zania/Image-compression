import cv2
import numpy as np
from read_ppm import read_ppm


def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

def print_psnr(input_file,original_img_path,compressed_img_path):
    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)

    # Read the original image and the decompressed image
    original_img = np.fromfile(original_img_path, dtype=np.uint8).reshape((height, width, 3))
    compressed_img = cv2.imread(compressed_img_path, cv2.IMREAD_COLOR)

    # Calculating PSNR
    psnr_value = calculate_psnr(original_img, compressed_img)
    print(f"PSNR: {psnr_value} dB")


if __name__ == '__main__':
    input_file = '../../dataset/rgb8bit/flower_foveon.ppm'
    original_img_path = '../data/image.raw'
    compressed_img_path = '../data/restored_image.png'

    print_psnr(input_file,original_img_path,compressed_img_path)