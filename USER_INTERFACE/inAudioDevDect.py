import pyaudio
import wave
import time as tm
import sys
import threading
import numpy as np
def list_device_input():
    p = pyaudio.PyAudio()
    default_host_api = p.get_default_host_api_info()

    print(f"Dispositivos de entrada de audio disponibles ():")

    audio_input_devices = []

    for i in range(default_host_api['deviceCount']):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            audio_input_devices.append((i, device_info["name"]))
    return audio_input_devices

class AudioManagerFile():
    def __init__(self,audio_file="",callback_data=None,callback_finish=None):
        self.audio_file = audio_file
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.wf = None
        self.paused = False
        self.play_thread = None
        self.start_position=0
        self.paused = False
        self.is_finish = False
        self.force_breake = False
        self.callback_data=callback_data
        self.callback_finish=callback_finish
        self.rate=0
    def play_audio(self):
        while True:
            if not self.paused or not self.force_breake:
                data = self.wf.readframes(1024)
                if not data :
                    self.callback_finish()
                    self.is_finish=True 
                    break  # Fin de la reproducción
                self.callback_data(data)
                self.stream.write(data)
    def play(self,audio_file="", start_time=0):
        if self.audio_file =="":
            self.audio_file=audio_file
        self.wf = wave.open(self.audio_file, 'rb')
        self.is_finish=False 
        # Obtiene la duración del archivo en segundos
        audio_duration = self.wf.getnframes() / self.audio.get_default_input_device_info()['defaultSampleRate']

        # Solicita al usuario la duración de la reproducción
        print(f"Duración del archivo: {audio_duration} segundos")

        # Calcula la posición de inicio en bytes
        self.start_position = int(start_time * self.audio.get_default_input_device_info()['defaultSampleRate'])
        self.rate=self.wf.getframerate()
        # Configura el flujo de salida para la reproducción de audio
        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wf.getsampwidth()),
                                     channels=self.wf.getnchannels(),
                                     rate=self.wf.getframerate(),
                                     output=True)
        print(self.wf.getframerate())
        self.wf.setpos(self.start_position)

        self.play_thread = threading.Thread(target=self.play_audio)
        self.play_thread.start()
    def isFinish(self):
        return self.is_finish
    def toggle_pause(self):
            self.paused = not self.paused
    def event_Jump(self,time):
            self.force_breake=True
            self.wf.setpos(int(time * self.audio.get_default_input_device_info()['defaultSampleRate']))
            self.force_breake=False
    def get_rate(self):
        return self.rate


#if __name__ == "__main__":
#    list=list_device_input()
#    for elemento in list:
#            print(elemento[1])
#    p=AudioManagerFile("Sound1.wav",printCallback)
#    p.play()
#    while True:
#        if p.isFinish():
#            print("Termino")
#            break
#        inputs =input("PARA")
#        times= int(inputs)
#        p.event_Jump(times)#
