# Draggable rectangle with blitting.
import numpy as np
import entryFrame as infDev
import listDevFrame as LsDev
import customtkinter as ctk



#Seleccion de torre y obtencion de datos

#sub clase que contiene las entradas para configurara cada onda

class cofingDevFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.tabview=ctk.CTkTabview(self,fg_color="gray20")
        self.tabview.grid(row=0,column=0,padx=10,pady=10,sticky="nswe")
        self.tabview.add("Torre 1")
        self.tabview.add("Torre 2")
        self.tabview.add("Viela")
        self.Entry_TW1= infDev.entryFrame(self.tabview.tab("Torre 1"))
        self.Entry_TW1.pack(padx=10,pady=10,fill="both",expand=True)
        self.Entry_TW2= infDev.entryFrame(self.tabview.tab("Torre 2"))
        self.Entry_TW2.pack(padx=10,pady=10,fill="both",expand=True)
        self.Entry_VIE= infDev.entryFrame(self.tabview.tab("Viela"))
        self.Entry_VIE.pack(padx=10,pady=10,fill="both",expand=True)
    def setValues(self,struct):
        
        self.Entry_TW1.setValues(struct['MTW_1'])
        self.Entry_TW2.setValues(struct['MTW_2'])
        self.Entry_VIE.setValues(struct['M_VIELA'])
    def getValues(self):

        my_Struct={   
            'MTW_1'  :self.Entry_TW1.getValues(),
            'MTW_2'  :self.Entry_TW2.getValues(),
            'M_VIELA':self.Entry_VIE.getValues()
            }
        return my_Struct

class infDevFrame(ctk.CTkFrame):
    def __init__(self, master,clb_master_GET=None,clb_master_SET=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)  # configure grid system
        self.callBack_Set=clb_master_SET
        # add widgets onto the frame...

        self.text_InfoDevText=ctk.CTkTextbox(self) 
        self.entry_infoDevText=ctk.CTkEntry(self,placeholder_text="Command to tower")
        self.BTNentry_infoDev=ctk.CTkButton(self,text="Send",command=self.sendingEvent) 
        self.cofingDevFrame = cofingDevFrame(self)
        self.listDevFrame =LsDev.listDevFrame(self,clb_SET=self.M_clb_SET,clb_GET=self.M_clb_GET,clb_RFH=self.M_clb_RFH)
        self.count=0
        self.listDevFrame.grid(row=0, column=2,padx=20,pady=20,sticky="nsew")
        self.cofingDevFrame.grid(row=0, column=0,padx=20,pady=20,columnspan=2,sticky="nsew")
        self.text_InfoDevText.grid(row=1, padx=20, columnspan=3,sticky="nsew")
        self.entry_infoDevText.grid(row=2,column=0,padx=20,columnspan=2,sticky="ew")
        self.BTNentry_infoDev.grid(row=2,column=2,padx=20,sticky="ew")

        self.text_InfoDevText.insert("0.0","-> |"+"Console Log with server..."+"\n")
        self.text_InfoDevText.configure(state="disabled")  
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
        MTW_1 = {
            'Speed'  : 1600,
            'AccPSec': 800,
            'DecPsec': 800,
            'StpPMel': 500,
            'StpPRev': 400,
            'HomeDir': -1
        }

        MTW_2 = {
            'Speed'  : 1600,
            'AccPSec': 800,
            'DecPsec': 4,
            'StpPMel': 6,
            'StpPRev': 400,
            'HomeDir': -1
        }
        M_VIELA = {
            'Speed'  : 1600,
            'AccPSec': 800,
            'DecPsec': 800,
            'StpPMel': 500,
            'StpPRev': 84,
            'HomeDir': -1
        }

        torres = {
            'MTW_1'  : MTW_1,
            'MTW_2'  : MTW_2,
            'M_VIELA': M_VIELA
        }
        self.cofingDevFrame.setValues(torres)
        print("GET_INFO")
    def M_clb_SET(Self):
        print("SET_INFO")
    def M_clb_RFH(Self):
        print("SET_REFRESH")
    def list_dev(self,list):
        self.listDevFrame.refreshListDev(list)






#
#class App(ctk.CTk):
#    def __init__(self):
#       super().__init__()
#       self.geometry("1080x720")
#       self.grid_rowconfigure((0,1,2,3,4,5), weight=1)  # configure grid system
#       self.grid_columnconfigure(0, weight=1)
#
#       self.UP_bar= ctk.CTkFrame(master=self,fg_color=("#3a7ebf"),width= 200, height= 50,corner_radius=0)
#       self.UP_bar.grid(row=0, column=0, padx=0,pady=0,sticky="NEW")
#       self.my_frame = infDevFrame(master=self)
#       self.my_frame.grid(row=1,rowspan=5, column=0, padx=20,pady=20 ,sticky="NSEW")
#
#if __name__ == "__main__":
#    app = App()
#    app.mainloop()#
