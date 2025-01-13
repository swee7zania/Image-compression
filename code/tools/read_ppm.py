import numpy as np


def read_ppm(file_path):
    with open(file_path, 'rb') as file:
        header = []
        while len(header) < 3:
            line = file.readline().decode('ascii').strip()
            if line and not line.startswith('#'):  # 跳过注释行
                header.append(line)

        magic_number = header[0]
        dimensions = header[1]
        max_value = header[2]

        channels = 3 if magic_number == 'P6' else 1
        width, height = map(int, dimensions.split())
        max_color = int(max_value)
        binary_start = file.tell()  # 记录像素数据的开始位置

        print(f'width:{width}, height:{height}, channels:{channels}')
        return magic_number, channels, width, height, max_color, binary_start


def extract_raw_data(file_path, binary_start, output_path):
    with open(file_path, 'rb') as file:
        file.seek(binary_start)
        raw_data = file.read()

        with open(output_path, 'wb') as raw_file:
            raw_file.write(raw_data)
            print('Extract successfully saved: data/image.raw')


if __name__ == "__main__":
    input_file = '../../dataset/rgb8bit/nightshot_iso_1600.ppm'
    output_file = '../data/image.raw'

    magic_number, channels, width, height, max_color, binary_start = read_ppm(input_file)
    extract_raw_data(input_file, binary_start, output_file)
