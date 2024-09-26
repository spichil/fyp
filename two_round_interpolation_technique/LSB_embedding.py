import random
from PIL import Image

def embed_data_paper(encrypted_image_path, output_image_path, secret_data, data_hiding_key, t=1):
    """
    Embedding data by flipping the t-th least significant bit of carrier pixels.
    Follows the two-round embedding process from the paper.
    """
    # Load the encrypted image
    encrypted_image = Image.open(encrypted_image_path).convert('L')
    pixel_map = encrypted_image.load()
    width, height = encrypted_image.size
    
    # Convert secret data into bits
    secret_bits = []
    for char in secret_data:
        # Convert each character to its binary representation and add to the list of secret bits
        secret_bits.extend([int(bit) for bit in format(ord(char), '08b')])

    # Carrier pixel sets (Set A and Set B)
    set_a = []
    set_b = []
    
    # Define sets A and B based on the pixel positions
    for i in range(height):
        for j in range(width):
            if i % 2 == 0 and j % 2 == 1:  # Set A: even rows, odd columns
                set_a.append((i, j))
            elif i % 2 == 1 and j % 2 == 0:  # Set B: odd rows, even columns
                set_b.append((i, j))
    
    # Initialize index for the secret bits
    bit_index = 0
    total_bits = len(secret_bits)

    # Function to modify the t-th least significant bit of a pixel based on a secret bit
    def flip_t_bit(pixel_value, secret_bit, t):
        mask = 1 << (t - 1)  # Create a mask for the t-th bit
        if ((pixel_value & mask) >> (t - 1)) == secret_bit:
            return pixel_value  # t-th bit already matches
        else:
            return pixel_value ^ mask  # Flip the t-th bit

    # Embed data in Set A first
    for pixel in set_a:
        if bit_index < total_bits:
            # Get the current pixel value
            pixel_value = pixel_map[pixel]
            # Modify the t-th LSB of the pixel value based on the secret bit
            new_pixel_value = flip_t_bit(pixel_value, secret_bits[bit_index], t)
            # Update the pixel map
            pixel_map[pixel] = new_pixel_value
            bit_index += 1

    # If secret data still remains, use Set B for embedding
    for pixel in set_b:
        if bit_index < total_bits:
            # Get the current pixel value
            pixel_value = pixel_map[pixel]
            # Modify the t-th LSB of the pixel value based on the secret bit
            new_pixel_value = flip_t_bit(pixel_value, secret_bits[bit_index], t)
            # Update the pixel map
            pixel_map[pixel] = new_pixel_value
            bit_index += 1

    if bit_index < total_bits:
        print("Warning: Not enough space to embed all the secret data.")

    # Save the image with the embedded data
    encrypted_image.save(output_image_path, format="tiff")
    print("Data embedding completed and saved as", output_image_path)
    encrypted_image.show()
    
    

# Example usage
secret_message = "This is the secret data."
data_hiding_key = "example_key" 
embed_data_paper("encrypted_image2.tiff", "stego_image_paper.tiff", secret_message, data_hiding_key)
