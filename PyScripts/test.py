from guizero import *
import tkinter as tk
from pathlib import Path
from io import StringIO
import paramiko, time, subprocess

target_ip = '192.168.1.119'
target_user = 'tom'
target_port = 22
target_password = 161198

def interactiveSSHShell():
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=target_ip, port=target_port, username=target_user, password=161198)
        while True:
            try:
                cmd = input("$> ")
                if cmd == "exit": break
                stdin, stdout, stderr = client.exec_command(cmd)
                print(stdout.read().decode())
            except KeyboardInterrupt:
                break 
        client.close()
    except Exception as err:
        print(str(err))
#interactiveSSHShell()


#RSA: static generate()
'''
If the shell is invoked explicitly, via shell=True, it is the application’s responsibility to ensure that 
all whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities.
'''
def add_keys_windows(pkey_path, target_user, target_pass): 
    #authorized_keysclear ???
# type %USERPROFILE%\.ssh\id_rsa.pub | ssh tom@192.168.1.119 "cat >> .ssh/authorized_keys"
#subprocess.run('"C:/Users/rette/.ssh/id_rsa.pub | ssh tom@192.168.1.119 cat >> .ssh/authorized_keys"',shell=True)
    command = f"type {pkey_path} | ssh {target_user}@192.168.1.119 'cat >> .ssh/authorized_keys'"
    return 1
def add_keys_linux(): #ssh-copy-id -i ~/.ssh/id_rsa.pub tom@192.168.1.119 -p 22
    #TODO: extend functionality to send the key to remote machine
    session = paramiko.SSHClient()
    session.load_system_host_keys()
    key_file = paramiko.RSAKey.from_private_key_file("C:/Users/rette/.ssh/id_rsa")
    session.connect(hostname=target_ip, username=target_user, pkey=key_file,
                        allow_agent=False, look_for_keys=False)

    session.close()

LARGE_FONT = ("Verdana", 12)
class tk_test(tk.Tk):
    #Runs on initialisation (load stuff)
    def __init__(self, *args, **kwargs): 
        #args: pass as much crap as you want (passing through values)
        #kwargs: key-word-arguments (passing through dictionaries)
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) #border of the window
        container.pack(side='top', fill='both', expand=True)
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        #frames are like sections to seperate widgets on the screen
        self.frames = {}

        for F in (StartPage,PageOne,PageTwo):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew ")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont] #key
        frame.tkraise()
def qf(stringtoprint):
    print(stringtoprint)
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside frame

        button1 = tk.Button(self, text="Use password",
                            #command=lambda: qf("This gets printed after")
                            command = lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = tk.Button(self, text="Use key",
                            #command=lambda: qf("This gets printed after")
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page one", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = tk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Page two",
                            command=lambda: controller.show_frame(PageOne))

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page two", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = tk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Page one",
                            command = lambda: controller.show_frame(PageOne))
        button2.pack()

app = tk_test()
app.mainloop()