
import matplotlib.pyplot as plt
import signal
import sys
import ServerAdmin as srvAd
import SideBar as SdB
import numpy as np
import customtkinter as ctk

# Dirección IP y puerto en localhost
# Ejemplo de uso
def receive_callback(data):
    print("Dato recibido:", data)

def signal_handler(sig, frame):
    print("Se ha recibido la señal SIGINT (Ctrl+C). Realizando tareas de cierre...")
    
    sys.exit(0)
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=100)

        self.sideBar= SdB.sideBar(self,width=75,fg_color=("#3a7ebf", "#1f538d"),corner_radius=0)
        self.sideBar.grid(row=0,column=0,sticky="nsw")

        self.frame1=ctk.CTkFrame(self,fg_color="red")
        self.frame1.grid(row=0,column=1,sticky="nswe")
        self.btn_ext=ctk.CTkButton(self.frame1,text="toggle",command=self.sideBar.change_width)        
        self.btn_ext.pack()
        
       




if __name__ == "__main__":
    # Crear un socket
    #client = srvAd.ClientSocket('localhost', 12345, receive_callback)
    #client.connect()
    signal.signal(signal.SIGINT, signal_handler)
    app = App()
    app.mainloop()


