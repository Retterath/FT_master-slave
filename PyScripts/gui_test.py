from guizero import *
from tkinter import ttk #Like the CSS for tkinter
import tkinter as tk

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
        #args: pass as much crap as you want (passing through values)
        #kwargs: key-word-arguments (passing through dictionaries)
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "FT_Master-Slave")
        main_frame = tk.Frame(self, background="cyan", relief=tk.RAISED, borderwidth=5)
        
        #Make the window sticky for every case
        main_frame.grid(row=0, column=0)

        menubar = tk.Menu(main_frame)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command= lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)
        #frames are like main_frames, sections to seperate widgets on the screen
        self.frames = {}

        
        for F in (StartPage,PageOne,PageTwo):
            frame = F(main_frame,self)
            self.frames[F] = frame
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
        ent_ip = ttk.Entry(ssh_frame)
        ssh_btn_sett = ttk.Button(ssh_frame, text="More Settings", command=lambda: addit_sett(self.hidden, btn_pkey, lbl_pkey,
                                                                                            ssh_btn_sett, btn_hosts, lbl_hosts))
        ssh_btn_connect = tk.Button(ssh_frame, text="Connect", command=lambda:controller.ssh_connect())
        lbl_pkey = tk.Label(ssh_frame, text="Private Key")
        btn_pkey = ttk.Button(ssh_frame, text="Select", command=lambda:controller.ssh_pkey())
        lbl_hosts = ttk.Label(ssh_frame, text="Known hosts")
        btn_hosts = ttk.Button(ssh_frame, text="Select", command=lambda:controller.ssh_hosts())
        #functionality
        ent_ip.focus()
        #layout
        ssh_frame.columnconfigure(0, weight=1)
        ssh_frame.columnconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        #position 
        ssh_frame.grid(row=1, column=0)
        lbl_main.grid(row=0, column=0, pady=10, padx=10)  
        lbl_ip.grid(row=0, column=0, padx=10)
        ent_ip.grid(row=0, column=1)
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
                return self.hidden
            else:
                ssh_btn_sett['text'] = 'Hide Settings'        
                lbl_pkey.grid(row=3, column=0)
                btn_pkey.grid(row=3, column=1, sticky=tk.W)
                lbl_hosts.grid(row=4, column=0)
                btn_hosts.grid(row=4, column=1, sticky=tk.W)
                self.hidden = True
                return self.hidden
        
        
        

    
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page one", font=LARGE_FONT,relief=tk.GROOVE, borderwidth=5) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Page two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page two", font=LARGE_FONT,relief=tk.GROOVE, borderwidth=5) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Page one",
                            command = lambda: controller.show_frame(PageOne))
        button2.pack()

app = tk_main()
app.geometry("1280x720")
app.mainloop()