import numpy as np


def calculate_entropy(file_path: str) -> float:
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    image_data = np.frombuffer(raw_data, dtype=np.uint8).reshape(-1, 3)

    combined_values = (image_data[:, 0].astype(np.int32) << 16) | \
                      (image_data[:, 1].astype(np.int32) << 8) | \
                      image_data[:, 2].astype(np.int32)

    unique_vals, counts = np.unique(combined_values, return_counts=True)
    probabilities = counts / combined_values.size

    entropy = -np.sum(probabilities * np.log2(probabilities))

    print(f"Shannon entropy of the RAW image: {entropy:.2f} bits")


if __name__ == "__main__":
    file_path = '../data/image.raw'
    calculate_entropy(file_path)
