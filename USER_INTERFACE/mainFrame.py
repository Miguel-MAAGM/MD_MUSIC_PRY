import sys
import numpy as np
import customtkinter as ctk
import struct
import socket
from configDevice import infDevFrame as infDev
from clientServer import manageClientServer as MCS
from audioFrame import AudioinFrame as AiF
import json

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



        self.protocol("WM_DELETE_WINDOW",self.CloseALL)

        self.AudioFrame= AiF.PlayFrame(self,clb_DATAOUT=self.clb_DataOut)
        self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 

        self.ConfigFrame= infDev.infDevFrame(self,
                                             clb_master_SET=self.setConfig,
                                             clb_master_GET=self.getConfig,
                                             clb_master_Refresh=self.refreshListDev,
                                             clb_master_SendPipeline=self.sendMessegePipe)
        self.ConfigFrame.grid(row=1,column=0,sticky ="NSWE") 

        self.talkToServer= MCS.manageClientServer(socket.gethostbyname(socket.gethostname()),port=12345,
                                                  clb_GetInf=None,
                                                  clb_List=self.clb_list,
                                                  clb_pipeline=None)
        self.talkToServer.connect()
    def clb_DataOut(self, data):
        print(data)
        pos=data[0]
        vel=data[1]
        dataA = {
                "ID":"TW1",
                "CMD": "MOV",
                "M1": pos[0],
                "M2": pos[0],
                "MV": vel
            }
        dataB = {
                "ID":"TW2",
                "CMD": "MOV",
                "M1": pos[1],
                "M2": pos[1],
                "MV": vel
            }
        dataC = {
                "ID":"TW3",
                "CMD": "MOV",
                "M1": pos[2],
                "M2": pos[2],
                "MV": vel
            }
        dataD = {
                "ID":"TW4",
                "CMD": "MOV",
                "M1": pos[3],
                "M2": pos[3],
                "MV": vel
            }
        data_master={
            "CMD":"MOV",
            "TW1":dataA,
            "TW2":dataB,
            "TW3":dataC,
            "TW4":dataD
        }
        json_data = json.dumps(data_master)
        print(json_data)
        self.talkToServer.send(json_data)
    def clb_list(self,data):
        self.ConfigFrame.setListDev(data)
        print(data)

    def refreshListDev(self):
        #self.ConfigFrame.setListDev(["DEV1","DEV2","DEV3","DEV4"])
        self.talkToServer.getListDev()
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

    def CloseALL(self):
        print("Cerrando")
        self.destroy()
        self.talkToServer.disconnect()


    def segmented_button_callback(self,value):
        print("segmented button clicked:", value)   
        if value== "PLAY":
            self.AudioFrame.grid(row=1,column=0,sticky ="NSWE") 
            self.ConfigFrame.grid_forget()
            print("PLAY")

        elif value =="CONFIG":
            self.AudioFrame.grid_forget()
            self.ConfigFrame.grid(row=1,column=0,sticky ="NSWE") 

            print("OTHER")
    

 