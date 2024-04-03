import customtkinter as ctk

class entryFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.label_Speed  =ctk.CTkLabel(self,text              ="Speed MAX (mm/s):")
        self.label_AccPSec=ctk.CTkLabel(self,text="Acceleration per second (mm/s ):")
        self.label_DecPsec=ctk.CTkLabel(self,text="Deceleration per second (mm/s ):")
        self.label_StpPMel=ctk.CTkLabel(self,text    ="Step per millimeter (Count):")
        self.label_StpPRev=ctk.CTkLabel(self,text    ="Step per revolution (Count):")
        self.label_HomeDir=ctk.CTkLabel(self,text    ="Home Dir (1/-1):")
        self.label_BaseDir=ctk.CTkLabel(self,text    ="Base Dir (1/-1):")
        
        validation=self.only_numbers
#
        self.entry_Speed  =ctk.CTkEntry(self)
        self.entry_AccPSec =ctk.CTkEntry(self)
        self.entry_DecPsec =ctk.CTkEntry(self)
        self.entry_StpPMel =ctk.CTkEntry(self)
        self.entry_StpPRev =ctk.CTkEntry(self)
        self.entry_HomeDir =ctk.CTkEntry(self)
        self.entry_BaseDir =ctk.CTkEntry(self)
        
        self.label_Speed.grid(  row=0, column=0,padx=20,sticky="we")
        self.label_AccPSec.grid(row=1, column=0,padx=20,sticky="we")
        self.label_DecPsec.grid(row=2, column=0,padx=20,sticky="we")
        self.label_StpPMel.grid(row=3, column=0,padx=20,sticky="we")
        self.label_StpPRev.grid(row=4, column=0,padx=20,sticky="we")
        self.label_HomeDir.grid(row=5, column=0,padx=20,sticky="we")
        self.label_BaseDir.grid(row=6, column=0,padx=20,sticky="we")
#
#
        self.entry_Speed  .grid(row=0, column=1,padx=20,sticky="we")
        self.entry_AccPSec.grid(row=1, column=1,padx=20,sticky="we")
        self.entry_DecPsec.grid(row=2, column=1,padx=20,sticky="we")
        self.entry_StpPMel.grid(row=3, column=1,padx=20,sticky="we")
        self.entry_StpPRev.grid(row=4, column=1,padx=20,sticky="we")
        self.entry_HomeDir.grid(row=5, column=1,padx=20,sticky="we")
        self.entry_BaseDir.grid(row=6, column=1,padx=20,sticky="we")

    def clear(self):
        self.entry_Speed  .delete(0,100)
        self.entry_AccPSec.delete(0,100)
        self.entry_DecPsec.delete(0,100)
        self.entry_StpPMel.delete(0,100)
        self.entry_StpPRev.delete(0,100)
        self.entry_HomeDir.delete(0,100)
        self.entry_BaseDir.delete(0,100)
    def only_numbers(char):
        print("New")
        return char.isdigit()or char=="."   

    def getValues(self):

        my_struct={
                'SPS_': self.entry_Speed  .get(),
                'ASPS': self.entry_AccPSec.get(),
                'DSPS': self.entry_DecPsec.get(),
                'SPM_': self.entry_StpPMel.get(),
                'SPR_': self.entry_StpPRev.get(),
                'Hdir': self.entry_HomeDir.get(),
                'bdir': self.entry_BaseDir.get()
            }
        return my_struct
    
    def setValues(self,struct):
        self.clear()
        self.entry_Speed  .insert(0,str(struct['SPS_']))

        self.entry_AccPSec.insert(0,str(struct['ASPS']))
 
        self.entry_DecPsec.insert(0,str(struct['DSPS']))
 
        self.entry_StpPMel.insert(0,str(struct['SPM_']))
 
        self.entry_StpPRev.insert(0,str(struct['SPR_']))
        
        self.entry_HomeDir.insert(0,str(struct['Hdir']))

        self.entry_BaseDir.insert(0,str(struct['bdir']))