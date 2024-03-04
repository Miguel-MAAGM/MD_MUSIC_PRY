#listDevFrame.py
import customtkinter as ctk

class listDevFrame(ctk.CTkFrame):
    def __init__(self, master,clb_GET=None,clb_SET=None,clb_RFH=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.label_Title=ctk.CTkLabel(self,text="Lista de torres", fg_color="gray30",corner_radius=10)
        self.label_Title.grid(row=0, column=0,padx=10,pady=10,columnspan=2,sticky="nsew")

        self.cmb_boxListDev =ctk.CTkComboBox(self,values=["No device"])
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