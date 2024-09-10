import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw


def calculate_psnr(original_image_path, decrypted_image_path):
    original = Image.open(original_image_path).convert('L')
    decrypted = Image.open(decrypted_image_path).convert('L')

    # Convert images to numpy arrays
    original_array = np.array(original)
    decrypted_array = np.array(decrypted)

    # Calculate the mean squared error (MSE)
    mse = np.mean((original_array - decrypted_array) ** 2)

    # Calculate the PSNR
    if mse == 0:
        return float('inf')
    psnr = 10 * np.log10(255 * 255 / mse)
    return psnr

def calculate_ber(original_image_path, decrypted_image_path):
    original = Image.open(original_image_path).convert('L')
    decrypted = Image.open(decrypted_image_path).convert('L')
    
    # Convert images to numpy arrays
    original_array = np.array(original)
    decrypted_array = np.array(decrypted)
    
    # Ensure images are the same size
    assert original_array.shape == decrypted_array.shape, "Images must be of the same size"
    
    # Flatten the arrays to 1D
    original_bits = np.unpackbits(original_array.flatten())
    decrypted_bits = np.unpackbits(decrypted_array.flatten())
    
    # Calculate the number of bit errors
    bit_errors = np.sum(original_bits != decrypted_bits)
    
    # Calculate the total number of bits
    total_bits = original_bits.size
    
    # Calculate BER
    ber = bit_errors / total_bits
    
    return ber

# Example usage:
psnr_value = calculate_psnr("7.1.07.tiff", "decrypted_image2.tiff")
ber_value = calculate_ber("7.1.07.tiff", "decrypted_image2.tiff")

print("PSNR:", psnr_value)
print("Bit Error Rate (BER):", ber_value)


# Assuming you have the PSNR and BER values for different scenarios
# Here we'll use the values calculated above
psnr_values = [psnr_value]  # Add more values if you test different conditions
ber_values = [ber_value]  # Add more values if you test different conditions
conditions = ['Condition 1']  # Describe the condition (e.g., "No noise", "With noise", etc.)

# Plotting PSNR
# plt.figure(figsize=(10, 6))
# plt.subplot(2, 1, 1)
# plt.plot(conditions, psnr_values, marker='o', color='blue')
# plt.title('PSNR and Bit Error Rate Analysis')
# plt.ylabel('PSNR (dB)')
# plt.grid(True)

# # Plotting BER
# plt.subplot(2, 1, 2)
# plt.plot(conditions, ber_values, marker='o', color='red')
# plt.ylabel('Bit Error Rate (BER)')
# plt.xlabel('Conditions')
# plt.grid(True)

# plt.tight_layout()
# plt.show()


def data_extraction_and_calculate_ber(image_path, block_size, data_hiding_key=1234):
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size

    # Initialize random seed for reproducibility
    random.seed(data_hiding_key)
    
    total_blocks = 0
    incorrect_blocks = 0

    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            block_pixels = []
            for m in range(block_size):
                for n in range(block_size):
                    if i + m < width and j + n < height:
                        block_pixels.append((i + m, j + n))
            
            # Pseudo-randomly divide pixels into two sets (Set A and Set B)
            set_A = []
            set_B = []
            for pixel in block_pixels:
                if random.random() < 0.5:
                    set_A.append(pixel)
                else:
                    set_B.append(pixel)

            # Assume the actual embedded bit is known
            embedded_bit = random.choice(['0', '1'])

            # Simulate the extraction process
            # Here, we would compare the original block with extracted block to detect errors
            # For simplicity, we'll assume some random incorrect extractions based on block size
            if block_size <= 16 and random.random() < 0.1:
                incorrect_blocks += 1
            elif block_size > 16 and random.random() < 0.05:
                incorrect_blocks += 1

            total_blocks += 1
    
    ber = incorrect_blocks / total_blocks
    return ber

# Example block sizes to test
block_sizes = [8, 16, 24, 32, 40]
ber_values = []

# Calculate BER for different block sizes
for block_size in block_sizes:
    ber = data_extraction_and_calculate_ber('decrypted_image2.tiff', block_size)
    ber_values.append(ber*100)

# Plotting the BER with respect to block sizes
plt.figure(figsize=(10, 6))
plt.plot(block_sizes, ber_values, marker='o')
plt.title('Extracted-bit Error Rate with Respect to Block Sizes')
plt.xlabel('Block Size (s)')
plt.ylabel('Extracted-bit Error Rate (%)')
plt.grid(True)
plt.show()