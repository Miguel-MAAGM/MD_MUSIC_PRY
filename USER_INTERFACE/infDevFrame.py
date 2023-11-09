# Draggable rectangle with blitting.
import numpy as np
import customtkinter as ctk



class listDevFrame(ctk.CTkFrame):
    def __init__(self, master,clb_GET=None,clb_SET=None,clb_RFH=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.label_Title=ctk.CTkLabel(self,text="Lista de torres", fg_color="gray30",corner_radius=10)
        self.label_Title.grid(row=0, column=0,padx=10,pady=10,columnspan=2,sticky="nsew")

        self.cmb_boxListDev =ctk.CTkComboBox(self)
        self.cmb_boxListDev.set("No device")
        self.Btn_Refresh    =ctk.CTkButton(self,text="Refresh",command=clb_RFH)
        self.Btn_GET        =ctk.CTkButton(self,text="Get data",command=clb_GET)
        self.Btn_SET        =ctk.CTkButton(self,text="Set data",command=clb_SET)

        self.cmb_boxListDev.grid(row=1, column=0,padx=20,pady=20)
        self.Btn_Refresh.grid(row=2, column=0,padx=10,pady=10)
        self.Btn_GET.grid(row=3, column=0,padx=10,pady=10)
        self.Btn_SET.grid(row=4, column=0,padx=10,pady=10)
    def refreshListDev(self,list):

        self.cmb_boxListDev.configure(values=list)
class entryFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.label_Speed  =ctk.CTkLabel(self,text              ="Speed MAX (mm/s):")
        self.label_AccPSec=ctk.CTkLabel(self,text="Acceleration per second (mm/s ):")
        self.label_DecPsec=ctk.CTkLabel(self,text="Deceleration per second (mm/s ):")
        self.label_StpPMel=ctk.CTkLabel(self,text    ="Step per millimeter (Count):")
        self.label_StpPRev=ctk.CTkLabel(self,text    ="Step per revolution (Count):")
        self.label_HomeDir=ctk.CTkLabel(self,text    ="Home Dir (1/-1):")
        validation=self.only_numbers
#
        self.entry_Speed  =ctk.CTkEntry(self, validate='key',validatecommand=(validation, '%S'))
        self.entry_AccPSec =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_DecPsec =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_StpPMel =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_StpPRev =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))
        self.entry_HomeDir =ctk.CTkEntry(self,validate='key',validatecommand=(validation, '%S'))

        
        self.label_Speed.grid(  row=0, column=0,padx=20,sticky="we")
        self.label_AccPSec.grid(row=1, column=0,padx=20,sticky="we")
        self.label_DecPsec.grid(row=2, column=0,padx=20,sticky="we")
        self.label_StpPMel.grid(row=3, column=0,padx=20,sticky="we")
        self.label_StpPRev.grid(row=4, column=0,padx=20,sticky="we")
        self.label_HomeDir.grid(row=5, column=0,padx=20,sticky="we")
#
        self.entry_Speed  .grid(row=0, column=1,padx=20,sticky="we")
        self.entry_AccPSec.grid(row=1, column=1,padx=20,sticky="we")
        self.entry_DecPsec.grid(row=2, column=1,padx=20,sticky="we")
        self.entry_StpPMel.grid(row=3, column=1,padx=20,sticky="we")
        self.entry_StpPRev.grid(row=4, column=1,padx=20,sticky="we")
        self.entry_HomeDir.grid(row=5, column=1,padx=20,sticky="we")
    def only_numbers(char):
        return char.isdigit()or char=="."
        #setSpeedInStepsPerSecond
        #setAccelerationInStepsPerSecondPerSecond
        #setDecelerationInStepsPerSecondPerSecond
        #setStepsPerMillimeter
        #
        #
        #
        #        
    def getValues(self):

        my_struct={
                'Speed'  : self.entry_Speed  .get(),
                'AccPSec': self.entry_AccPSec.get(),
                'DecPsec': self.entry_DecPsec.get(),
                'StpPMel': self.entry_StpPMel.get(),
                'StpPRev': self.entry_StpPRev.get(),
                'HomeDir': self.entry_HomeDir.get()
            }
        return my_struct
    
    def setValues(self,struct):
        self.entry_Speed  .delete(0,100)
        self.entry_Speed  .insert(1,str(struct['Speed']))
 
        self.entry_AccPSec.delete(0,100)
        self.entry_AccPSec.insert(1,str(struct['AccPSec']))
 
        self.entry_DecPsec.delete(0,100)
        self.entry_DecPsec.insert(1,str(struct['DecPsec']))
 
        self.entry_StpPMel.delete(0,100)
        self.entry_StpPMel.insert(1,str(struct['StpPMel']))
 
        self.entry_StpPRev.delete(0,100)
        self.entry_StpPRev.insert(1,str(struct['StpPRev']))
        
        self.entry_HomeDir.delete(0,100)
        self.entry_HomeDir.insert(1,str(struct['HomeDir']))

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
        self.Entry_TW1= entryFrame(self.tabview.tab("Torre 1"))
        self.Entry_TW1.pack(padx=10,pady=10,fill="both",expand=True)
        self.Entry_TW2= entryFrame(self.tabview.tab("Torre 2"))
        self.Entry_TW2.pack(padx=10,pady=10,fill="both",expand=True)
        self.Entry_VIE= entryFrame(self.tabview.tab("Viela"))
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
        
        # add widgets onto the frame...

        self.text_InfoDevText=ctk.CTkTextbox(self) 
        self.entry_infoDevText=ctk.CTkEntry(self,placeholder_text="Command to tower")
        self.BTNentry_infoDev=ctk.CTkButton(self,text="Send",command=self.newEvent) 
        self.cofingDevFrame = cofingDevFrame(self)
        self.listDevFrame =listDevFrame(self,clb_SET=self.M_clb_SET,clb_GET=self.M_clb_GET,clb_RFH=self.M_clb_RFH)
        self.count=0
        self.listDevFrame.grid(row=0, column=2,padx=20,pady=20,sticky="nsew")
        self.cofingDevFrame.grid(row=0, column=0,padx=20,pady=20,columnspan=2,sticky="nsew")
        self.text_InfoDevText.grid(row=1, padx=20, columnspan=3,sticky="nsew")
        self.entry_infoDevText.grid(row=2,column=0,padx=20,columnspan=2,sticky="ew")
        self.BTNentry_infoDev.grid(row=2,column=2,padx=20,sticky="ew")

        self.text_InfoDevText.insert("0.0","-> |"+"Console Log with server..."+"\n")
        self.text_InfoDevText.configure(state="disabled")  
    def newEvent(self):
        self.text_InfoDevText.configure(state="normal")
        self.text_InfoDevText.insert("0.0",f"<- {self.count} |"+"Console Log with server... event "+"\n")
        self.count=self.count+1
        self.text_InfoDevText.configure(state="disabled")
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
            'DecPsec': 800,
            'StpPMel': 500,
            'StpPRev': 400,
            'HomeDir': -1
        }
        M_VIELA = {
            'Speed'  : 1600,
            'AccPSec': 800,
            'DecPsec': 800,
            'StpPMel': 500,
            'StpPRev': 400,
            'HomeDir': -1
        }

        torres = {
            'MTW_1'  : MTW_1,
            'MTW_2'  : MTW_1,
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
#class App(ctk.CTk):
#    def __init__(self):
#        super().__init__()
##        self.geometry("1080x720")
##        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)  # configure grid system
##        self.grid_columnconfigure(0, weight=1)
##
#        self.UP_bar= ctk.CTkFrame(master=self,#fg_color=("#3a7ebf"),width= 200, height= 50,corner_radius=0)
#        self.UP_bar.grid(row=0, column=0, padx#=0,pady=0,sticky="NEW")
#        self.my_frame = infDevFrame(master=self)
###        self.my_frame.grid(row=1,rowspan=5, column=0, padx=20,pady=20 ,sticky="NSEW")
###if __name__ == "__main__":
###    app = App()
###    app.mainloop()
###
####
#
