from turtle import width
import pyaudio
import numpy as np
import wave
import librosa
import customtkinter as ctk

# Variables para la grabacion del audio
RATE = 44100
RECORD_SECONDS = 10
CHANNELS = 2
p = pyaudio.PyAudio()

# Funcion para escoger dispositivo de entrada de audio
def set_input_device(device_index):
    global input_device_index
    input_device_index = device_index

# Funcion para grabar audio
def grabar_audio():
    global input_device_index
    global audio_data
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=1024,
                    input_device_index = input_device_index)
    print("Recording")
    frames = []
    for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(np.fromstring(data, dtype=np.int16))
    grabacion_finalizada.configure(text=f"Grabación Finalizada !! ")
    stream.stop_stream()
    stream.close()
    p.terminate()
    # Guarda la grabación como un archivo .wav
    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    # Concatenate all frames into one numpy array
    audio_data = np.concatenate(frames)
    audio_data = audio_data.astype(float)

# Funcion para calcular los BPM
def calcular_bpm():
    # Estima el tempo del audio original
    tempo, beats = librosa.beat.beat_track(y=audio_data, sr=RATE)
    tempo_label.configure(text=f"Tempo original: {tempo} BPM")
    # Aumenta el tempo al doble
    audio_data_fast = librosa.effects.time_stretch(audio_data, rate=2)
    # Estima el tempo del audio acelerado
    tempo_fast, _ = librosa.beat.beat_track(y=audio_data_fast, sr=RATE)
    tempo_fast_label.configure(text=f"Tempo original: {tempo_fast} BPM")

# Obtener la lista de dispositivos de entrada de audio
device_info = p.get_host_api_info_by_index(0)  # Usar el primer host API
device_count = device_info.get("deviceCount")
input_device_names = [p.get_device_info_by_host_api_device_index(0, i).get("name") for i in range(device_count)]

#................. Interfaz Grafica.....................
# Apariencia
ctk.set_appearance_mode("System") # Puede ser Dark o Ligth tambien
ctk.set_default_color_theme("blue") # Puede ser dark-blueo o green tambien
#Window
window=ctk.CTk()
window.title('Orquesta Pacifica')
window.geometry('600x400')

#Paso 1: Entrada de Audio 
selected_input_device = ctk.StringVar()
description_label = ctk.CTkLabel(window, text="Aquí debe seleccionar la opción de entrada de audio:",font=('Arial',18))
description_label.grid(row=0, column=0,)
for i, device_name in enumerate(input_device_names): #Radio Boton para seleccion entrada de audio
    ctk.CTkRadioButton(window, text=device_name, variable=selected_input_device, value=i, command=lambda i=i: set_input_device(i),font=('Arial',14)).grid(row=i+1, column=0, sticky="w")

#Paso 2: Grabar Canción
leer_bpm_label = ctk.CTkLabel(window, text="Aquí debe grabar la canción:",font=('Arial',18))
leer_bpm_label.grid(row=10, column=0,)
leer_bpm_button=ctk.CTkButton(window,text='Grabar Canción',command=grabar_audio)#Boton para leer BPM
leer_bpm_button.grid(row=14, column=0, sticky="w")#Boton para leer BPM
grabacion_finalizada = ctk.CTkLabel(window,text="",font=('Arial',14)) # Para mostrar tempo
grabacion_finalizada.grid(row=16, column=0, sticky="w")

# Paso 3: Calcular BPM
calcular_tempo_label = ctk.CTkLabel(window, text="Aquí debe calcular los BPM de la cancion:",font=('Arial',18))
calcular_tempo_label.grid(row=17, column=0,)
tempo_label = ctk.CTkLabel(window,text="",font=('Arial',14)) # Para mostrar tempo
tempo_label.grid(row=20, column=0,sticky="w")
tempo_fast_label = ctk.CTkLabel(window, text="",font=('Arial',14)) # Para mostrar tempo fast
tempo_fast_label.grid(row=22, column=0,sticky="w")
calcular_button = ctk.CTkButton(window, text="Calcular BPM", command=calcular_bpm)# Boton del tempo leido
calcular_button.grid(row=18, column=0, sticky="w")

#Run
window.mainloop()
