
import customtkinter as ctk

class logFrame(ctk.CTkFrame):
    def __init__(self, master,Clb_SendEvent=None ,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        self.text_InfoDevText=ctk.CTkTextbox(self) 
        self.entry_infoDevText=ctk.CTkEntry(self,placeholder_text="Command to tower")
        self.BTNentry_infoDev=ctk.CTkButton(self,text="Send",command=self.actionEntryBt) 
        self.clb_Send=Clb_SendEvent
        self.text_InfoDevText.insert("0.0","-> |"+"Console Log with server..."+"\n")
        self.text_InfoDevText.configure(state="disabled")  
        self.count=0
        self.text_InfoDevText.grid(row=0,column=0, padx=20, pady=20, rowspan=2, columnspan=3,sticky="nsew")
        self.entry_infoDevText.grid(row=2,column=0,padx=20, pady=5,columnspan=2,sticky="ew")
        self.BTNentry_infoDev.grid(row=2, column=2,padx=20, pady=5, sticky="ew")

    def recibeEvent(self, messege):
        self.text_InfoDevText.configure(state="normal")
        self.text_InfoDevText.insert("0.0",f"<- {self.count} |"+"Server response->"+messege+"\n")
        self.count=self.count+1
        self.text_InfoDevText.configure(state="disabled")

    def actionEntryBt(self):
        self.text_InfoDevText.configure(state="normal")
        self.text_InfoDevText.insert("0.0",f"<- {self.count} |"+"Client send ->"+self.entry_infoDevText.get()+"\n")
        self.count=self.count+1
        self.text_InfoDevText.configure(state="disabled")
        self.clb_Send(self.entry_infoDevText.get())
        self.entry_infoDevText.delete(0,100)
        
