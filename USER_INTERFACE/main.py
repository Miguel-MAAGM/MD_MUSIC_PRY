
import signal
import sys
import ServerAdmin as srvAd
import SideBar as SdB
import numpy as np
import customtkinter as ctk
import AudioinFrame as AdI
import infDevFrame as iDF
import inAudioDevDect as Audio
import librosa
import ServerAdmin
import struct
# Dirección IP y puerto en localhost
# Ejemplo de uso
def signal_handler(sig, frame):
    print("Se ha recibido la señal SIGINT (Ctrl+C). Realizando tareas de cierre...")
    sys.exit(0)
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        toServer= ServerAdmin.ClientSocket("localHost",122345,receive_callback=self.callBack_Server)

        self.geometry("1080x720")
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_rowconfigure((1), weight=100)  # configure grid system
        self.grid_columnconfigure((0), weight=1)
        self.UP_bar= ctk.CTkFrame(master=self,fg_color=("#3a7ebf"),width= 200, height= 50,corner_radius=0)
        self.UP_bar.grid(row=0, column=0, padx=0,pady=0,sticky="NEW")
        segemented_button = ctk.CTkSegmentedButton(self.UP_bar, values=["PLAY", "CONFIG"],
                                                     command=self.segmented_button_callback,bg_color="transparent",fg_color="#3a7ebf",
                                                     unselected_color="#3a7ebf")
        segemented_button.pack(pady=20)
        segemented_button.set("PlAY")  # set initial value
        self.AudioManagerFile=Audio.AudioManagerFile(callback_data=self.Clb_Audio,callback_finish=self.finish_Song)
        self.AudioFrame= AdI.PlayFrame(self,clb_PLAY=self.PLAY)
        self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 

        self.ConfigFrame= iDF.infDevFrame(self)
        self.ConfigFrame.list_dev(["VALOR1","VALOR2","VALOR3",])
        self.count=0
        self.frame=[]
    def segmented_button_callback(self,value):
        print("segmented button clicked:", value)   
        if value== "PLAY":
            self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 
            self.ConfigFrame.grid_forget()

            print("PLAY")

        else:
            self.AudioFrame.grid_forget()
            self.ConfigFrame.grid(row=1,column=0,sticky ="NSWE") 

            print("OTHER")
    
    def PLAY(self):
        self.AudioManagerFile.play(self.AudioFrame.get_Path())
    def Clb_Audio(self,data):

        if(self.count<100):
            self.frame.append(np.frombuffer(data, dtype=np.int16))
            self.count=self.count+1
        else:
            audio_data = np.concatenate(self.frame)
            audio_data = audio_data.astype(float)
            #tempo, beats = librosa.beat.beat_track(y=audio_data.astype(float), sr=self.AudioManagerFile.get_rate())
            audio_data_fast = librosa.effects.time_stretch(audio_data, rate=2)
            # Estima el tempo del audio acelerado
            tempo_fast, _ = librosa.beat.beat_track(y=audio_data_fast, sr=self.AudioManagerFile.get_rate())
            self.count=0
            self.frame=[]
            print(tempo_fast)
    def finish_Song(self):
        self.count=0
        self.frame=[]
        print("FINISH SONG")
    def callBack_Server(self,data):
        print(data)

 
if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)
    
    app = App()
    app.mainloop()


