import sys
import numpy as np
import customtkinter as ctk
import struct
from configDevice import infDevFrame as infDev

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
#        toServer= ServerAdmin.ClientSocket("localHost",122345,receive_callback=self.callBack_Server)

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
        #self.AudioManagerFile=Audio.AudioManagerFile(callback_data=self.Clb_Audio,callback_finish=self.finish_Song)
        #self.AudioFrame= AdI.PlayFrame(self,clb_PLAY=self.PLAY)
        #self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 

        self.ConfigFrame= infDev.infDevFrame(self,
                                             clb_master_SET=self.setConfig,
                                             clb_master_GET=self.getConfig,
                                             clb_master_Refresh=self.refreshListDev,
                                             clb_master_SendPipeline=self.sendMessegePipe)
        self.ConfigFrame.grid(row=1,column=0,sticky ="NSWE") 
       # self.ConfigFrame.list_dev(["VALOR1","VALOR2","VALOR3",])
        #self.count=0
        #self.frame=[]
        #self.canvas=ctk.CTkCanvas(self)
    def refreshListDev(self):
        self.ConfigFrame.setListDev(["DEV1","DEV2","DEV3","DEV4"])
        return True
    def setConfig(self,messege): #manda json 
        print(messege)
        return True
    def getConfig(self,messege):# recibe json
        print(messege)
        
        return True
    def sendMessegePipe(self, messege):#texto plano
        
        print(messege)
        return True



    def segmented_button_callback(self,value):
        print("segmented button clicked:", value)   
        if value== "PLAY":
           # self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 
       #     self.ConfigFrame.grid_forget()

            print("PLAY")

        elif value =="CONFIG":
           # self.AudioFrame.grid_forget()
       #     self.ConfigFrame.grid(row=1,column=0,sticky ="NSWE") 

            print("OTHER")
    

 