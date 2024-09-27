import customtkinter as ctk
import panels

class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')

        self.my_font = ctk.CTkFont(family="Helvetica ", weight = "bold")
        # Add tabs
        self.add('Watermarking')
        self.add('Decryption')
        self.add('Metrics')

        # Add frames
        WatermarkingFrame(self.tab('Watermarking'))
        InputBoxFrame(self.tab('Watermarking'))

class WatermarkingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        panels.WatermarkingMethod(self, 'Choose a method')

class InputBoxFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        panels.InputBox(self)