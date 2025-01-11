import numpy as np
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tools.convert_to_ycbcr import ycbcr_to_rgb


def rle_decompress(compressed_data, shape):
    decompressed = np.zeros(shape, dtype=np.uint8)
    idx = 0

    for value, count in compressed_data:
        end_idx = idx + count
        decompressed.ravel()[idx:end_idx] = value
        idx = end_idx

    return decompressed


def restore_image(npz_file):
    data = np.load(npz_file)
    Y_compressed = data['Y']
    Cb_compressed = data['Cb']
    Cr_compressed = data['Cr']
    height, width = data['shape']

    # Decompressing RLE Data
    Y = rle_decompress(Y_compressed, (height, width))
    Cb = rle_decompress(Cb_compressed, (height, width))
    Cr = rle_decompress(Cr_compressed, (height, width))

    # Convert YCbCr to RGB
    rgb = ycbcr_to_rgb(Y, Cb, Cr)

    # Save the recovered image
    Image.fromarray(rgb).save('data/restored_image.png')
    print("Image recovery completed and saved: data/restored_image.png")


if __name__ == '__main__':
    # The path can be kept unchanged
    restore_image('data/compressed_data.npz')
