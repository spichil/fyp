from LSB_embedding import *
def data_extraction(encrypted_image_path, output_image_path, secret_data, data_hiding_key, t=1):
    """
    Extracting data by using the data hiding key to find pixel groups for set A and set B, then
    flipping the t-th LSB of all pixels within each pixel group, creating Gi and FGi, which stands
    for the pixel group and flipped pixel group. The two-round interpolation technique is used to 
    judge which of these pixel groups are correct for set A. After all pixels of set A have been 
    recovered to their original values, the pixel groups for set B are reconstructed. A similar 
    process of flipping pixel groups are done for set B, but the pixel prediction is executed with 
    the variant cubic based bicubic interpolation algorithm.
    """
    # Load the encrypted image
    encrypted_image = Image.open(encrypted_image_path).convert('L')
    pixel_map = encrypted_image.load()
    width, height = encrypted_image.size
    
    secret_bits = []
    set_a = []
    set_b = []
    
    # Define sets A and B based on the pixel positions
    for i in range(height):
        for j in range(width):
            if i % 2 == 0 and j % 2 == 1:  # Set A: even rows, odd columns
                set_a.append((i, j))
            elif i % 2 == 1 and j % 2 == 0:  # Set B: odd rows, even columns
                set_b.append((i, j))
    
    #TO DO: pixel group flipping, run pixel predictor algorithms for each set.


    # Save the image with the embedded data
    encrypted_image.save(output_image_path, format="tiff")
    print("Data embedding completed and saved as", output_image_path)
    encrypted_image.show()