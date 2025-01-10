import numpy as np


def print_ppm(filename):
    with open(filename, 'rb') as f:
        f.readline()
        dimensions = f.readline().decode().strip()
        width, height = map(int, dimensions.split())
        max_color = int(f.readline().decode().strip())
        dtype = np.uint8 if max_color < 256 else np.uint16
        pixel_data = np.frombuffer(f.read(), dtype=dtype)
    return width, height, max_color, pixel_data


def read_ppm(file_path):
    with open(file_path, 'rb') as f:
        f.readline()
        dimensions = f.readline().decode().strip()
        width, height = map(int, dimensions.split())
        max_color = int(f.readline().decode().strip())
        dtype = np.uint8 if max_color < 256 else np.uint16
        img_data = np.fromfile(f, dtype=dtype)
        img = img_data.reshape((height, width, 3))
        return img


if __name__ == "__main__":
    input_file = '../../dataset/rgb8bit/nightshot_iso_1600.ppm'

    print(print_ppm(input_file))
    print()
    print(read_ppm(input_file))
