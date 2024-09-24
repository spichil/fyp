import customtkinter as ctk
from tkinter import Label
from image_widgets import *
from PIL import Image, ImageTk
from menu import * 

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
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)

        # reset the grid
        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        # Close button to choose another image
        self.close_button = CloseOutput(self, self.close_edit)

        # Menu for settings
        self.menu = Menu(self)
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        # Recreate the import
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):        
        # Function to resize the image
        self.image_output.delete("all")
        self.image_output.create_image(event.width/2,event.height/2, image = self.image_tk)


App()