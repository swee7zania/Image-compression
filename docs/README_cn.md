# **智能移动设备图像传输**

随着移动设备的普及，图像的存储和传输成本显著增加。为了降低带宽需求，同时保持用户感知质量，我提出一种结合人眼感知特点的图像压缩算法。并在论文 *Five Modulus Method For Image Compression (https://arxiv.org/abs/1211.4591)* 中汲取灵感，将数据取整后再乘以该取整值，使相邻的数值在规定区间内归为相同的值，从而更适应游程编码 (REL)。

### 1. 核心思想

- **人眼感知模型**：人眼对图像的不同区域敏感性不同
  - 对亮度（`Y` 通道）变化极为敏感，特别是边缘与高频细节。
  - 对色度（`Cb` 和 `Cr` 通道）变化的敏感性较低，尤其是低频区域。
- **FMM 应用**：结合人眼感知特性
  - 在亮度通道上使用较小的模数，保留更多细节。
  - 在色度通道上使用较大的模数，显著减少数据量。
- **熵编码**：利用游程编码 (REL)
  - 进一步提升压缩效率，减少冗余信息存储。

### 2. 详细设计内容

#### 2.1 编码 Pipeline

1. **读取与预处理**
   - 读取 `.ppm` 图像数据，亮度通道 `Y`、色度通道 `Cb` 和 `Cr`。
   - 转换为 `YCbCr` 颜色空间，分离亮度与色度通道。
2. **FMM 量化**
   - 亮度通道 `Y`：暂时取模数为4，保留更多视觉重要信息。
   - 色度通道 `Cb` 和 `Cr`：暂时取模数为 7，进一步减少存储和传输数据量。
   - 可以根据图像内容复杂度，动态调整 FMM 量化参数。
4. **熵编码**
   - 将 FMM 量化后的值通过熵编码进一步压缩。
   - 使用 **RLE（游程编码）**，对连续重复的数据段进行有效压缩。
5. **压缩文件打包**
   - 将 RLE 编码后的数据存为二进制文件，保存相关数据。

#### 2.2 解码 Pipeline

1. **读取与解码**
   - 从压缩文件中提取熵编码数据。
   - 分别对 `Y`、`Cb`、`Cr` 三个通道进行 RLE 解码，恢复量化后的数据。
4. **颜色空间逆转换**
   - 将还原的 `YCbCr` 数据转换回 RGB 颜色空间。
5. **输出图像**
   - 生成解压后的图像，存储为常见格式。

------

# 功能模块

## 图像读取工具

- 函数：`read_ppm`

  - 用于读取 PPM 文件并返回重构的图像数组。

- 参数：

  - `file_path`：字符串类型，PPM 文件的路径。

- 返回值：

  - `img`：三维 NumPy 数组，表示读取的 RGB 图像，形状为 `(height, width, 3)`。

- 读取结果：

  我读取了数据集里其中一个 .ppm 数据，并打印了它的存储内容，打印结果如下：

  | .ppm 数据                                                    | 第一个像素 RGB = (5,13,26)                                   |
  | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250108180928715.png" alt="image-20250108180918838"/> | <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250108180918838.png" alt="image-20250108180918838" style="zoom:60%;" /> |

  根据这里我们可以判断，原始图像 .ppm 是用 BIP方式存储的。BIP 存储方式为每个像素的所有 RGB 依次存储。例如 `Pixel1 的 [R, G, B] → Pixel2 的 [R, G, B] → Pixel3 的 [R, G, B]`。

---

## `YCbCr` 与 RGB 转换

### 1. **RGB to `YCbCr` 转换**

- **函数**： `rgb_to_ycbcr_pillow` 

  将 RGB 图像转换为 `YCbCr` 颜色空间。

- **参数**：
  - `img`：`numpy.ndarray` 类型，输入的 RGB 图像。

- **返回值**：

  - `Y`：亮度通道（`numpy.ndarray`）。

  - `Cb`：蓝色色度通道（`numpy.ndarray`）。

  - `Cr`：红色色度通道（`numpy.ndarray`）。

- **实现步骤**：
  - 使用 Pillow 将 RGB 图像转换为 `YCbCr` 图像。
  - 将 `YCbCr` 图像转换为 NumPy 数组。
  - 分离 `Y`、`Cb`、`Cr` 三个通道并返回。

### 2. **`YCbCr` to RGB 转换**

- **函数** `ycbcr_to_rgb_pillow` 

  - 将 `YCbCr` 图像还原为 RGB 图像。

- **参数**：

  - `Y`：亮度通道（`numpy.ndarray`）。

  - `Cb`：蓝色色度通道（`numpy.ndarray`）。

  - `Cr`：红色色度通道（`numpy.ndarray`）。

- **返回值**：
  - `rgb_img`：`numpy.ndarray` 类型，重建后的 RGB 图像。

- **实现步骤**：
  - 将 `Y`、`Cb`、`Cr` 三个通道堆叠为一个三维数组。
  - 使用 Pillow 将堆叠数组转化为 `YCbCr` 图像。
  - 将 `YCbCr` 图像转换回 RGB 图像并返回。

### 3. 测试用例

这只是一个工具，但我在 main 函数中写了一个测试用例。

- **RGB to `YCbCr`**
  - 读取原始图像 `../../dataset/rgb8bit/nightshot_iso_1600.ppm`。
  - 调用 `rgb_to_ycbcr_pillow` 将图像分离为 `Y`、`Cb`、`Cr` 通道。
  - 分别将 `Y` 通道、`Cb` 通道、`Cr` 通道保存在 `../data/ycbcr` 目录中。

- **`YCbCr` to RGB**
  - 调用 `ycbcr_to_rgb_pillow`，参数为 `Y`、`Cb`、`Cr` 通道数据。
  - 还原为 RGB 图像，并保存至 `../data/ycbcr/recover_rgb_pillow.png`。

---

## FMM 量化工具

### 1. 模块概述

- **函数** `fmm_quantization`
  - 对给定通道数据进行有限模数量化。
- **参数**：
  - `channel`：`numpy.ndarray` 类型，表示图像的一个通道。
  - `modulus`：整数，FMM 量化的模数。
- **返回值**：
  - 量化后的通道数据，`numpy.ndarray` 类型。
- **实现步骤**：
  1. 通过四舍五入调整后再乘以模数，得到量化结果。
  2. 返回量化后的通道数据。

### 2. **测试**用例

这只是一个工具，但我在 main 函数中写了一个测试用例。

-  使用 `read_ppm` 从指定路径读取 PPM 图像。
- 使用 `rgb_to_ycbcr_pillow` 将 RGB 图像转换为 `Y`、`Cb`、`Cr` 三个通道。
- 对每个通道进行 FMM 量化，可自由设置模数达到想要的效果。
- 将量化后的 `Y`、`Cb`、`Cr` 通道分别保存为 PNG 图像。
-  使用 `ycbcr_to_rgb_pillow` 将量化后的 `YCbCr` 数据还原为 RGB 图像，并保存。

------

# 压缩与解压

## 压缩功能实现

### 1. 游程编码 (REL)

- **函数**：`rle_compress`
  - 对输入的二维图像通道数据进行 **RLE（游程编码）** 压缩。

- **参数**：
  - `channel`：`numpy.ndarray` 类型，输入的图像通道数据（二维数组）。

- **返回值**：
  - `compressed`：列表，每个元素格式为 `(value, count)`，表示某像素值及其连续出现的次数。

- **实现步骤**：
  - 将二维图像通道展平为一维数组。
  - 遍历像素值，记录连续重复的像素值及其计数。
  - 将压缩结果存入列表并返回。

### 2. 压缩文件保存

- **函数**：`save_compressed_data_npz`
  - 将压缩后的通道数据及图像形状保存为二进制 `.npz` 文件。

- **参数**：

  - `Y_compressed`：亮度通道 `Y` 的 RLE 压缩数据。

  - `Cb_compressed`：色度通道 `Cb` 的 RLE 压缩数据。

  - `Cr_compressed`：色度通道 `Cr` 的 RLE 压缩数据。

  - `Y_shape`：原始图像 Y 通道的形状（元组）。

  - `filename`：字符串，保存的文件名。

- **实现步骤**：

  - 使用 `numpy.savez_compressed` 保存 `Y`、`Cb`、`Cr` 通道的压缩数据和图像形状。

  - 生成二进制 `.npz` 文件，用于后续解压和还原。

### 3. 代码执行

更改 main 函数中的图像路径，即可调用模块实现图像压缩，生成压缩后的二进制文件。

1. 使用 `read_ppm` 从路径 `../dataset/rgb8bit/nightshot_iso_1600.ppm` 读取 RGB 图像。
2. 使用 `rgb_to_ycbcr_pillow` 将图像分解为 `Y`、`Cb`、`Cr` 三个通道。
3. 对每个通道进行 FMM 量化：这里我取 `Y` 通道模数为 4，`Cb` 和 `Cr` 通道模数为 7。
4. 对量化后的 `Y`、`Cb`、`Cr` 通道数据进行 RLE 压缩。
5. 调用 `save_compressed_data_npz`将压缩数据和图像形状信息保存为二进制文件 `data/compressed_data.npz`。

------

## 解压功能实现

### 1. 编码解压

- **函数**：`rle_decompress`

  - 对 RLE 压缩数据进行解压缩，将其还原为二维图像数据。

- **参数**：

  - `compressed_data`：列表，包含 RLE 压缩的 `(value, count)` 元组。

  - `shape`：解压后图像的形状（如 `(height, width)`）。

- **返回值**：
  - `decompressed`：`numpy.ndarray` 类型，解压后的二维图像数据。

- **实现步骤**：

  - 初始化一个全零数组，形状为 `shape`。

  - 遍历 `compressed_data`，将每个值根据其计数填入解压数组的相应位置。

  - 返回解压后的图像数据。

### 2. 恢复图像

- **函数**：`restore_image_from_npz`
  - 从 `.npz` 文件中恢复压缩前的 RGB 图像并保存。

- **参数**：
  - `npz_filename`：字符串，输入的 `.npz` 文件路径。

- **实现步骤**：
  - 加载压缩数据：从 `.npz` 文件中读取压缩的 `Y`、`Cb`、`Cr` 数据及图像形状信息。
  - 解压缩：对 `Y`、`Cb`、`Cr` 通道数据分别调用 `rle_decompress` 进行解压缩。
  - `YCbCr` 转 RGB：使用 `ycbcr_to_rgb_pillow` 将解压后的 `YCbCr` 数据转换为 RGB 图像。
  - 保存恢复图像：将恢复的 RGB 图像保存为常见的 PNG 图像格式。

## **代码执行**

在 main 函数中调用的 `restore_image_from_npz` 中，更改传入的参数（压缩后的二进制文件路径），即可调用模块实现图像复原，得到复原后的图像。

两个图像的对比如下：

| 原始图像                                                     | 压缩文件                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `nightshot_iso_1600.ppm` （21610 KB）                        | `compressed_data.npz`（9457 KB）                             |
| <img src="D:\0. Data Transmittion\Image Compression\assets\image-20250110181253164.png" alt="image-20250110181253164"/> | ![image-20250110181316824](D:\0. Data Transmittion\Image Compression\assets\image-20250110181316824.png) |

压缩率计算：
$$
\text{压缩率} = \frac{9457}{21610} \times 100\% \approx 43.75\%
$$
最终的压缩率约为 **43.75%**。
