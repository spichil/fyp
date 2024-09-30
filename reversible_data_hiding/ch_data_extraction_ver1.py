from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter
from reversible_data_hiding.image_encryption2 import aesCTR
import random
import matplotlib.pyplot as plt
import os

def decrypt_image(input_image_path, output_image_path, key):
    '''
    Decryption process is similar to encryption process, just done in reverse using the same key.
    '''
    # Ensure key is 16 bytes long (128 bits)
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (128 bits) long.")
    
    # Load the input image and set the full path for the output image
    input_image_full_path = os.path.abspath(input_image_path)  # Get absolute path for the input
    output_image_full_path = os.path.abspath(output_image_path)  # Get absolute path for the output

    # Import an image from directory
    input_image = Image.open(input_image_full_path)    
    
    # Extract the width and height of the image
    width, height = input_image.size
    
    # Generate pseudo-random bits using AES-CTR
    num_bits = width * height * 8
    stream_cipher = aesCTR(key, num_bits)
    
    bit_index = 0
    
    # Create a new image for the decrypted output
    decrypted_image = Image.new("L", (width, height))
    pixel_map = decrypted_image.load()
    
    # Decryption process
    for i in range(width):
        for j in range(height):
            # Getting the pixel value
            pixel_value = input_image.getpixel((i, j))
            after_decryption_pixel_value = 0
            
            for k in range(8):
                # Bit extraction using division and modulo
                bit = (pixel_value // (2 ** k)) % 2
                
                # Get the corresponding pseudo-random bit
                random_bit = stream_cipher[bit_index]
                bit_index += 1
                
                # XOR operation with generated bit
                resulting_bit = bit ^ random_bit
                
                after_decryption_pixel_value += resulting_bit * (2 ** k)
            
            # Update the pixel value with the decrypted value
            pixel_map[i, j] = int(after_decryption_pixel_value)
    
    # Saving the final output
    decrypted_image.save(output_image_full_path, format="tiff")

def data_extraction(image_path, output_path, block_size, data_hiding_key):
    """
    Data extraction function to be executed after image decryption.
    Extracts embedded bits from the decrypted image.
    """
    embedded_bits = ""
    
    # Load the decrypted image
    image_full_path = os.path.abspath(image_path)
    output_full_path = os.path.abspath(output_path)
    
    image = Image.open(image_full_path).convert('L')   
    pixel_map = image.load()
    width, height = image.size

    # Initialize random seed for reproducibility
    random.seed(data_hiding_key)

    # Copy the input image twice for spatial correlation comparison
    h0_image = image.copy()
    h0_pixelmap = h0_image.load()
    h1_image = image.copy()
    h1_pixelmap = h1_image.load()

    # Segmentation of decrypted image into non-overlapping blocks
    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            block_pixels = [(i + m, j + n) for m in range(block_size) for n in range(block_size) 
                            if i + m < width and j + n < height]
                
            # Pseudo-randomly divide pixels into two sets (Set A and Set B)
            set_A, set_B = [], []
            for pixel in block_pixels:
                if random.random() < 0.5:
                    set_A.append(pixel)
                else:
                    set_B.append(pixel)

            # Flip LSB of pixels in Set A, then update the pixels in h0
            for pixel in set_A:
                pixel_value = pixel_map[pixel]
                pixel_bin = format(pixel_value, '08b')
                new_pixel_bin = pixel_bin[:-1] + ('1' if pixel_bin[-1] == '0' else '0')
                h0_pixelmap[pixel] = int(new_pixel_bin, 2)

            # Flip LSB of pixels in Set B, then update the pixels in h1
            for pixel in set_B:
                pixel_value = pixel_map[pixel]
                pixel_bin = format(pixel_value, '08b')
                new_pixel_bin = pixel_bin[:-1] + ('1' if pixel_bin[-1] == '0' else '0')
                h1_pixelmap[pixel] = int(new_pixel_bin, 2)

            # Compare spatial correlation to determine most correct block
            h0_fluc = fluctuation_calculation(h0_image, block_size, i, j)
            h1_fluc = fluctuation_calculation(h1_image, block_size, i, j)

            # Compare fluctuations: lower fluctuation = closer to original
            if h0_fluc < h1_fluc:
                for pixel in set_A:
                    pixel_value = pixel_map[pixel]
                    pixel_bin = format(pixel_value, '08b')
                    new_pixel_bin = pixel_bin[:-1] + ('1' if pixel_bin[-1] == '0' else '0')
                    pixel_map[pixel] = int(new_pixel_bin, 2)
                embedded_bits += "0"
            else:
                for pixel in set_B:
                    pixel_value = pixel_map[pixel]
                    pixel_bin = format(pixel_value, '08b')
                    new_pixel_bin = pixel_bin[:-1] + ('1' if pixel_bin[-1] == '0' else '0')
                    pixel_map[pixel] = int(new_pixel_bin, 2)
                embedded_bits += "1"

    decoded_message = decode_binary_string(embedded_bits)

    # Save the image with embedded data
    image.save(output_full_path)

    print(f"Extracted Message: {decoded_message}")
    return decoded_message

def decode_binary_string(s):
    return ''.join(chr(int(s[i * 8: i * 8 + 8], 2)) for i in range(len(s) // 8))

def fluctuation_calculation(input_image, block_size, i, j):
    fluctuation = 0
    pixel_map = input_image.load()
    for u in range(1, block_size - 1):
        for v in range(1, block_size - 1):
            neighbors = (pixel_map[i + u - 1, j + v] + pixel_map[i + u + 1, j + v] +
                         pixel_map[i + u, j + v - 1] + pixel_map[i + u, j + v + 1]) / 4
            fluctuation += abs(pixel_map[i + u, j + v] - neighbors)
    return fluctuation

def calculate_ber(extracted_bits, original_bits):
    errors = sum(e != o for e, o in zip(extracted_bits, original_bits))
    return errors / len(original_bits)

def plot_ber_vs_block_size(block_sizes, ber_values):
    plt.figure(figsize=(10, 6))
    plt.plot(block_sizes, ber_values, marker='o')
    plt.title('Extracted-Bit Error Rate with Respect to Block Sizes')
    plt.xlabel('Block Size')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True)
    plt.show()
