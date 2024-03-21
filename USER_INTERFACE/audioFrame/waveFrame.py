import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class waveFrame(ctk.CTkFrame):
    def __init__(self,master,clb_PLAY=None, fs=1000, T=0.10,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.root=master
        self.fs = fs
        self.T = T
        self.t = np.linspace(0, T, int(T * fs))  # Tiempo de la señal
        self.fig, self.ax = plt.subplots()
        self.tipo_onda="Triangular"
        self.ax.grid(True)
        self.ax.grid(True,color="#f3f6f4")
        self.fig.set_facecolor("#212121")
        self.ax.set_facecolor("#212121")
        self.ax.tick_params(axis='x', colors='#f3f6f4')  # Cambiar color de los ejes X a rojo
        self.ax.tick_params(axis='y', colors='#f3f6f4')  # Cambiar color de los ejes Y a verde
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self)

        #self.combobox = ctk.CTkComboBox(self,values=["triangular", "rectangular","senoidal","None"],
        #                                     command=self.combobox_callback)
        #self.combobox.grid(column=0,row=1,padx=20,sticky="W")

        self.plot_canvas.get_tk_widget().grid(column=0,row=0,padx=20,pady=20,sticky="nswe")
        self.animation_id = None  # Variable para almacenar el ID del temporizador
        
        
        #self.combobox.set("senoidal")  # set initial value
            
    def generar_onda(self, tipo):
        if tipo == "triangular":
            # Señal triangular
            triangular_freq = 40  # Frecuencia de la señal triangular (Hz)
            triangular_amplitude = 1.0  # Amplitud de la señal triangular
            signal = triangular_amplitude * (2 * np.abs((self.t * triangular_freq) % 1) - 1)

        elif tipo == "rectangular":
            # Señal rectangular
            rectangular_freq = 40  # Frecuencia de la señal rectangular (Hz)
            rectangular_duty_cycle = 0.5  # Ciclo de trabajo de la señal rectangular
            signal = np.where(np.mod(self.t * rectangular_freq, 1) < rectangular_duty_cycle, 1.0, -1.0)

        elif tipo == "senoidal":
            # Señal senoidal
            sinusoidal_freq = 20  # Frecuencia de la señal senoidal (Hz)
            sinusoidal_amplitude = 0.8  # Amplitud de la señal senoidal
            signal = sinusoidal_amplitude * np.sin(2 * np.pi * sinusoidal_freq * self.t)
        elif tipo== "None":
            self.t=0
            signal=0
        else:
            raise ValueError("Tipo de onda no válido. Debe ser 'triangular', 'rectangular' o 'senoidal'.")

        return self.t, signal

    def generar_rectas_verticales(self, num_lineas, separacion,ofset):
        x_intersecciones = [i * separacion + ofset for i in range(num_lineas)]
        y_intersecciones = []

        for x_interseccion in x_intersecciones:
            idx = np.abs(self.t - x_interseccion).argmin()
            y_interseccion = self.signal[idx]
            y_intersecciones.append(y_interseccion)

        return x_intersecciones, y_intersecciones

    def visualizar_onda(self, type):
        self.tipo_onda=type
        self.t, self.signal = self.generar_onda(self.tipo_onda)
        self.ax.plot(self.t, self.signal, label=f'Onda {self.tipo_onda.capitalize()}')

    def visualizar_recta(self,num_lineas, separacion,ofset):
        colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Colores disponibles
        x_intersecciones, y_intersecciones = self.generar_rectas_verticales(num_lineas, separacion,ofset)
        self.ax.scatter(x_intersecciones, y_intersecciones, color='red', label='Intersecciones')
        for i in range(num_lineas):
            x_linea = i * separacion+ofset
            color = colores[i % len(colores)]  # Seleccionar color de forma cíclica
            self.ax.axvline(x=x_linea, color=color, linewidth=2)

        return x_intersecciones, y_intersecciones
    def render(self):
        #self.ax.grid(True,color="#f3f6f4")
        self.fig.set_facecolor("#212121")
        self.ax.set_facecolor("#212121")
        self.ax.set_ylim(-1, 1) 
        self.ax.set_xlim(0, 0.1) 
        
        self.ax.tick_params(axis='x', colors='#f3f6f4')  # Cambiar color de los ejes X a rojo
        self.ax.tick_params(axis='y', colors='#f3f6f4')  # Cambiar color de los ejes Y a verde
        self.plot_canvas.draw()
    def clear(self):
        self.ax.clear()



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.grid_rowconfigure((0), weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.PlayFra=waveFrame(self)
        self.ofset=0
        self.PlayFra.grid(column=0,row=0,sticky="nswe")
        self.PlayFra.visualizar_onda()
        self.PlayFra.visualizar_recta(4,0.005,self.ofset)
        self.PlayFra.render() 
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.animation_id=None
        self.rpi()
    def close(self):
        if self.animation_id:
            self.after_cancel(self.animation_id) 
        self.quit()
        self.destroy()
        
    def rpi(self):
        
        self.PlayFra.clear()
        
        self.PlayFra.visualizar_onda()
        x_intersecciones, y_intersecciones=self.PlayFra.visualizar_recta(4,0.005,self.ofset)
        print(str(x_intersecciones)+" "+str(y_intersecciones))
        self.PlayFra.render() 
        
        if self.ofset>(0.1-(0.005*3)):
            self.ofset=0

        self.ofset+=0.001

        self.animation_id = self.after(10, self.rpi)



if __name__ == "__main__":
    app = App()

    app.mainloop()
##