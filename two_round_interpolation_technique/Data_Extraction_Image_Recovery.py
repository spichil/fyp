from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter
import numpy as np
from parabolic_interpolation_algorithm import parabolic_interpolation_algorithm
from variant_cubic_based_bicubic_interpolation_algorithm import cubic_based_bicubic_interpolation_algorithm
from Function_equation import calculate_b


# Function to flip the t-th least significant bit
def flip_bit(pixel_value, t):
    return pixel_value ^ (1 << (t-1))

# AES-CTR Mode for decryption
def aesCTR(key, num_bits):
    counter = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    num_bytes = (num_bits + 7) // 8
    random_bytes = cipher.encrypt(b'\x00' * num_bytes)
    return [((byte >> (7 - i)) & 1) for byte in random_bytes for i in range(8)]

# Decrypt the encrypted image using AES-CTR
def decrypt_image(input_image_path, output_image_path, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (128 bits) long.")
    
    input_image = Image.open(input_image_path)
    width, height = input_image.size
    num_bits = width * height * 8
    stream_cipher = aesCTR(key, num_bits)
    
    bit_index = 0
    decrypted_image = Image.new("L", (width, height))
    pixel_map = decrypted_image.load()
    
    for i in range(width):
        for j in range(height):
            pixel_value = input_image.getpixel((i, j))
            after_decryption_pixel_value = 0
            for k in range(8):
                bit = (pixel_value // (2 ** k)) % 2
                random_bit = stream_cipher[bit_index]
                bit_index += 1
                resulting_bit = bit ^ random_bit
                after_decryption_pixel_value += resulting_bit * (2 ** k)
            pixel_map[i, j] = int(after_decryption_pixel_value)
    
    decrypted_image.save(output_image_path, format="tiff")
    decrypted_image.show()
    return output_image_path

# Reconstruct pixel groups for Set A and Set B
def reconstruct_pixel_groups(width, height, data_hiding_key):
    set_a = [(i, j) for i in range(height) for j in range(width) if i % 2 == 0 and j % 2 == 1]
    set_b = [(i, j) for i in range(height) for j in range(width) if i % 2 == 1 and j % 2 == 0]
    return set_a, set_b

# Process pixel group: original, flipped, predicted groups
def process_pixel_group(image, group, t, use_bicubic=False):
    # Load pixel map
    pixel_map = image.load()
    
    # Get original pixel values from the group
    original_group = [pixel_map[x, y] for x, y in group]
    
    # Flip the t-th LSB to create the flipped group
    flipped_group = [flip_bit(pixel_map[x, y], t) for x, y in group]
    
    # Use the interpolation algorithm to predict pixel values
    if use_bicubic:
        predicted_group = cubic_based_bicubic_interpolation_algorithm(image, group)
    else:
        predicted_group = parabolic_interpolation_algorithm(image, group)
    
    # Return the original, flipped, and predicted groups, along with the secret bit
    return original_group, flipped_group, predicted_group

# Recover the original pixels based on b value
def recover_original_pixels(pixel_map, group, recovered_group):
    for (x, y), value in zip(group, recovered_group):
        pixel_map[x, y] = value

# Main function for data extraction and image recovery
def extract_and_recover_image(input_image_path, output_image_path, key, data_hiding_key, t=1):
    # Load the decrypted image
    decrypted_image = Image.open(input_image_path).convert('L')
    pixel_map = decrypted_image.load()
    width, height = decrypted_image.size
    
    set_a, set_b = reconstruct_pixel_groups(width, height, data_hiding_key)  # Define sets A and B
    secret_bits = []  # To store the extracted secret bits
    
    # First round: Process Set A
    for group in set_a:
        original_group, flipped_group, predicted_group = process_pixel_group(pixel_map, group, t)
        
        # Integrate calculate_b function here
        secret_bit = calculate_b(original_group, flipped_group, predicted_group)  # Get the value of b
        secret_bits.append(secret_bit)  # Store the extracted bit
        
        # Recover the original pixels
        recover_original_pixels(pixel_map, group, original_group if secret_bit == 0 else flipped_group)
    
    # Second round: Process Set B
    for group in set_b:
        original_group, flipped_group, predicted_group = process_pixel_group(pixel_map, group, t, use_bicubic=True)
        secret_bit = calculate_b(original_group, flipped_group, predicted_group)  # Get the value of b
        secret_bits.append(secret_bit)  # Store the extracted bit
        recover_original_pixels(pixel_map, group, original_group if secret_bit == 0 else flipped_group)
    
    # Save the recovered image
    recovered_image = Image.fromarray(np.array(decrypted_image))
    recovered_image.save(output_image_path, format="tiff")
    recovered_image.show()

    # Extracted secret data (convert secret_bits to string)
    extracted_data = ''.join(chr(int(''.join(map(str, secret_bits[i:i+8])), 2)) for i in range(0, len(secret_bits), 8))
    return extracted_data

# Test function to decrypt, recover, and extract data
def test_data_extraction_and_recovery():
    encrypted_image_path = "stego_image_correct.tiff"  # Path to your encrypted image
    decrypted_image_path = "decrypted_image.tiff"
    recovered_image_path = "recovered_image.tiff"

    # Example keys (adjust the keys according to your setup)
    image_encryption_key = b'pzkUHwYaLVLml0hh'
    data_hiding_key = "example_key"

    # Step 1: Decrypt the image
    decrypted_image = decrypt_image(encrypted_image_path, decrypted_image_path, image_encryption_key)
    
    # Step 2: Extract secret data and recover the original image
    extracted_data = extract_and_recover_image(decrypted_image_path, recovered_image_path, image_encryption_key, data_hiding_key, t=1)
    
    # Step 3: Print the extracted secret data
    print("Extracted secret data:", extracted_data)

    # Step 4: Load and show the recovered image
    recovered_image = Image.open(recovered_image_path)
    recovered_image.show()

if __name__ == "__main__":
    test_data_extraction_and_recovery()
