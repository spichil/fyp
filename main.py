import customtkinter as ctk
from tkinter import Label
from PIL import Image, ImageTk
from image_widgets import *  # Assuming this contains your custom widgets
from menu import *  # Assuming this handles additional UI elements
from reversible_data_hiding.image_encryption2 import encrypt_image  # Your encryption logic
from reversible_data_hiding.data_embedding import data_embedding_paper  # Your embedding logic
from reversible_data_hiding.ch_data_extraction_ver1 import decrypt_image, data_extraction  # Your decryption and extraction logic

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        self.geometry('1000x600')
        self.title('Watermarking App')
        self.minsize(1000, 600)

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # Widget to import the image
        self.image_import = ImageImport(self, self.import_image)

        # Run
        self.mainloop()
            
    def import_image(self, path):
        self.image_path = path  # Store image path
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)

        # reset the grid
        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        # Close button to choose another image
        self.close_button = CloseOutput(self, self.close_edit)

        # Menu for settings
        self.menu = Menu(self, self.submit_watermark, self.submit_decryption)  # Pass watermarking and decryption functions
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        # Recreate the import
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):        
        # Function to resize the image
        self.image_output.delete("all")
        self.image_output.create_image(event.width / 2, event.height / 2, image=self.image_tk)

    def submit_watermark(self, algorithm, watermark_text):
        """
        This function will be triggered when the user presses the 'Submit' button in the Menu.
        It handles the encryption and embedding process based on the user input.
        """
        encrypted_image_path = "encrypted_image.tiff"  # Path to save encrypted image
        embedded_image_path = "embedded_image.tiff"    # Path to save embedded image
        key = b'pzkUHwYaLVLml0hh'  # Example key; adjust as needed
        block_size = 32            # Example block size; adjust as needed
        data_hiding_key = 1234      # Example data hiding key; adjust as needed

        # Step 1: Encrypt the image
        encrypt_image(self.image_path, encrypted_image_path, key)

        # Step 2: Embed the watermark text
        data_embedding_paper(encrypted_image_path, watermark_text, embedded_image_path, block_size, data_hiding_key)

        # Step 3: Display the watermarked image
        self.image = Image.open(embedded_image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_output.create_image(self.image_output.winfo_width()/2, self.image_output.winfo_height()/2, image=self.image_tk)


    def submit_decryption(self, encrypted_image_path, key, block_size, data_hiding_key):
        # Decrypt the image
        decrypted_image_path = "decrypted_image.tiff"
        output_image_path = "output_image_with_extracted_data.tiff"
        key_bytes = key.encode('utf-8')

        decrypt_image(encrypted_image_path, decrypted_image_path, key_bytes)

        # Extract the watermark
        extracted_message = data_extraction(decrypted_image_path, output_image_path, block_size, data_hiding_key)

        # Display the decrypted image and extracted watermark message
        self.image = Image.open(output_image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_output.create_image(self.image_output.winfo_width() / 2, self.image_output.winfo_height() / 2, image=self.image_tk)

        # Show the extracted watermark message in a label
        self.decrypted_message_label = Label(self, text=f"Extracted Message: {extracted_message}", font=("Helvetica", 12))
        self.decrypted_message_label.grid(row=1, column=1, pady=20)

class Menu(ctk.CTkTabview):
    def __init__(self, parent, submit_watermark_func, submit_decryption_func):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.my_font = ctk.CTkFont(family="Helvetica", weight="bold")

        # Add tabs
        self.add('Watermarking')
        self.add('Decryption')
        self.add('Statistics')

        # Add frames
        WatermarkingFrame(self.tab('Watermarking'), submit_watermark_func)
        DecryptionFrame(self.tab('Decryption'), submit_decryption_func)

class DecryptionFrame(ctk.CTkFrame):
    def __init__(self, parent, submit_decryption_func):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # Add label for decryption image path
        self.image_path_label = ctk.CTkLabel(self, text="Enter path of encrypted image:", font=("Helvetica", 12))
        self.image_path_label.pack(pady=10)

        self.image_path_entry = ctk.CTkEntry(self, width=200)
        self.image_path_entry.pack(pady=10)

        # Add input for decryption key
        self.key_label = ctk.CTkLabel(self, text="Enter decryption key (16 bytes):", font=("Helvetica", 12))
        self.key_label.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, width=200)
        self.key_entry.pack(pady=10)

        # Add block size input
        self.block_size_label = ctk.CTkLabel(self, text="Enter block size:", font=("Helvetica", 12))
        self.block_size_label.pack(pady=10)

        self.block_size_entry = ctk.CTkEntry(self, width=200)
        self.block_size_entry.pack(pady=10)

        # Add data hiding key input
        self.data_hiding_key_label = ctk.CTkLabel(self, text="Enter data hiding key:", font=("Helvetica", 12))
        self.data_hiding_key_label.pack(pady=10)

        self.data_hiding_key_entry = ctk.CTkEntry(self, width=200)
        self.data_hiding_key_entry.pack(pady=10)

        # Add submit button for decryption
        self.submit_button = ctk.CTkButton(
            self, text="Decrypt", 
            command=lambda: submit_decryption_func(
                self.image_path_entry.get(),
                self.key_entry.get(),
                int(self.block_size_entry.get()),
                int(self.data_hiding_key_entry.get())
            )
        )
        self.submit_button.pack(pady=20)

class WatermarkingFrame(ctk.CTkFrame):
    def __init__(self, parent, submit_watermark_func):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # Add watermarking method selection
        self.method_label = ctk.CTkLabel(self, text="Choose Watermarking Algorithm:", font=("Helvetica", 12))
        self.method_label.pack(pady=10)

        self.method_var = ctk.StringVar(value="Algorithm 1")
        self.method_menu = ctk.CTkOptionMenu(self, values=["Algorithm 1", "Algorithm 2"], variable=self.method_var)
        self.method_menu.pack(pady=10)

        # Add input box for watermark text
        self.text_input_label = ctk.CTkLabel(self, text="Enter the text to watermark:", font=("Helvetica", 12))
        self.text_input_label.pack(pady=10)

        self.text_input = ctk.CTkEntry(self, width=200)
        self.text_input.pack(pady=10)

        # Add submit button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=lambda: submit_watermark_func(self.method_var.get(), self.text_input.get()))
        self.submit_button.pack(pady=20)


if __name__ == "__main__":
    App()