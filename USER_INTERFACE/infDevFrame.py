# Draggable rectangle with blitting.
import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def only_numbers(char):
    return char.isdigit()or char=="."

class listDevFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.label_Title=ctk.CTkLabel(self,text="Lista de torres", fg_color="gray30",corner_radius=10)
        self.label_Title.grid(row=0, column=0,padx=10,pady=10,columnspan=2,sticky="nsew")

        self.cmb_boxListDev =ctk.CTkComboBox(self)
        self.Btn_Refresh    =ctk.CTkButton(self,text="Refresh",command=self.refreshListDev)
        self.Btn_GET        =ctk.CTkButton(self,text="Get data")
        self.Btn_SET        =ctk.CTkButton(self,text="Set data")

        self.cmb_boxListDev.grid(row=1, column=0,padx=20,pady=20)
        self.Btn_Refresh.grid(row=2, column=0,padx=10,pady=10)
        self.Btn_GET.grid(row=3, column=0,padx=10,pady=10)
        self.Btn_SET.grid(row=4, column=0,padx=10,pady=10)
    def refreshListDev(self):
        self.cmb_boxListDev.configure(values=["new value 1", "new value 2"])



        
class cofingDevFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.label_Title=ctk.CTkLabel(self,text="Configuracion de torre", fg_color="gray30",corner_radius=10)
        self.label_Title.grid(row=0, column=0,padx=10,pady=10,columnspan=2,sticky="nsew")

        self.label_Speed  =ctk.CTkLabel(self,text              ="Speed MAX (mm/s):")
        self.label_AccPSec=ctk.CTkLabel(self,text="Acceleration per second (mm/s ):")
        self.label_DecPsec=ctk.CTkLabel(self,text="Deceleration per second (mm/s ):")
        self.label_StpPMel=ctk.CTkLabel(self,text    ="Step per millimeter (Count):")
        self.label_StpPRev=ctk.CTkLabel(self,text    ="Step per revolution (Count):")
        validation=master.register(only_numbers)

        self.entry_Speed  =ctk.CTkEntry(self, validate='key',validatecommand=(validation, '%S'))
        self.entry_AccPSec =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_DecPsec =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_StpPMel =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_StpPRev =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        
        self.label_Speed.grid(  row=1, column=0,padx=20,sticky="we")
        self.label_AccPSec.grid(row=2, column=0,padx=20,sticky="we")
        self.label_DecPsec.grid(row=3, column=0,padx=20,sticky="we")
        self.label_StpPMel.grid(row=4, column=0,padx=20,sticky="we")
        self.label_StpPRev.grid(row=5, column=0,padx=20,sticky="we")

        self.entry_Speed  .grid(row=1, column=1,padx=20,sticky="we")
        self.entry_AccPSec.grid(row=2, column=1,padx=20,sticky="we")
        self.entry_DecPsec.grid(row=3, column=1,padx=20,sticky="we")
        self.entry_StpPMel.grid(row=4, column=1,padx=20,sticky="we")
        self.entry_StpPRev.grid(row=5, column=1,padx=20,sticky="we")
        #setSpeedInStepsPerSecond
        #setAccelerationInStepsPerSecondPerSecond
        #setDecelerationInStepsPerSecondPerSecond
        #setStepsPerMillimeter
        #
        #
        #
        #

class infDevFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        
        # add widgets onto the frame...

        self.text_InfoDevText=ctk.CTkTextbox(self) 
        self.entry_infoDevText=ctk.CTkEntry(self,placeholder_text="Command to tower")
        self.BTNentry_infoDev=ctk.CTkButton(self,text="Send",command=self.newEvent) 
        self.cofingDevFrame = cofingDevFrame(self)
        self.listDevFrame =listDevFrame(self)
        self.count=0
        self.listDevFrame.grid(row=0, column=2,padx=20,pady=20,sticky="nsew")
        self.cofingDevFrame.grid(row=0, column=0,padx=20,pady=20,columnspan=2,sticky="nsew")
        self.text_InfoDevText.grid(row=1, padx=20, columnspan=3,sticky="nsew")
        self.entry_infoDevText.grid(row=2,column=0,padx=20,columnspan=2,sticky="ew")
        self.BTNentry_infoDev.grid(row=2,column=2,padx=20,sticky="ew")

        self.text_InfoDevText.insert("0.0","-> |"+"Console Log with server..."+"\n")
        self.text_InfoDevText.configure(state="disabled")  
    def newEvent(self):
        self.text_InfoDevText.configure(state="normal")
        self.text_InfoDevText.insert("0.0",f"<- {self.count} |"+"Console Log with server... event "+"\n")
        self.count=self.count+1
        self.text_InfoDevText.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.UP_bar= ctk.CTkFrame(master=self,fg_color=("#3a7ebf"),width= 200, height= 50,corner_radius=0)
        self.UP_bar.grid(row=0, column=0, padx=0,pady=0,sticky="NEW")
        self.my_frame = infDevFrame(master=self)
        self.my_frame.grid(row=1,rowspan=5, column=0, padx=20,pady=20 ,sticky="NSEW")
if __name__ == "__main__":
    app = App()
    app.mainloop()



