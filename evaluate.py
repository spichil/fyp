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



from ch_data_extraction_ver1 import decrypt_image, data_extraction, calculate_ber, plot_ber_vs_block_size
from data_embedding import data_embedding_paper
def run_experiment(image_path, output_path, secret_data, key, block_sizes, data_hiding_key=1234):
    ber_values = []
    
    for block_size in block_sizes:
        print(f"Running for block size: {block_size}")
        output_image_path = f"embedded_image_block_{block_size}.tiff"
        decrypted_image_path = f"decrypted_image_block_{block_size}.tiff"
        
        # Embed the data
        data_embedding_paper(image_path, secret_data, output_image_path, block_size, data_hiding_key)
        
        # Decrypt the image
        decrypt_image(output_image_path, decrypted_image_path, key)
        
        # Extract the data
        extracted_bits = data_extraction(decrypted_image_path,output_path, block_size, data_hiding_key)
        
        # Convert the original secret data to binary for comparison
        original_bits = ''.join(format(byte, '08b') for byte in bytearray(secret_data, encoding='utf-8'))
        
        # Calculate BER
        ber = calculate_ber(extracted_bits, original_bits)
        ber_values.append(ber)
        print(f"BER for block size {block_size}: {ber}")

    return block_sizes, ber_values

# Run the experiment and plot the results
if __name__ == "__main__":
    block_sizes = [8, 16, 32, 64]  # Different block sizes to test
    data_hiding_key = 1234
    key = b'pzkUHwYaLVLml0hh'
    image_path = 'encrypted_image.tiff'
    secret_data = 'Secret'
    output_path = 'recovered_image.tiff'
    
    # Run the experiment
    block_sizes, ber_values = run_experiment(image_path, output_path, secret_data, key, block_sizes, data_hiding_key)
    print(data_extraction(image_path, output_path, block_size=32, data_hiding_key=data_hiding_key))

    # Plot the results
    plot_ber_vs_block_size(block_sizes, ber_values)
