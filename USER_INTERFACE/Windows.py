# Draggable rectangle with blitting.
import NOAA_DATA
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MyPanel(ctk.CTkFrame):
    def __init__(self, master, round=10):
        super().__init__(master)
        self._border_width=5
        self._corner_radius=round
        # add widgets onto the frame, for example:
        self.pos=200
        self.end_pos=100
        self.in_start_pos=True
        self.label = ctk.CTkLabel(self,text="CH 1")
        self.label.grid(row=0, column=0, padx=20,pady=10,sticky="nsew")
        self.PgBar=ctk.CTkSlider(self, orientation="vertical")
        self.PgBar.grid(row=1, column=0, padx=20,pady=0,sticky="nsew")
        self.Status = ctk.CTkButton(self,text="",width=30,height=30,corner_radius=30,command=self.animate)
        self.Status.grid(row=2, column=0, padx=0,pady=10)
        self.start_pos = 100 + 0.04
    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        print("VAMOS")
        if self.pos > self.end_pos:
            self.pos -=1
            self.width=self.pos
            print(self.pos)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False
                  
    def animate_backwards(self):
        print("VAMOS2")
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

        


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.myFrame=MyPanel(self,round=100)
        self.myFrame.pack()
        self.frame= ctk.CTkFrame(self,
                                 width=200,
                                 height=200,
                                 corner_radius=20,
                                 bg_color="yellow")
        self.frame.pack(padx=20,pady=20)
        self.btn1=ctk.CTkButton(self.frame,text="hola")
        self.btn1.place(relx=1,rely=0.3,anchor="center")


app = App()
app.mainloop()

