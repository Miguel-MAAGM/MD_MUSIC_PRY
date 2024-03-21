import numpy as np
import customtkinter as ctk
import pyaudio
import os
from . import waveFrame as wFrame
from . import inAudioDevDect as auDev
from . import FFTframe as fftF

import threading
class subFrameMic((ctk.CTkFrame)):
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1), weight=1)  # configure grid system
        self.grid_columnconfigure((0,1), weight=1)
        self.label_info=ctk.CTkLabel(self,text="Lista de dispositivos")
        self.cmb_lis=ctk.CTkComboBox(self,values=["Device"])
        self.label_info.grid(column=0,row=0,padx=20,pady=20,columnspan=2,sticky="we")
        self.cmb_lis.grid(column=0,row=1,padx=20,pady=20,columnspan=2,sticky="we")
        self.list=[]
        self.set_list(self.list_device_input())
    def set_list(self,list):
        self.list=[]
        for index, name in list:
            self.list.append(name)
        self.cmb_lis.configure(values=self.list)
    def list_device_input(self):
        p = pyaudio.PyAudio()
        default_host_api = p.get_default_host_api_info()
        audio_input_devices = []

        for i in range(default_host_api['deviceCount']):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                audio_input_devices.append((i, device_info["name"]))
        return audio_input_devices
    def index(self):
        return self.list.index(self.cmb_lis.get())
        
class subFrameFile((ctk.CTkFrame)):
    def __init__(self,master,clb_PLAY=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_columnconfigure((0,1,2), weight=1)
        self.ruta=""
        self.btn_FileEx=ctk.CTkButton(self, text="Buscar",command=self.file_expDialog)
        self.entry_FileEx=ctk.CTkEntry(self, placeholder_text="Ruta")
        #self.btn_Start=ctk.CTkButton(self,text="PLAY",command=clb_PLAY)
        self.btn_FileEx.  grid(row=0,column=2,padx=20,pady=20,sticky="we")
        self.entry_FileEx.grid(row=0,column=0,padx=20,pady=20,columnspan=2,sticky="we")
        #self.btn_Start.grid(row=1,column=2,padx=20,pady=20,sticky="we")

    def file_expDialog(self):
        ruta=ctk.filedialog.askopenfile(title="archivo de audio")
        print(ruta.name)
        self.ruta=ruta.name
        self.entry_FileEx.delete(0,400)
        file = os.path.basename(ruta.name)
        self.entry_FileEx.insert(0,file)

class btPlayFrame(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None,
                             clb_STOP=None,
                             clb_PAUSE=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        self.grid_columnconfigure((0), weight=1)
        self.btn_Play=ctk.CTkButton(self, text="PLAY",command=clb_PLAY)
        self.btn_Stop=ctk.CTkButton(self, text="STOP",command=clb_STOP)
        self.btn_Pause=ctk.CTkButton(self, text="PAUSE",command=clb_PAUSE)
        self.btn_Play  .grid(row=0, column=0,padx=20,pady=20,sticky="we")
        self.btn_Stop  .grid(row=1, column=0,padx=20,pady=20,sticky="we")
        self.btn_Pause .grid(row=2, column=0,padx=20,pady=20,sticky="we")
       
        
        


class PlayFrame(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1), weight=1)  # configure grid system
        
        self.grid_columnconfigure((0), weight=100)
        self.grid_columnconfigure((1), weight=40)

        self.tabview=ctk.CTkTabview(self)
        self.FFTWindow=fftF.canvasMat(self)
        self.WaveFunction=wFrame.waveFrame(self)
        self.panel= btPlayFrame(self,self.actionPlay,self.actionStop,self.actionPuse)
        self.Wav=auDev.AudioManagerFile("",self.clb_wav_play,self.clb_wav_finish)
        self.Mic=auDev.AudioManagerMic(self.clb_mic_play)
        
        self.FFTWindow.grid(row=0, column=0,padx=20,pady=20,sticky="nswe")
        self.WaveFunction.grid(row=1, column=0,padx=20,pady=20,sticky="nswe")
        self.panel.grid(row=1,column=1,padx=20,pady=20,sticky="nswe")
        self.tabview._segmented_button.grid(sticky="we")
        
        self.tabview.add("Lectura por archivo")
        self.tabview.add("Lectura por Microfono")
        self.tabview.grid(row=0, column=1,padx=20,pady=20,sticky="nswe")
        self.subFrameMic=subFrameMic(master=self.tabview.tab("Lectura por Microfono"))
        self.subFrameMic.pack(padx=20,pady=20,expand=True)
        
        self.subFrameFile=subFrameFile(master=self.tabview.tab("Lectura por archivo"),clb_PLAY=clb_PLAY)
        self.subFrameFile.pack(padx=20,pady=20,expand=True)
        self.typeOfStream=""
        self.buffer=[]
        self.size=0
        self.ofset=0
        self.redermi_hilo =threading.Thread(target=self.WaveFunction.render)
    def clb_wav_play(self,data):
        self.buffer.extend(data)
        self.size+=len(data)
        if((self.size>1024*4)):
            self.FFTWindow.compute(self.buffer,4)
            self.FFTWindow.animation()
            self.WaveFunction.clear()
            self.WaveFunction.visualizar_onda("triangular")
            x_intersecciones, y_intersecciones=self.WaveFunction.visualizar_recta(4,0.005,self.ofset)
            #print(str(x_intersecciones)+" "+str(y_intersecciones))
            self.ofset+=0.0001
            if self.ofset>(0.1-(0.005*3)):
                self.ofset=0
            self.WaveFunction.render()
            self.buffer=[]
            self.size=0

    def clb_wav_finish(self):
        self.FFTWindow.clear()

        self.actionStop()
        
        
    def clb_mic_play(self,data,chunk):
        self.buffer.extend(data)
        self.size+=len(data)
        if((self.size>1024*4)):
            print(str(len(data))+"--------")
            self.FFTWindow.compute(self.buffer,4)
            self.FFTWindow.animation()
            self.WaveFunction.clear()
            self.WaveFunction.visualizar_onda("triangular")
            x_intersecciones, y_intersecciones=self.WaveFunction.visualizar_recta(4,0.005,self.ofset)
            #print(str(x_intersecciones)+" "+str(y_intersecciones))
            self.ofset+=0.001
            if self.ofset>(0.1-(0.005*3)):
                self.ofset=0
            self.WaveFunction.render()
            self.buffer=[]
            self.size=0

    def get_Path(self):
        return self.subFrameFile.ruta
    def actionPlay(self):
        self.typeOfStream=self.tabview._segmented_button.get()
        self.tabview._segmented_button.configure(state=ctk.DISABLED)
        if self.typeOfStream=="Lectura por Microfono":
            
       
            self.Mic.start_recording(self.subFrameMic.index())
        elif self.typeOfStream=="Lectura por archivo":
            print("ARCHIVO")
            print(self.subFrameFile.ruta)
            self.Wav.start_audio_file(self.subFrameFile.ruta,)
           

    def actionPuse(self):

        self.Wav.toggle_pause()
        
        print("Pause")
    
    def actionStop(self):
        self.tabview._segmented_button.configure(state=ctk.NORMAL)
        if(not self.Wav.is_finish):
            print("aa")
            self.Wav.stream.stop_stream()
            self.Wav.stream.close() 
        self.Mic.stop()   
        print("STOP")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.PlayFra=PlayFrame(self)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.PlayFra.grid(row=0, column=0, padx=20, pady=20,sticky="nswe")#
    def close(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
##