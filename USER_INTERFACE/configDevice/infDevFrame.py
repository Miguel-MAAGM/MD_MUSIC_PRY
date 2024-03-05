# Draggable rectangle with blitting.
import numpy as np
from . import listDevFrame as LsDev
from . import configDevFrame as cfd
import customtkinter as ctk


#Seleccion de torre y obtencion de datos

#sub clase que contiene las entradas para configurara cada onda



class infDevFrame(ctk.CTkFrame):
    def __init__(self, master,
                 clb_master_SET=None,
                 clb_master_GET=None,
                 clb_master_Refresh=None,
                 clb_master_SendPipeline=None,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        self.callBack_Set=clb_master_SET #Sending JSON CONFIG
        self.callBack_Get=clb_master_GET #Get JSON CONFIG  
        self.callBack_Refresh=clb_master_Refresh #GET List Device
        self.callBack_SendPipeline=clb_master_SendPipeline #Send mesage plain to Device Select

        
        # add widgets onto the frame...

        self.text_InfoDevText=ctk.CTkTextbox(self) 
        self.entry_infoDevText=ctk.CTkEntry(self,placeholder_text="Command to tower")
        self.BTNentry_infoDev=ctk.CTkButton(self,text="Send",command=self.sendingEvent) 
        self.cofingDevFrame = cfd.cofingDevFrame(self)
        self.listDevFrame =LsDev.listDevFrame(self,
                                              clb_SET=self.M_clb_SET, #action from set button
                                              clb_GET=self.M_clb_GET, #action from GET button
                                              clb_RFH=self.M_clb_RFH) #action from RFH button
        ##self.count=0
        self.listDevFrame.grid(row=0, column=2,padx=20,pady=20,sticky="nsew")
        self.cofingDevFrame.grid(row=0, column=0,padx=20,pady=20,columnspan=2,sticky="nsew")
        self.text_InfoDevText.grid(row=1, padx=20, columnspan=3,sticky="nsew")
        self.entry_infoDevText.grid(row=2,column=0,padx=20,columnspan=2,sticky="ew")
        self.BTNentry_infoDev.grid(row=2,column=2,padx=20,sticky="ew")

        #self.text_InfoDevText.insert("0.0","-> |"+"Console Log with server..."+"\n")
        #self.text_InfoDevText.configure(state="disabled")  

    def sendingEvent(self):
        self.text_InfoDevText.configure(state="normal")
        self.text_InfoDevText.insert("0.0",f"<- {self.count} |"+"Console Log with server... event ->"+self.entry_infoDevText.get()+"\n")
        self.count=self.count+1
        self.text_InfoDevText.configure(state="disabled")
        self.callBack_Set(self.entry_infoDevText.get())
        self.entry_infoDevText.delete(0,100)
        self.getingEvent()




    def getingEvent(self):
        print("New Data")
    def M_clb_GET(self):
#        MTW_1 = {
#            'Speed'  : 1600,
#            'AccPSec': 800,
#            'DecPsec': 800,
#            'StpPMel': 500,
#            'StpPRev': 400,
#            'HomeDir': -1
#        }
#
#        MTW_2 = {
#            'Speed'  : 1600,
#            'AccPSec': 800,
#            'DecPsec': 4,
#            'StpPMel': 6,
#            'StpPRev': 400,
#            'HomeDir': -1
#        }
#        M_VIELA = {
#            'Speed'  : 1600,
#            'AccPSec': 800,
#            'DecPsec': 800,
#            'StpPMel': 500,
#            'StpPRev': 84,
#            'HomeDir': -1
#        }
#
#        torres = {
#            'MTW_1'  : MTW_1,
#            'MTW_2'  : MTW_2,
#            'M_VIELA': M_VIELA
#        }
#        self.cofingDevFrame.setValues(torres)
        print("GET_INFO")
    def M_clb_SET(Self):
        print("SET_INFO")
    def M_clb_RFH(Self):
        print("SET_REFRESH")
    def list_dev(self,list):
        self.listDevFrame.refreshListDev(list)







