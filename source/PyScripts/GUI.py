from guizero import *
from tkinter import ttk #Like the CSS for tkinter
import tkinter as tk
import handshake as hsh

#Convention:
#display_NAME: for initializing the objects
#__NAME: to connect object values to the lib
#__NAME: use camelCase
# lambda function is NOT invoked right then and there
# we can also use .. , args=[] for command

'''
Label	lbl	lbl_name
Button	btn	btn_submit
Entry	ent	ent_age
Text	txt	txt_notes
Frame	frm	frm_address
'''
################################
# Global functions & variables #
################################
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    lbl = ttk.Label(popup, text=msg, font=NORM_FONT)
    lbl.pack(side="top", fill="x", pady=10)
    btn1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    btn1.pack()
class tk_main(tk.Tk):    
    def __init__(self, *args, **kwargs): #Runs on initialisation (load stuff)
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "FT_Master-Slave")
        self.main_frame = tk.Frame(self, background="cyan", relief=tk.RAISED, borderwidth=5)
        self.main_frame.grid(row=0, column=0)

        menubar = tk.Menu(self.main_frame)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command= lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        self.frames = {}        
        frame = StartPage(self.main_frame,self)
        self.frames[StartPage] = frame
        frame.grid(row=3,column=3, sticky="nsew")        
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont] #key
        frame.tkraise()
#########
# Pages #
#########
class StartPage(tk.Frame):
    hidden = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)        
        #widgets
        lbl_main = ttk.Label(self, text="Main Page", font=LARGE_FONT,relief=tk.GROOVE, borderwidth=5)
        ssh_frame = ttk.LabelFrame(self, text="SSH connect")

        ent_pass = ttk.Entry(ssh_frame, show='*')
        lbl_pass = ttk.Label(ssh_frame, text="Password:")
        lbl_ip = ttk.Label(ssh_frame, text="IP Address:")
        self.ent_ip = ttk.Entry(ssh_frame)
        ssh_btn_sett = ttk.Button(ssh_frame, text="More Settings", command=lambda: addit_sett(self.hidden, btn_pkey, lbl_pkey,
                                                                                            ssh_btn_sett, btn_hosts, lbl_hosts))
        ssh_btn_connect = tk.Button(ssh_frame, text="Connect", command=lambda: Ssh.connect(self,"1","1"))
        lbl_pkey = tk.Label(ssh_frame, text="Private Key")
        btn_pkey = ttk.Button(ssh_frame, text="Select", command=lambda:controller.ssh_pkey())
        lbl_hosts = ttk.Label(ssh_frame, text="Known hosts")
        btn_hosts = ttk.Button(ssh_frame, text="Select", command=lambda:controller.ssh_hosts())
        #functionality
        self.ent_ip.focus() #Created the UI "SSH Connect". Functionality will be added this week. Closes #1 Closes #3
        #layout
        ssh_frame.columnconfigure(0, weight=1)
        ssh_frame.columnconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        #position 
        ssh_frame.grid(row=1, column=0)
        lbl_main.grid(row=0, column=0, pady=10, padx=10)  
        lbl_ip.grid(row=0, column=0, padx=10)
        self.ent_ip.grid(row=0, column=1)
        ent_pass.grid(row=1, column=1, pady=10, padx=10)
        lbl_pass.grid(row=1, column=0)
        ssh_btn_connect.grid(row=2, column=1, sticky=tk.E, padx=2, pady=2)
        ssh_btn_sett.grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
    
        def addit_sett(hidden, btn_pkey, lbl_pkey, ssh_btn_sett, btn_hosts, lbl_hosts):
            if hidden:
                ssh_btn_sett['text'] = 'More Settings'
                lbl_pkey.grid_forget()
                btn_pkey.grid_forget()
                btn_hosts.grid_forget()
                lbl_hosts.grid_forget()
                self.hidden = False
            else:
                ssh_btn_sett['text'] = 'Hide Settings'        
                lbl_pkey.grid(row=3, column=0)
                btn_pkey.grid(row=3, column=1, sticky=tk.W)
                lbl_hosts.grid(row=4, column=0)
                btn_hosts.grid(row=4, column=1, sticky=tk.W)
                self.hidden = True
            return self.hidden
    @staticmethod
    def get_ip_entity_string(self):
        return self.ent_ip.get()
class Ssh(StartPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
    
    def connect(self, target_ip, target_pass): #works        
        entity_str = StartPage.get_ip_entity_string(self)
        print(entity_str)
#########
# Pages #
#########

def main():
    app = App(title='File transfer', width=800, height=600)
    
    def display_ping():
        box_ping = Box(app, width=300, height=200, border=1,layout='grid',align='left')
        PushButton(box_ping,command=lambda: __ping(input_box),text="Ping",grid=[0,0])
        input_box = TextBox(box_ping, grid=[10,0])
    def __ping(inputBox):
        hsh.pinhshx(inputBox.value)
    def display_transfer_file():
        #width=800, height=600
        
        box_transfer = Box(app, width=300, height=200, border=1,layout='grid',align='right')
        #client
        client_file = Text(box_transfer, text="Client file",grid=[0,0])
        text_clientFile = TextBox(box_transfer,text="", grid=[10,0])
        text_clientFile.disable()
        PushButton(box_transfer, command=lambda: __transferFileWindow(),text="Search",grid=[20,0])
        
        #server
        server_file = Text(box_transfer, text="Server file", grid=[0,10])
        text_serverFile = TextBox(box_transfer, grid=[10,10])
        text_serverFile.disable()
        PushButton(box_transfer,command=lambda: __transferFileWindow(text_clientFile),text="Search",grid=[20,10])
        
        transfer_button = PushButton(box_transfer, command=__transfer_file,
                                             args=[text_clientFile, text_serverFile],
                                             text="Transfer", grid=[20,30])
        
    
    def __transfer_file(clientFile, serverFile):
        hsh.trahsh_file(clientFile.value, serverFile.value)
    
    def __transferFileWindow():
        
        file_name = filedialog.askopenfilename(initialdir = "/",title = "Select a File")
        #textBox.value = file_name
        hsh.trahsh_file_window()
    
    
    #I will try and use Tkinter here
    def ssh_select(): #Choose whether password or private-key should be used

        txtbox_passwd = TextBox(app)
        btn_pkey = PushButton(app, text="Use key")
    ssh_select()
    app.display()
app = tk_main()
app.geometry("1280x720")
app.mainloop()
