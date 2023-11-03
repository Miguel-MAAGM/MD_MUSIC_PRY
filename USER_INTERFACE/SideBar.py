from typing import Optional, Tuple, Union
import numpy as np
import customtkinter as ctk


class sideBar(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        #self.grid_rowconfigure((0,1,2,3,4,5), weight=1)  # configure grid system
        #self.grid_columnconfigure((0), weight=1)
        self.state_value=True
        self.state_animation=False



        self.frame=ctk.CTkFrame(self,width=300,height=300,corner_radius=0,fg_color=("#3a7ebf", "#1f538d"))
        self.frame.place(x=0,y=0)
        self.button_toggle=ctk.CTkButton(self.frame,text="TOGLE",corner_radius=0,command=self.change_width)
        self.button_toggle.place(x=0,y=0)
        
        self.button_play=ctk.CTkButton(self.frame,text="PLAY",corner_radius=0)
        self.button_play.place(x=0,y=50)
        
        self.button_Audio=ctk.CTkButton(self.frame,text="Audio",corner_radius=0)
        self.button_Audio.place(x=0,y=100)

        self.button_Config=ctk.CTkButton(self.frame,text="Configuracion",corner_radius=0)
        self.button_Config.place(x=0,y=150)
        
    def change_width(self):
        if self.state_animation==False:
            
            if self.state_value== True:
                self.state_animation=True
                
                self.state_value=False
                self.change_width_animation(self.cget("width"), 200, 200)

            else:
                self.state_animation=True
                self.state_value=True
                self.change_width_animation(self.cget("width" ),50, 200)
        else:

            print("in viaje")

    def change_width_animation(self, current_width, target_width, duration):
        step = (target_width - current_width) / (duration / 10)  # Incremento por cada 10 ms

        self.animate_width(current_width, target_width, step)

    def animate_width(self, current_width, target_width, step):

        if step>0:
            if current_width <= target_width:
                self.configure(width=int(current_width)) 
                self.after(10, self.animate_width, current_width + step, target_width, step)
            else:
                print("end")
                self.state_animation=False
        else:
            if current_width >= target_width:
                self.configure(width=int(current_width)) 
                self.after(10, self.animate_width, current_width + step, target_width, step)
            else:
                print("end")
                self.state_animation=False
