import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

def procesar_frame(frame,pilar):
    # Calcula la FFT del frame
    fft_frame = fft(frame)
    
    # Calcula el valor absoluto de la FFT
    abs_fft_frame = np.abs(fft_frame)
    
    # Normaliza los valores absolutos de la FFT
    normalized_fft_frame = abs_fft_frame / np.max(abs_fft_frame)
    normalized_fft_frame =normalized_fft_frame[:len(frame)//2] 
    
    # Divide el frame en cuatro partes
    longitud_parte = len(normalized_fft_frame) // pilar
    partes = [normalized_fft_frame[i:i+longitud_parte] for i in range(0, len(normalized_fft_frame), longitud_parte)]
    
    # Calcula el promedio de cada parte
    promedios_partes = [np.mean(parte) for parte in partes]
    
    return promedios_partes
def generar_señal(fs, duracion, f1, f2, f3, f4, A1=1, A2=1, A3=1, A4=1):
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
t, señal = generar_señal(fs, duracion, f1, f2, f3, f4)


# Procesar el frame
promedios_partes = procesar_frame(señal,4)
print(promedios_partes)
# Graficar los promedios de las partes en un gráfico de barras
partes_labels = ['Parte 1', 'Parte 2', 'Parte 3', 'Parte 4']
plt.bar(partes_labels, promedios_partes)
plt.title('Promedios de las partes del frame (normalizado)')
plt.xlabel('Partes')
plt.ylabel('Promedio')
plt.show()