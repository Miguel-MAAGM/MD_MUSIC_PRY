from typing import Optional, Tuple, Union
import numpy as np
import customtkinter as ctk
import pyaudio



class subFrameMic((ctk.CTkFrame)):
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        self.grid_columnconfigure((0,1,2), weight=1)
        self.label_info=ctk.CTkLabel(self,text="Lista de dispositivos")
        self.cmb_lis=ctk.CTkComboBox(self,values=["Device"])
        self.label_info.grid(column=0,row=0,sticky="we")
        self.cmb_lis.grid(column=1,columnspan=2,row=0,sticky="we")
        self.set_list(self.list_device_input())
    def set_list(self,list):
        listB=[]
        for index, name in list:
            listB.append(name)
        self.cmb_lis.configure(values=listB)
    def list_device_input(self):
        p = pyaudio.PyAudio()
        default_host_api = p.get_default_host_api_info()
        audio_input_devices = []

        for i in range(default_host_api['deviceCount']):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                audio_input_devices.append((i, device_info["name"]))
        return audio_input_devices
    
class subFrameFile((ctk.CTkFrame)):
    def __init__(self,master,clb_PLAY=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        self.grid_columnconfigure((0,1,2), weight=1)
        self.ruta=""
        self.btn_FileEx=ctk.CTkButton(self, text="Buscar",command=self.file_expDialog)
        self.entry_FileEx=ctk.CTkEntry(self, placeholder_text="Ruta")
        self.btn_Start=ctk.CTkButton(self,text="PLAY",command=clb_PLAY)
        self.btn_FileEx.  grid(row=0,column=2,padx=20,pady=20,sticky="we")
        self.entry_FileEx.grid(row=0,column=0,padx=20,pady=20,columnspan=2,sticky="we")
        self.btn_Start.grid(row=1,column=2,padx=20,pady=20,sticky="we")

    def file_expDialog(self):
        ruta=ctk.filedialog.askopenfile(title="archivo de audio")
        print(ruta.name)
        self.ruta=ruta.name
        self.entry_FileEx.delete(0,400)
        self.entry_FileEx.insert(0,ruta.name)


class PlayFrame(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.tabview=ctk.CTkTabview(self)
        self.tabview._segmented_button.grid(sticky="nswe")
        
        self.tabview.add("Lectura por archivo")
        self.tabview.add("Lectura por Microfono")
        self.tabview.grid(row=0, column=0, padx=20, pady=20,sticky="nswe")
        self.subFrameMic=subFrameMic(master=self.tabview.tab("Lectura por Microfono"))
        self.subFrameMic.pack(padx=20,pady=20,fill="both",expand=True)
        
        self.subFrameFile=subFrameFile(master=self.tabview.tab("Lectura por archivo"),clb_PLAY=clb_PLAY)
        self.subFrameFile.pack(padx=20,pady=20,fill="both",expand=True)
    def get_Path(self):
        return self.subFrameFile.ruta

import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ctkApp:
        
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.root.update()
        self.frame = ctk.CTkFrame(master=self.root,
                                  height= self.root.winfo_height()*0.95,
                                  width = self.root.winfo_width()*0.66,
                                  fg_color="darkblue")
        self.frame.place(relx=0.33, rely=0.025)
        self.input =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=100,
                                   justify='center',
                                   width=300,
                                   height=50,
                                   fg_color="darkblue")
        self.input.insert(0,100)
        self.input.place(relx=0.025,rely=0.5)
        self.slider = ctk.CTkSlider(master=self.root,
                                    width=300,
                                    height=20,
                                    from_=1,
                                    to=1000,
                                    number_of_steps=999,
                                    command=self.update_surface)
        self.slider.place(relx= 0.025,rely=0.75) 
        self.button = ctk.CTkButton(master = self.root,
                               text="Update Graph",
                               width=300,
                               height=50,
                               command=self.update_window)
        self.button.place(relx=0.025,rely=0.25)
        self.root.mainloop()
    
    def update_window(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(11,5.3)
        global x,y,s,c
        x,y,s,c = np.random.rand(4,int(self.input.get()))
        ax.scatter(x,y,s*self.slider.get(),c)
        ax.axis("off")
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        canvas = FigureCanvasTkAgg(fig,master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        self.root.update()
        
    def update_surface(self,other):
      # Cerrar la figura actual si existe
        plt.close('all')

        fig, ax = plt.subplots()
        fig.set_size_inches(11, 5.3)
        ax.scatter(x, y, s * self.slider.get(), c)
        ax.axis("off")
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        self.root.update()

if __name__ == "__main__":        
    CTK_Window = ctkApp()