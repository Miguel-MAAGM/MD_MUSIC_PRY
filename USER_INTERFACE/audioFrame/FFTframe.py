import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
from scipy.fft import fft
import random
class canvasMat(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.root = master
        self.fig, self.ax = plt.subplots()
        
        self.ax.grid(True)
        self.ax.set_ylim(0, 1) 
        self.ax.grid(True,color="#f3f6f4")
        self.fig.set_facecolor("#212121")
        self.ax.set_facecolor("#212121")
        self.ax.tick_params(axis='x', colors='#f3f6f4')  # Cambiar color de los ejes X a rojo
        self.ax.tick_params(axis='y', colors='#f3f6f4')  # Cambiar color de los ejes Y a verde
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_canvas.get_tk_widget().grid(row=0,column=0,padx=20,pady=20,sticky="nswe")
        self.animation_id = None  # Variable para almacenar el ID del temporizador
        self.counter = 0
        self.x_data = []
        self.y_data = []
        self.pilar =0
        
        self.promedios_partes=[]
        self.animation()

    def compute(self,frame,pilar):
        self.pilar=pilar
        # Calcula la FFT del frame
        fft_frame = fft(frame)

        # Calcula el valor absoluto de la FFT
        abs_fft_frame = np.abs(fft_frame)
        ##log_fft_frame = np.log10(abs_fft_frame + 1)

        # Normaliza los valores absolutos de la FFT
        normalized_fft_frame = abs_fft_frame / np.max(abs_fft_frame)
        self.promedios_partes =normalized_fft_frame[:len(frame)//5] 
        
        return  self.promedios_partes
        # Divide el frame en cuatro partes
        ##longitud_parte = len(normalized_fft_frame) // pilar
        ##partes = [normalized_fft_frame[i:i+longitud_parte] for i in range(0, len(normalized_fft_frame), longitud_parte)]

        # Calcula el promedio de cada parte
        ##self.promedios_partes  = [np.mean(parte) / np.max(abs_fft_frame) for parte in partes]  # Normaliza los promedios
                  
    def generate_string_list(self,num):
        string_list = []
        for i in range(1, num + 1):
            string_list.append("Pilar " + str(i))
        return string_list
    def animation(self):
        
    
        self.counter+=1
        self.ax.clear()
        
        self.ax.grid(True,color="#f3f6f4")
        self.fig.set_facecolor("#212121")
        self.ax.set_facecolor("#212121")
        self.ax.tick_params(axis='x', colors='#f3f6f4')  # Cambiar color de los ejes X a rojo
        self.ax.tick_params(axis='y', colors='#f3f6f4')  # Cambiar color de los ejes Y a verde
        #partes_labels = self.generate_string_list(self.pilar)
        print(len(self.promedios_partes))
        self.ax.plot(range(len(self.promedios_partes)), self.promedios_partes)
        self.plot_canvas.draw()
    def clear(self):
        self.ax.clear()
        self.plot_canvas.draw()



def generar_señal(fs, duracion, f1, f2, f3, f4, A1=1, A2=1000, A3=1, A4=1):
    t = np.linspace(0, duracion, int(fs * duracion))
    señal = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t) + A3 * np.sin(2 * np.pi * f3 * t) + A4 * np.sin(2 * np.pi * f4 * t)
    return t, señal
# Ejemplo de uso
# Generar un frame de ejemplo (usando datos aleatorios)
fs = 44000  # Frecuencia de muestreo
duracion = 1  # Duración de la señal en segundos
f1 = 0  # Frecuencia del primer tono
f2 = 0  # Frecuencia del segundo tono
f3 = 20000  # Frecuencia del tercer tono
f4 = 0  # Frecuencia del cuarto tono
def generate_random_number():
    return random.randint(0, 20000)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")

        self.PlayFra=canvasMat(self)
    
        self.PlayFra.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.animation_id=None
        

        self.rpi()
    def close(self):
        if self.animation_id:
            self.after_cancel(self.animation_id) 
        self.quit()
        self.destroy()
        
    def rpi(self):
        t, señal = generar_señal(fs,duracion, random.randint(0, 20000),random.randint(0, 20000),random.randint(10000, 20000),random.randint(1000, 20000))
        self.PlayFra.compute(señal,4)
        self.PlayFra.animation()
        self.animation_id = self.after(1000, self.rpi)
if __name__ == "__main__":
    app = App()

    app.mainloop()
##