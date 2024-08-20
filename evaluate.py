import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

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
key = b'pzkUHwYaLVLml0hh'
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
