import random
from PIL import Image

def embed_data_with_key(image_path, output_image_path, secret_data, data_hiding_key, t=1, group_size=4):
    """
    Embed secret data into the image by using the data hiding key to shuffle pixel groups for Set A and Set B,
    then flipping the t-th LSB of all pixels within each pixel group.
    """
    # Load the image
    image = Image.open(image_path).convert('L')  # Convert image to grayscale
    pixel_map = image.load()
    width, height = image.size

    # Convert the secret data to bits
    secret_bits = ''.join(format(ord(char), '08b') for char in secret_data)
    bit_index = 0

    # Define sets A and B based on pixel positions
    set_a = []
    set_b = []

    for i in range(height):
        for j in range(width):
            if i % 2 == 0 and j % 2 == 1:  # Set A: even rows, odd columns
                set_a.append((i, j))
            elif i % 2 == 1 and j % 2 == 0:  # Set B: odd rows, even columns
                set_b.append((i, j))

    # Function to flip the t-th least significant bit of a pixel
    def flip_t_bit(pixel_value, bit, t):
        mask = 1 << (t - 1)
        return (pixel_value & ~mask) | ((bit << (t - 1)) & mask)

    # Shuffle the pixel groups using the data hiding key
    random.seed(data_hiding_key)
    random.shuffle(set_a)
    random.shuffle(set_b)

    # Split Set A and Set B into non-overlapping groups
    def create_groups(pixel_set, group_size):
        groups = [pixel_set[i:i+group_size] for i in range(0, len(pixel_set), group_size)]
        return groups

    groups_a = create_groups(set_a, group_size)
    groups_b = create_groups(set_b, group_size)

    # Embed data into Set A (simplified embedding for demo purposes)
    for group in groups_a:
        if bit_index >= len(secret_bits):
            break
        for pixel in group:
            if bit_index >= len(secret_bits):
                break
            pixel_value = pixel_map[pixel]
            bit_to_embed = int(secret_bits[bit_index])
            bit_index += 1
            # Flip the t-th LSB to embed the bit
            pixel_map[pixel] = flip_t_bit(pixel_value, bit_to_embed, t)

    # Embed data into Set B (optional, depending on available data)
    for group in groups_b:
        if bit_index >= len(secret_bits):
            break
        for pixel in group:
            if bit_index >= len(secret_bits):
                break
            pixel_value = pixel_map[pixel]
            bit_to_embed = int(secret_bits[bit_index])
            bit_index += 1
            # Flip the t-th LSB to embed the bit
            pixel_map[pixel] = flip_t_bit(pixel_value, bit_to_embed, t)

    # Save the image with the embedded data
    image.save(output_image_path, format="tiff")
    print("Data embedding completed and saved as", output_image_path)
    image.show()

# Example usage
secret_data = "Hello"  # Data to be embedded
data_hiding_key = "example_key"  # Key for shuffling pixel groups
embed_data_with_key("encrypted_image2.tiff", "stego_image_correct.tiff", secret_data, data_hiding_key)
