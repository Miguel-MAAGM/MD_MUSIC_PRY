import pyaudio
import wave
import time as tm
import threading
import numpy as np
import sounddevice as sd
import time
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
        self.size=0
        self.chunk=2304
        self.total_frames_read = 0  # Inicializar el contador de frames leídos
        
    def play_audio(self,in_data, frame_count, time_info, status):
        
        raw_data = self.wf.readframes(frame_count)
        data = np.frombuffer(raw_data, dtype=np.int16)
        if self.wf.getnchannels()==2:
            data_combined = data[::self.wf.getnchannels()] + data[1::self.wf.getnchannels()]
            self.callback_data(data_combined)        
        else:
            self.callback_data(data)        

        if self.chunk>len(raw_data) :
            self.is_finish=True
            self.callback_finish()

        return(data, pyaudio.paContinue)

    def start_audio_file(self,audio_file="", start_time=0):
        if self.audio_file =="":
            self.audio_file=audio_file
        self.wf = wave.open(self.audio_file, 'rb')
        print("WABE")
        self.is_finish=False 
        # Obtiene la duración del archivo en segundos
        audio_duration = self.wf.getnframes() / self.audio.get_default_input_device_info()['defaultSampleRate']
        print(self.wf.getnframes())
        # Solicita al usuario la duración de la reproducción
        print(f"Duración del archivo: {audio_duration} segundos")

        # Calcula la posición de inicio en bytes
        self.start_position = int(start_time * self.audio.get_default_input_device_info()['defaultSampleRate'])
        self.rate=self.wf.getframerate()

        # Configura el flujo de salida para la reproducción de audio
        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wf.getsampwidth()),
                                     channels=self.wf.getnchannels(),
                                     rate=self.wf.getframerate(),
                                     output=True,
                                     stream_callback=self.play_audio,
                                     start =False)

        self.wf.setpos(self.start_position)
        self.stream.start_stream()
       # self.play_thread = threading.Thread(target=self.play_audio)
        #self.play_thread.start()
    def isFinish(self):
        return self.is_finish
    def toggle_pause(self):
        if self.stream.is_active():
            self.stream.stop_stream()
        else :
            self.stream.start_stream()

    def event_Jump(self,time):
            self.force_breake=True
            self.wf.setpos(int(time * self.audio.get_default_input_device_info()['defaultSampleRate']))
            self.force_breake=False
    def get_rate(self):
        return self.rate
class AudioManagerMic():
    def __init__(self,callback_data=None):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.frames = []
        self.stream=None 
        self.clb=callback_data
        self.p = pyaudio.PyAudio()

    def set_input_device(self, device_index):
        self.device_index = device_index

    def callback(self, in_data, frame_count, time_info, status):
        data = np.frombuffer(in_data, dtype=np.int16)
        self.clb(data,self.RATE)
        return (in_data, pyaudio.paContinue)

    def start_recording(self,INDEX):
        self.device_index = INDEX
        self.stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK,
                             input_device_index=self.device_index,
                             stream_callback=self.callback)
        self.stream.start_stream()
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()


