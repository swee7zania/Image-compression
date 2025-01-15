# **Image Transmission for Intelligent Mobile Devices**

With the proliferation of smart mobile devices such as smartphones, drones, and dashcams, these devices frequently capture high-resolution images or videos. However, the constraints of storage capacity and network bandwidth—especially in real-time transmission scenarios—necessitate efficient compression methods. This project introduces an **image compression algorithm** inspired by **perceptual coding**, which leverages the characteristics of human visual perception to achieve **visually lossless** yet highly efficient compression.

Perceptual coding exploits the non-uniform sensitivity of the human visual system to different spatial frequencies, allowing for the selective preservation of critical details while discarding less perceptible information. To implement this, I utilize **FMM quantization** to achieve controllable lossy compression by assigning different modulus, effectively reducing data size without noticeable quality degradation. This approach ensures that visually significant details, such as edges and high-frequency components, are preserved, while low-sensitivity regions are compressed more aggressively.

In addition, **entropy coding**—specifically **Run-Length Encoding (RLE)**—is employed to further enhance compression efficiency. After FMM quantization, the redundancy in low-frequency regions of the chrominance channels creates long sequences of repeated values, making RLE particularly effective. The combination of FMM and RLE not only reduces data size but also simplifies the encoding and decoding processes, making the algorithm suitable for real-time applications in resource-constrained devices like drones.

### **1. Scenario Description**

Assume a practical application scenario: a wildlife protection monitoring system, in which multiple drones are used to capture images of wildlife and transmit them to a central monitoring station in real time. The system has the following constraints:

- **Image resolution requirements:** Since wildlife live in a wide area, using larger pictures facilitates better observation of wildlife. Therefore, in the original data set of the project, each image is at least 1920×1080.
- **Network bandwidth limitations:** Assume that drones in some areas still transmit data through 4G networks with an average bandwidth of 5 Mbps.
- **Transmission delay requirements:** For real-time monitoring, the transmission time of each image must not exceed 2 seconds.
- **Storage space limitations:** Drones have limited local storage capacity, so high compression rates allow drones to save more data and keep them working longer.
- **Quality requirements:** In order not to affect the observation of animal researchers, we should retain the important information of the image to the greatest extent possible. Therefore, the PSNR (peak signal-to-noise ratio) of the decompressed image at least 30 dB.

Given these constraints, efficient image compression is essential to reduce data size while ensuring visual quality and meeting transmission and storage requirements. Specifically, the compression algorithm must achieve:

- A compressed bit rate of **2 Mbps** or lower.
- A compression ratio of at least **50%**, e.g., reducing the size of a 3 MB image to 1200 KB or less.

### 2. Core Concept

#### 2.1 Human Visual Perception

Perceptual coding aims to compress image data while ensuring that the reconstructed images appear visually identical to the original ones. By taking advantage of the human eye's varying sensitivity to different frequencies, compression algorithms can discard more information in less sensitive regions while retaining higher fidelity in critical areas. Sensitivity of human eyes varies across different image regions:
- Highly sensitive to luminance (`Y` channel) changes, especially edges and high-frequency details.
- Less sensitive to chrominance (`Cb` and `Cr` channels) changes, particularly in low-frequency regions.

#### 2.2 FMM Application

The Five Modulus Method (FMM) leverages human visual perception to achieve efficient compression while maintaining perceived image quality:

- Smaller moduli are applied to the luminance channel (`Y`) to preserve critical visual details.
- Larger moduli are used for the chrominance channels (`Cb` and `Cr`), reducing data volume significantly without noticeable quality degradation.

#### 2.3 Controllable Lossy Compression

FMM enables flexible control over the compression ratio and visual quality. By dynamically adjusting modulus values for each channel, the compression pipeline can meet diverse application requirements. For example:

- High-quality mode: Smaller moduli are used for all channels to minimize distortion.
- Bandwidth-saving mode: Larger moduli are applied to `Cb` and `Cr`, while a moderately larger modulus is used for `Y` to achieve higher compression rates without compromising overall image clarity.

#### 2.4 Run-Length Encoding (RLE)

RLE is a straightforward algorithm that is computationally efficient, making it ideal for real-time applications like image transmission in drones or mobile devices. It requires minimal computational resources compared to more complex methods like Huffman or arithmetic coding.

- **Cooperate with FMM**: After FMM quantization, low-frequency regions in `Cb` and `Cr` channels often contain long runs of identical values, perfectly suited for RLE. This synergy allows RLE to efficiently compress repetitive data, significantly reducing file size.
- **Simplified Decoding Process**: Unlike complex lossy compression algorithms such as JPEG or HEVC, the combined FMM+RLE approach requires lower computational resources for decoding. This makes it ideal for embedded systems or real-time transmission scenarios.
- **Low Computational Complexity**: Compared to more complex methods like Huffman or arithmetic coding, RLE is lightweight and fast, making it suitable for real-time applications on resource-constrained devices.

### 3. Detailed Design

#### 3.1 Encoding Pipeline

1. Reading and extraction:
   - Read `.ppm` image data, extract binary data from the `.ppm` file, remove the header, and convert to `.raw` format for entropy calculation.
   - Calculate the entropy of the original `.raw` image as a measure of data complexity.
2. Preprocessing:
   - Read `.raw` image data, including luminance channel `Y` and chrominance channels `Cb` and `Cr`.
   - Convert to `YCbCr` color space, separating luminance and chrominance channels.
3. FMM Quantization:
   - Luminance channel `Y`: Modulus temporarily set to 4 to retain more visually important details.
   - Chrominance channels `Cb` and `Cr`: Modulus temporarily set to 7 to further reduce storage and transmission data.
   - FMM quantization parameters can be dynamically adjusted based on image complexity.
4. Entropy Coding:
   - Compress quantized values further using entropy coding.
   - Use **RLE (Run-Length Encoding)** to effectively compress repetitive data segments.
5. Packaging Compressed File:
   - Save RLE-encoded data as a binary file, storing relevant data.

#### 3.2 Decoding Pipeline

1. Reading and Decoding:
   - Extract entropy-coded data from the compressed file.
   - Decode `Y`, `Cb`, and `Cr` channels using RLE to restore quantized data.
2. Inverse Color Space Conversion:
   - Convert restored `YCbCr` data back to RGB color space.
3. Output Image:
   - Generate the decompressed image and save it in a common format.

### 4. Compression Results

#### 4.1 Extract raw data

In the case of `cathedral.ppm`, I removed the header data and kept only the original binary image data.

<img src="D:\0. Data Transmittion\Image Compression\assets\image-20250115151448756.png" alt="image-20250115151448756" style="zoom:33%;" />

#### 4.2 Quantization and Entropy

In the case of `nightshot_iso_1600.ppm`, I calculated the original entropy and the entropy after FMM quantization.

| Raw Entropy | Entropy After FMM Quantization                               |
| ----------- | ------------------------------------------------------------ |
| 15.46 bits  | `Y` channel: 4.94 bits; `Cb` channel:2.33 bits; `Cr` channel:1.66 bits |

The `Y` channel modulus is 3, and the `Cb` and `Cr` channel modulus is 10. It can be seen that the entropy of the original image is higher and the compression space is smaller. After FMM quantization, the entropy value is significantly smaller, and there is more room for compression. 

This shows that FMM quantization plays a very good role. The higher the modulus, the lower the entropy value.

#### 4.3 Before and After

The comparison between the original and compressed images is as follows:

| Original Image                                               | Decompress Image                                             | FMM modulus       | Compression Ratio | PSNR     | SSIM   |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- | ----------------- | -------- | ------ |
| `nightshot_iso_1600.raw` (21609KB)                           | `compressed_data.npz` (8651 KB)                              | Y:3;  Cb:9; Cr:9  | ≈ 60%             | ≈30.02dB | ≈0.951 |
| <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250110181253164.png" alt="image-20250110181253164"/> | ![image-20250110181316824](D:\0. Data Transmittion\Image Compression\assets\image-20250110181316824.png) |                   |                   |          |        |
| `flower_foveon.raw` (10047KB)                                | `compressed_data.npz` (1481 KB)                              | Y:2; Cb:10; Cr:10 | ≈ 85%             | ≈31.16dB | ≈0.985 |
| `cathedral.raw`（17625KB)                                    | `compressed_data.npz` (5978 KB)                              | Y:1; Cb:10; Cr:10 | ≈ 66%             | ≈30.81dB | ≈0.978 |

From the compression results, we can see that we can flexibly adjust the modulus according to the characteristics of the image. The **compression rate** is as high as **over 60%**, and the compressed image is perceived the same by the human eye.

A high **Peak Signal-to-Noise Ratio (PSNR)** value of **>30 dB** indicates good image quality, suitable for storage or transmission, and has little effect on the human eye. It indicate that the adopted FMM+RLE method has achieved a good balance between compression efficiency and image quality.

The **Structural Similarity Index Measure (SSIM)** ranges from [0, 1]. The closer the value is to 1, the more similar the two images are. The SSIM range of these compressed images is basically **0.95 ~ 0.99**, which means that the images are almost lossless and the quality after compression is very close to the original image.

------

# Functional Modules

## Image Reading Tool

### 1. Read `.ppm`

- **Function**: `read_ppm`

  - Reads PPM files and returns reconstructed image arrays.

- **Parameters**:

  - `file_path`: String, path to the PPM file.

- **Returns**:

  - `img`: 3D NumPy array representing the RGB image, with shape `(height, width, 3)`.
  - `magic_number`: Identifier of the PPM file type (`P6` for binary RGB, `P5` for grayscale).
  - `channels`: Number of color channels (3 for RGB, 1 for grayscale).
  - `width`: Width of the image in pixels.
  - `height`: Height of the image in pixels.
  - `max_color`: Maximum color value (usually 255 for 8-bit images).
  - `binary_start`: Position in the file where binary pixel data begins.

- **Results**:

  I read a `.ppm` dataset and printed its contents. Results are as follows:

  | .ppm Data                                                    | First Pixel RGB = (5,13,26)                                  |
  | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250108180928715.png" alt="image-20250108180918838"/> | <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250108180918838.png" alt="image-20250108180918838" style="zoom:60%;" /> |

  This confirms that the original `.ppm` image is stored in Band Interleaved by Pixel (BIP) format, where all RGB values of each pixel are stored sequentially, e.g., `Pixel1 [R, G, B] → Pixel2 [R, G, B] → Pixel3 [R, G, B]`.

#### 2. Extract raw data

- **Function**: `extract_raw_data`

  Extracts the binary pixel data from a PPM file and saves it as a raw binary file.

- **Parameters**:
  - `file_path`: Path to the PPM file.
  - `binary_start`: Position in the file where binary pixel data begins (returned by `read_ppm`).
  - `output_path`: Path to save the extracted raw binary data.
- **Steps**:
  1. Open the PPM file in binary read mode.
  2. Move the file pointer to the position of `binary_start` to skip the header.
  3. Read the binary pixel data.
  4. Save the pixel data to the specified output path as a raw file.

------

## `YCbCr` and RGB Conversion

### 1. **RGB to `YCbCr` Conversion**

- **Function**: `rgb_to_ycbcr`

  Converts an RGB image to `YCbCr` color space.

- **Parameters**:

  - `img`: `numpy.ndarray`, input RGB image.

- **Returns**:

  - `Y`: Luminance channel (`numpy.ndarray`).
  - `Cb`: Blue chrominance channel (`numpy.ndarray`).
  - `Cr`: Red chrominance channel (`numpy.ndarray`).

- **Steps**:

  - Use Pillow to convert RGB to `YCbCr`.
  - Convert `YCbCr` to NumPy array.
  - Separate and return `Y`, `Cb`, `Cr` channels.

### 2. **`YCbCr` to RGB Conversion**

- **Function**: `ycbcr_to_rgb`

  Restores an RGB image from `YCbCr`.

- **Parameters**:

  - `Y`, `Cb`, `Cr`: Channels as `numpy.ndarray`.

- **Returns**:

  - `rgb_img`: Reconstructed RGB image (`numpy.ndarray`).

- **Steps**:

  - Stack `Y`, `Cb`, `Cr` into a 3D array.
  - Convert the stacked array to `YCbCr` using Pillow.
  - Convert `YCbCr` back to RGB.

### 3. Test Cases

This is just a utility, but I included a test case in the main function.

- **RGB to `YCbCr`**:
  - Read the original image `../../dataset/rgb8bit/nightshot_iso_1600.ppm`.
  - Use `rgb_to_ycbcr` to separate the image into `Y`, `Cb`, and `Cr` channels.
  - Save the `Y`, `Cb`, and `Cr` channels individually in the `../data/ycbcr` directory.
- **`YCbCr` to RGB**:
  - Use `ycbcr_to_rgb` with the `Y`, `Cb`, and `Cr` channel data.
  - Restore the RGB image and save it to `../data/ycbcr/recover_rgb_pillow.png`.

------

## FMM Quantization Tool

### 1. Module Overview

- **Function**: `fmm_quantization`
  - Performs finite modulus quantization on a given channel.
- **Parameters**:
  - `channel`: `numpy.ndarray`, representing one channel of an image.
  - `modulus`: Integer, the modulus used for FMM quantization.
- **Returns**:
  - Quantized channel data (`numpy.ndarray`).
- **Steps**:
  1. Adjust values using rounding, then multiply by the modulus to get quantized results.
  2. Return the quantized data.

### 2. Test Case

This is another utility, with a test case provided in the main function.

- Use `read_ppm` to read a PPM image from a specified path.
- Use `rgb_to_ycbcr` to convert the RGB image to `Y`, `Cb`, and `Cr` channels.
- Apply FMM quantization to each channel, adjusting the modulus to achieve the desired effect.
- Save the quantized `Y`, `Cb`, and `Cr` channels as PNG images.
- Use `ycbcr_to_rgb to restore the quantized `YCbCr` data to an RGB image and save it.

------

# Compression and Decompression

## Compression Implementation

### 1. Run-Length Encoding (RLE)

- **Function**: `rle_compress`
  - Compresses a 2D image channel using **RLE (Run-Length Encoding)**.
- **Parameters**:
  - `channel`: `numpy.ndarray`, input image channel (2D array).
- **Returns**:
  - `compressed`: List of tuples `(value, count)`, representing the pixel value and its consecutive occurrence count.
- **Steps**:
  - Flatten the 2D image channel into a 1D array.
  - Iterate through pixel values, recording consecutive repeated values and their counts.
  - Store the compressed results in a list and return it.

### 2. Saving Compressed Data

- **Function**: `save_compressed_data_npz`
  - Saves the compressed channel data and image dimensions as a binary `.npz` file.
- **Parameters**:
  - `Y_compressed`: Compressed `Y` channel data.
  - `Cb_compressed`: Compressed `Cb` channel data.
  - `Cr_compressed`: Compressed `Cr` channel data.
  - `Y_shape`: Original dimensions of the `Y` channel.
  - `filename`: String, the name of the output file.
- **Steps**:
  - Use `numpy.savez_compressed` to save the compressed data and image dimensions.
  - Generate a binary `.npz` file for later decompression and restoration.

### 3. Code Execution

To execute the compression, modify the image path in the main function to call the modules and generate a compressed binary file.

1. Use `read_ppm` to read an RGB image from `../dataset/rgb8bit/nightshot_iso_1600.ppm`.
2. Use `rgb_to_ycbcr` to separate the image into `Y`, `Cb`, and `Cr` channels.
3. Perform FMM quantization on each channel with modulus 4 for `Y` and modulus 7 for `Cb` and `Cr`.
4. Compress the quantized `Y`, `Cb`, and `Cr` channels using RLE.
5. Save the compressed data and image dimensions to `data/compressed_data.npz` using `save_compressed_data_npz`.

------

## Decompression Implementation

### 1. Decoding Decompression

- **Function**: `rle_decompress`
  - Decompresses RLE data to restore 2D image data.
- **Parameters**:
  - `compressed_data`: List of RLE-compressed `(value, count)` tuples.
  - `shape`: Tuple representing the shape of the decompressed image (e.g., `(height, width)`).
- **Returns**:
  - `decompressed`: `numpy.ndarray`, the decompressed 2D image data.
- **Steps**:
  - Initialize a zero-filled array with the specified shape.
  - Iterate over `compressed_data`, filling the array with each value according to its count.
  - Return the decompressed image data.

### 2. Restoring Image

- **Function**: `restore_image_from_npz`
  - Restores the original RGB image from a compressed `.npz` file.
- **Parameters**:
  - `npz_filename`: String, path to the input `.npz` file.
- **Steps**:
  - Load compressed data: Extract compressed `Y`, `Cb`, `Cr` data and image shape from the `.npz` file.
  - Decompress: Use `rle_decompress` to restore `Y`, `Cb`, and `Cr` channels.
  - Convert `YCbCr` to RGB: Use `ycbcr_to_rgb` to transform the decompressed data back to an RGB image.
  - Save the restored image as a common PNG format.

### 3. Code Execution

Modify the parameter in the main function to point to the path of the compressed binary file when calling `restore_image_from_npz`. This will decompress the image and restore it to its original form.

