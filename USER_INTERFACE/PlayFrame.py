# Draggable rectangle with blitting.
import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class gri2dPlot(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)


class gridPlot(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()
