import cv2
import numpy as np
from read_ppm import read_ppm
from skimage.metrics import structural_similarity as ssim


def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr


def calculate_ssim(img1, img2):
    # 转换为灰度图以计算 SSIM
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ssim_value, _ = ssim(img1_gray, img2_gray, full=True)
    return ssim_value


def print_ssim(input_file, original_img_path, compressed_img_path):
    # 读取图像
    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)
    original_img = np.fromfile(original_img_path, dtype=np.uint8).reshape((height, width, 3))
    compressed_img = cv2.imread(compressed_img_path, cv2.IMREAD_COLOR)

    # 计算 SSIM
    ssim_value = calculate_ssim(original_img, compressed_img)
    print(f"SSIM: {ssim_value}")


def print_psnr(input_file, original_img_path, compressed_img_path):
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

    print_psnr(input_file, original_img_path, compressed_img_path)
    print_ssim(input_file, original_img_path, compressed_img_path)
