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
                             clb_PAUSE=None,
                             combobox_callback=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1,2,3), weight=1)  # configure grid system
        self.grid_columnconfigure((0), weight=1)
        self.btn_Play=ctk.CTkButton(self, text="PLAY",command=clb_PLAY)
        self.btn_Stop=ctk.CTkButton(self, text="STOP",command=clb_STOP)
        self.btn_Pause=ctk.CTkButton(self, text="PAUSE",command=clb_PAUSE)
        self.cm_Box= ctk.CTkComboBox(self,values=["triangular", "rectangular","senoidal"],
                                     command=combobox_callback)
        self.cm_Box.set("triangular")
        self.btn_Play  .grid(row=0, column=0,padx=20,pady=20,sticky="we")
        self.btn_Stop  .grid(row=1, column=0,padx=20,pady=20,sticky="we")
        self.btn_Pause .grid(row=2, column=0,padx=20,pady=20,sticky="we")
        self.cm_Box    .grid(row=3, column=0,padx=20,pady=20,sticky="we")
        
        


class PlayFrame(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None,clb_DATAOUT=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0,1), weight=1)  # configure grid system
        
        self.grid_columnconfigure((0), weight=100)
        self.grid_columnconfigure((1), weight=40)
        self.clb_DAtaOut=clb_DATAOUT
        self.tabview=ctk.CTkTabview(self)
        self.FFTWindow=fftF.canvasMat(self)
        self.WaveFunction=wFrame.waveFrame(self)
        self.panel= btPlayFrame(self,self.actionPlay,self.actionStop,self.actionPuse,combobox_callback=self.clb_cmBox)
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
        self.countTime=0
        self.fft_out=0
        self.countTimeRender=0        
        self.redermi_hilo =threading.Thread(target=self.WaveFunction.render)
        self.waveType="triangular"

        self.WaveFunction.visualizar_onda(self.waveType)
        points=self.WaveFunction.getPoints(50,4)
        out=self.prepareData(points,[0,0,0,0])
        self.clb_DAtaOut(out)
        self.WaveFunction.visualizar_recta(points)
        self.WaveFunction.render()

    def prepareData(self, points,power):
        signal = [tupla[1] for tupla in points]
        resultado = [list(map(float, x)) for x in zip(power, signal)]
        return resultado
    
    def clb_cmBox(self,choice):
        print(choice)
        self.waveType=choice
        self.WaveFunction.clear()

        self.WaveFunction.visualizar_onda(self.waveType)
        self.WaveFunction.idx=0
        points=self.WaveFunction.getPoints(50,4)
        self.WaveFunction.visualizar_recta(points)
        out=self.prepareData(points,[0,0,0,0])
        self.clb_DAtaOut(out)
        self.WaveFunction.render()
        
    def clb_wav_play(self,data):

        if((self.size<1024)):
            self.buffer.extend(data)
            self.size+=len(data)
        else:
            del self.buffer[0:1024]
            self.buffer.extend(data)

            
        if self.countTime <50:
            self.countTime+=1

        else:
            self.countTime=0

            self.fft_out=self.FFTWindow.compute(self.buffer,4)

            self.FFTWindow.animation()
            
        if  self.countTimeRender<325:
            self.countTimeRender+=1
        else:
            self.WaveFunction.clear()
            points=self.WaveFunction.getPoints(50,4)
            self.WaveFunction.visualizar_onda(self.waveType)
            self.WaveFunction.visualizar_recta(points)
            self.WaveFunction.render()
            self.countTimeRender=0
            signal = [tupla[1] for tupla in points]
            resultado = [list(map(float, x)) for x in zip(self.fft_out, signal)]
            #print(data)
            self.clb_DAtaOut(resultado)
            #self.WaveFunction.clear()
            #self.WaveFunction.visualizar_onda(self.waveType)
            #x_intersecciones, y_intersecciones=self.WaveFunction.visualizar_recta(4,0.005,self.ofset)
            #valor_medio = np.mean(fft_out[::500])*10
            
            ##print(str(x_intersecciones)+" "+str(y_intersecciones))
            #self.ofset+=0.0001
            #if self.ofset>(0.1-(0.005*3)):
            #    self.ofset=0
            #self.WaveFunction.render()
            #self.buffer=[]
            #self.size=0
            
    def clb_wav_finish(self):
        points=self.WaveFunction.getPoints(50,4)
        out=self.prepareData(points,[0,0,0,0])
        self.clb_DAtaOut(out)
        self.actionStop()


        
    def clb_mic_play(self,data,chunk):
        self.buffer.extend(data)
        self.size+=len(data)
        if((self.size>1024*10)):
            print(str(len(data))+"--------")
            #self.FFTWindow.compute(self.buffer,4)
            #self.FFTWindow.animation()
            #self.WaveFunction.clear()
            #self.WaveFunction.visualizar_onda(self.waveType)
            #cordenada=[x_intersecciones, y_intersecciones]
            #self.clb_DAtaOut(cordenada)
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
            self.Wav.start_audio_file(self.subFrameFile.ruta,)
           

    def actionPuse(self):

        self.Wav.toggle_pause()
        
    
    def actionStop(self):
        self.tabview._segmented_button.configure(state=ctk.NORMAL)
        self.Wav.stop()    
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