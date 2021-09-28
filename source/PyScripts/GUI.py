from guizero import *
from tkinter import BooleanVar, Menu, StringVar, ttk #Like the CSS for tkinter
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

def openCLI():
    window = tk.Toplevel() #window that has an independent existence under the window manager
    window.lift()
    window.geometry('1334x486+150+150')
    window.resizable(width=True, height=True)
    window.title("Remote CLI")
    w_id = window.winfo_id()
    os.system('xterm -into %d -geometry 230x50 -sb &' % w_id)
class tk_main(tk.Tk):    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "FT_Master-Slave")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        container = tk.Frame(self, background="bisque", relief=tk.RAISED, borderwidth=5) 
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #TODO: Add delete_all_local_keys option
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command= lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        sshbar = tk.Menu(container, tearoff=0)
        sshbar.add_command(label="Open CLI", command= lambda: openCLI())
        sshbar.add_separator()
        menubar.add_cascade(label="Extra", menu=sshbar)
        tk.Tk.config(self, menu=menubar)



        self.frames = {}        
        for F in (StartPage,PageMatPlot):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")             
        self.show_frame(StartPage)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
#########
# Pages #
#########
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)        
        self.sett_state = BooleanVar(self, value = False)
        self.usr = StringVar(self)
        self.pwd = StringVar(self)
        self.ip = StringVar(self)
        self.pkey_path = StringVar(self)
        self.host_path = StringVar(self)

        # Frames
        frm_nav = tk.Frame(self, bg="bisque2")        
        ssh_conn_frame = ttk.LabelFrame(self, text="SSH connect", height=60)
        ssh_status_frame = ttk.LabelFrame(self, text="Status")
        ssh_output_frame = ttk.LabelFrame(self, text="Output", relief=tk.SUNKEN, borderwidth=5)
        
        # Entries
        ent_user = ttk.Entry(ssh_conn_frame, textvariable=self.usr)
        ent_pass = ttk.Entry(ssh_conn_frame, show='*', textvariable=self.pwd)
        ent_ip = ttk.Entry(ssh_conn_frame, textvariable=self.ip)
        self.ent_pkey = ttk.Entry(ssh_conn_frame, state='disabled', textvariable=self.pkey_path)
        self.ent_host = ttk.Entry(ssh_conn_frame, state='disabled', textvariable=self.host_path)

        ent_pass.insert(0, '161198')
        ent_ip.insert(0, '192.168.122.174')
        ent_user.insert(0, 'server')

        # Labels
        lbl_user = ttk.Label(ssh_conn_frame, text="Username")
        lbl_sett = ttk.Label(ssh_conn_frame, text="More Settings")
        self.lbl_ping = tk.Label(ssh_conn_frame, width=5, fg='green')
        lbl_pass = ttk.Label(ssh_conn_frame, text="Password:")
        lbl_ip = ttk.Label(ssh_conn_frame, text="IP Address:")
        self.lbl_pkey = tk.Label(ssh_conn_frame, text="Private Key", width=10, justify=tk.LEFT)
        self.lbl_hosts = ttk.Label(ssh_conn_frame, text="Known host", width=10, justify=tk.LEFT)
         
        # Buttons & Checkbuttons
        chk_btn = tk.Checkbutton(ssh_conn_frame, variable=self.sett_state, command= lambda: addit_sett())
        btn_ping = ttk.Button(ssh_conn_frame, text="Ping", command=lambda: Ssh.ping(self))
        btn_home = ttk.Button(frm_nav, text="Homepage")
        btn_matplot = ttk.Button(frm_nav, text="Matplotlib", command=lambda: controller.show_frame(PageMatPlot))
        btn_conn = tk.Button(ssh_conn_frame, text="Connect", command=lambda: Ssh.connect(self))
        btn_key = ttk.Button(ssh_conn_frame, text="Select", state='disabled',command=lambda: self.file_window('Select a private key', 'btn_pkey'))
        btn_host = ttk.Button(ssh_conn_frame, text="Select", state='disabled',command=lambda:self.file_window('Select a host file', 'btn_hosts'))
        
        # Text
        self.txt_status = tk.Text(ssh_status_frame,state='disabled', font=('Courier New', 11), width=40, height=5)
        txt_data = tk.Text(ssh_output_frame, state='disabled', font=('Arial', 16), width=30, height=6)
        #functionality
        ent_ip.focus() 
        
        # layout of columns/rows
        self.grid_columnconfigure(0, weight=1, minsize=450)
        self.grid_rowconfigure(0, weight=1, minsize=30)
        
        #layout of frames
        frm_nav.grid(row=0, column=0, sticky="ew")
        ssh_conn_frame.grid(row=1, column= 0, sticky="w")
        ssh_status_frame.grid(row=2, column=0, sticky="ew")
        ssh_output_frame.grid(row=2, column=4, sticky="ew")
        
        #layout of labels
        lbl_user.grid(row=1, column=0, sticky="w")
        self.lbl_pkey.grid(row=4, column=0)
        self.lbl_hosts.grid(row=5, column=0)
        lbl_sett.grid(row=3, column=0)
        self.lbl_ping.grid(row=0, column=3)
        lbl_ip.grid(row=0, column=0, padx=1, sticky="w")
        lbl_pass.grid(row=2, column=0, padx=1, sticky="w")
        
        #layout of entities        
        ent_user.grid(row=1, column=1)
        ent_ip.grid(row=0, column=1, padx=10, pady=1, sticky="e")
        ent_pass.grid(row=2, column=1, padx=10, pady=3, sticky="e")
        self.ent_pkey.grid(row=4, column=1)
        self.ent_host.grid(row=5, column=1)
        
        #layout of texts
        self.txt_status.grid(row=0, column=0, sticky="ew")
        txt_data.grid(row=0, column=0, sticky="ew")

        #layout of buttons & checkbuttons
        btn_key.grid(row=4, column=2, sticky="w")
        btn_host.grid(row=5, column=2, sticky="w")
        chk_btn.grid(row=3, column=1, sticky="w")
        btn_ping.grid(row=0, column=2)
        btn_home.grid(row=0, column=0, sticky="nw")
        btn_matplot.grid(row=0, column=1, sticky="nw")
        btn_conn.grid(row=3, column=3, padx=2, pady=2, sticky="w")
    
        def addit_sett():
            if self.sett_state.get():
                self.ent_pkey.config(state='enabled')
                self.ent_host.config(state='enabled')
                btn_key.config(state='enabled')
                btn_host.config(state='enabled')
            else: 
                self.ent_pkey.config(state='disabled')
                self.ent_host.config(state='disabled')
                btn_key.config(state='disabled')
                btn_host.config(state='disabled')
            return self.sett_state
    
    def file_window(self, w_name, lbl):
        work_dir = Path('source','Keys', 'RSA')
        remote_file = filedialog.askopenfilename(initialdir = Path().home(), title = w_name)
        local_file = Path(remote_file)

        if not remote_file: return None
            
        if lbl == 'btn_pkey':
            self.ent_pkey.insert(0, local_file)

        elif lbl == 'btn_hosts':
            self.ent_host.insert(0, local_file)

        with local_file.open(mode = 'r') as f:
            work_dir.write_text(f.read())

        return remote_file
class Ssh(StartPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
    def connect(self):    
        target_pass = self.pwd.get()
        target_ip = self.ip.get()
        pkey = self.pkey_path.get()
        host = self.host_path.get()
        user = self.usr.get()
        
        if (pkey=='') or (host==''):
            session = hsh.ssh_raw_conn(target_ip = target_ip, 
                    target_pass = target_pass, 
                    user = user)
            self.txt_status.config(state='normal')
            self.txt_status.insert(tk.END, "Connected:\n")
            stdin, stdout, stderr = session.exec_command('whoami')
            output = stdout.read().decode()
            self.txt_status.insert(tk.END, output)

        else:
            session = hsh.ssh_conn(target_ip, target_pass, 22)

        # They are file objects => they need to be closed
        stdin.close()
        stdout.close()
        stderr.close()
        session.close()
    def ping(self):
        target_ip = self.ip.get()
        status = hsh.ping_ssh(target_ip)
        if status == "ON":
            self.lbl_ping.config(text = status, fg='green')
            return
        self.lbl_ping.config(text = status, fg='red')
        return
class PageMatPlot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Matplotlib page", font=LARGE_FONT,relief=tk.GROOVE, borderwidth=5) 
        label.pack(pady=10, padx=10) 

        button1 = ttk.Button(self, text="Back to Homepage",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
       

app = tk_main()
#app.geometry('{}x{}'.format(960, 350))
app.mainloop()
