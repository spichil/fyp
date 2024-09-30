import customtkinter as ctk
from tkinter import Label
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from image_widgets import *  # Assuming this contains your custom widgets
from menu import *  # Assuming this handles additional UI elements
from reversible_data_hiding.image_encryption2 import encrypt_image  # Your encryption logic
from reversible_data_hiding.data_embedding import data_embedding_paper  # Your embedding logic
from reversible_data_hiding.ch_data_extraction_ver1 import decrypt_image, data_extraction  # Your decryption and extraction logic
from reversible_data_hiding.evaluate import calculate_psnr, plot_multiple_ber, run_experiment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        # Statistics frame placeholder
        self.statistics_frame = None

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

        # Calculate PSNR value
        psnr_value = calculate_psnr(self.image_path, embedded_image_path)

        # Update PSNR in the Statistics tab
        if self.statistics_frame is not None:
            self.statistics_frame.update_psnr(psnr_value)

    def submit_decryption(self, encrypted_image_path, key, block_size, data_hiding_key):
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

        # Pass paths for statistics update
        if self.statistics_frame:
            self.statistics_frame.set_paths(self.image_path, decrypted_image_path)

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
        parent.statistics_frame = StatisticsFrame(self.tab('Statistics'))
        
class StatisticsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')
        self.original_image_path = None
        self.decrypted_image_path = None

        # PSNR and BER labels
        self.psnr_label = ctk.CTkLabel(self, text="PSNR: N/A", font=("Helvetica", 12))
        self.psnr_label.pack(pady=10)

        self.ber_label = ctk.CTkLabel(self, text="BER: N/A", font=("Helvetica", 12))
        self.ber_label.pack(pady=10)

        # Button to calculate and show statistics
        self.stat_button = ctk.CTkButton(self, text="Calculate Statistics", command=self.calculate_and_show_statistics)
        self.stat_button.pack(pady=20)

        # Placeholder for the graph
        self.canvas = None

    # Add this method to set the paths
    def set_paths(self, original_image_path, decrypted_image_path):
        self.original_image_path = original_image_path
        self.decrypted_image_path = decrypted_image_path

    def calculate_and_show_statistics(self):
        if self.original_image_path is None or self.decrypted_image_path is None:
            print("Error: Image paths not set!")
            return

        # Sample Parameters
        block_sizes = [4, 8, 16, 32, 64]
        data_hiding_key = 1234
        key = b'pzkUHwYaLVLml0hh'
        secret_data = 'Secret'
        output_path = 'recovered_image.tiff'

        # Call run_experiment to calculate PSNR and BER
        block_sizes, ber_values = run_experiment(self.original_image_path, output_path, secret_data, key, block_sizes, data_hiding_key)

        # Calculate and show PSNR
        psnr_value = calculate_psnr(self.original_image_path, self.decrypted_image_path)
        self.psnr_label.configure(text=f"PSNR: {psnr_value:.2f} dB")

        # Update BER value (for block size 32 as an example)
        ber_value = ber_values[block_sizes.index(32)]
        self.ber_label.configure(text=f"BER: {ber_value:.2f}%")

        # Plot BER graph using plot_multiple_ber
        self.plot_ber_graph(block_sizes, [ber_values], [self.original_image_path])

    def plot_ber_graph(self, block_sizes, ber_results, image_names):
        # Create a figure and plot the BER
        fig, ax = plt.subplots(figsize=(6, 4))
        for ber_values, image_name in zip(ber_results, image_names):
            ax.plot(block_sizes, ber_values, marker='o', label=image_name)

        ax.set_title('Extracted-Bit Error Rate with Respect to Block Sizes')
        ax.set_xlabel('Block Size')
        ax.set_ylabel('Extracted-bit Error Rate (%)')
        ax.grid(True)

        # If a canvas already exists, clear it first
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        # Create a canvas for the figure
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20)


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
