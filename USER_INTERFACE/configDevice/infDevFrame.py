# Draggable rectangle with blitting.
import numpy as np
from . import listDevFrame as LsDev
from . import configDevFrame as cfd
from . import logFrame as lf
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

        self.LogFrame= lf.logFrame(self,Clb_SendEvent=self.sendingEvent) #action send
                                                                         #Recive
        self.cofingDevFrame = cfd.cofingDevFrame(self) # set and get function
        self.listDevFrame =LsDev.listDevFrame(self,
                                              clb_SET=self.M_clb_SET, #action from set button
                                              clb_GET=self.M_clb_GET, #action from GET button
                                              clb_RFH=self.M_clb_RFH) #action from RFH button

        self.listDevFrame.grid(row=0, column=2,padx=10,pady=10,sticky="nsew")
        self.cofingDevFrame.grid(row=0, column=0,padx=10,pady=10,columnspan=2,sticky="nsew")
        self.LogFrame.grid(row=1,column=0,padx=10,pady=10,rowspan=2,columnspan=3,sticky="nsew")

    
    def M_clb_GET(self):

        self.callBack_Get(self.listDevFrame.getSelectDevice())
        print("GET_INFO")
    def M_clb_SET(self):
        self.callBack_Set(self.cofingDevFrame.getValues())
        print("SET_INFO")

    def M_clb_RFH(self):
        self.callBack_Refresh()
        print("SET_REFRESH")
    
    def setListDev(self,messege):
        self.listDevFrame.refreshListDev(messege)

    def sendingEvent(self,messege):
        self.callBack_SendPipeline(messege )
        return True

    


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


