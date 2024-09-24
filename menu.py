import customtkinter as ctk

class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')

        # Add tabs
        self.add('Watermarking')
        self.add('Statistics')

        WatermarkingFrame(self.tab('Watermarking'))

class WatermarkingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')