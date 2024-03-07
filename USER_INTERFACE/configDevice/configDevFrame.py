from . import entryFrame as infDev
import customtkinter as ctk


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