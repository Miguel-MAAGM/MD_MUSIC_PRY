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
