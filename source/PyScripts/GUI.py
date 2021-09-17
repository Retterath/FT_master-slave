from guizero import *
from tkinter import ttk #Like the CSS for tkinter
import tkinter as tk
import handshake as hsh
import shutil
from pathlib import Path

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
        # Frames
        lbl_main = ttk.Label(self, text="Homepage", font=LARGE_FONT, borderwidth=5)
        ssh_conn_frame = ttk.LabelFrame(self, text="SSH connect")
        ssh_status_frame = ttk.LabelFrame(self, text="Status", height=100, width=300)
        ssh_output_frame = ttk.LabelFrame(self, text="Output", relief=tk.SUNKEN, borderwidth=5, height=200, width=700)
        
        # Entities
        self.ent_pass = ttk.Entry(ssh_conn_frame, show='*')
        self.ent_ip = ttk.Entry(ssh_conn_frame)
        
        # Labels
        lbl_pass = ttk.Label(ssh_conn_frame, text="Password:")
        lbl_ip = ttk.Label(ssh_conn_frame, text="IP Address:")
        self.lbl_pkey = tk.Label(ssh_conn_frame, width=10, text="Private Key")
        self.lbl_hosts = ttk.Label(ssh_conn_frame, width=10, text="Known hosts")
        
        # Buttons
        #TODO: Add a ping button with the option (ckeckbox) <- if checked, ping every N seconds
        ssh_btn_connect = tk.Button(ssh_conn_frame, text="Connect", command=lambda: Ssh.connect(self))
        self.btn_pkey = ttk.Button(ssh_conn_frame, text="Select", command=lambda: self.file_window('Select a private key', 'btn_pkey'))
        self.btn_hosts = ttk.Button(ssh_conn_frame, text="Select", command=lambda:self.file_window('Select a host file', 'btn_hosts'))
        ssh_btn_sett = ttk.Button(ssh_conn_frame, text="More Settings", command=lambda: addit_sett(self))
        #functionality
        self.ent_ip.focus() 

        #layout of columns/rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        ssh_conn_frame.grid_rowconfigure(1, weight=1)
        ssh_conn_frame.grid_columnconfigure(0, weight=1)
        ssh_output_frame.grid_columnconfigure(1, weight=1)
        ssh_output_frame.grid_rowconfigure(1, weight=1)
        #w_id = ssh_status_frame.winfo_id()
        #os.system('xterm -into %d -geometry 40x20 -sb &' % w_id)
        
        #layout of frames
        ssh_conn_frame.grid(row=1, column= 0, sticky="w")
        ssh_status_frame.grid(row=2, column=0, sticky="w")
        ssh_output_frame.grid(row=1, column=1, sticky="e")
        
        #layout of labels
        lbl_main.grid(row=0, column=0, pady=10, padx=10, sticky="nw")  
        lbl_ip.grid(row=0, column=0, padx=1, sticky="w")
        lbl_pass.grid(row=1, column=0, padx=1, sticky="w")
        
        #layout of entities
        self.ent_ip.grid(row=0, column=1, padx=10, pady=1, sticky="e")
        self.ent_pass.grid(row=1, column=1, padx=10, pady=3, sticky="e")
        
        #layout of buttons
        ssh_btn_connect.grid(row=2, column=1, padx=2, pady=2, sticky="w")
        ssh_btn_sett.grid(row=2, column=0, padx=2, pady=2, sticky="w")
    
        def addit_sett(self):
            if self.hidden:
                ssh_btn_sett['text'] = 'More Settings'
                self.lbl_pkey.grid_forget()
                self.btn_pkey.grid_forget()
                self.btn_hosts.grid_forget()
                self.lbl_hosts.grid_forget()
                self.hidden = False
            else:
                ssh_btn_sett['text'] = 'Hide Settings'        
                self.lbl_pkey.grid(row=3, column=0)
                self.btn_pkey.grid(row=3, column=1, sticky=tk.W)
                self.lbl_hosts.grid(row=4, column=0)
                self.btn_hosts.grid(row=4, column=1, sticky=tk.W)
                self.hidden = True
            return self.hidden
    @staticmethod
    def get_ent_text(self):
        return {'ip':self.ent_ip.get(), 'pass':self.ent_pass.get()}
    
    def file_window(self, w_name, lbl): #works, but not safe. TODO: read bytes instead
        to_cwd_path = Path('Keys', 'RSA')
        from_file = filedialog.askopenfilename(initialdir = Path().home().joinpath('.ssh'),title = w_name)
        from_file_path = Path(from_file)
        if not from_file:
            return None
        if lbl == 'btn_pkey':
            self.lbl_pkey.configure(text=from_file_path.name)
        elif lbl == 'btn_hosts':
            self.lbl_hosts.configure(text=from_file_path.name)
        with from_file_path.open(mode = 'r') as f:
            to_cwd_path.write_text(f.read())
        return from_file    
class Ssh(StartPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
    def connect(self): #works        
        cred = StartPage.get_ent_text(self) #TODO: Add port
        pkey = self.btn_pkey
        hosts = self.btn_hosts 

        #if privatekey and knownhosts are None -> connect raw
        if (pkey is None) or (hosts is None):
            session = hsh.ssh_raw_conn(target_ip=cred['ip'], target_pass=cred['pass'])
        else:
            session = hsh.ssh_conn(cred['ip'], cred['pass'], 22)
        
        #session = hsh.ssh_raw_conn(target_ip=text['ip'], target_pass=text['pass'])
        #session.exec_command("ifconfig")

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
    
    
    
    
    app.display()
app = tk_main()
app.geometry('{}x{}'.format(960, 350))
app.mainloop()
