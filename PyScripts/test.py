from guizero import *
from tkinter import filedialog
import paramiko
hostname = "127.0.0.1"
port = 22
user = "tom"
passwd = "starwars"
def test1():
    app = App(title='Lane Control', width=1000, height=600,layout='grid',bg=(88,129,101))
    app.text_size = 20
    box_ping = Box(app, width=400, height=200, border=1, grid=[100,500],layout='grid')                          
    
    input_box = TextBox(box_ping,grid=[100,400])
    PushButton(box_ping,text="Ping", grid=[100,300])
    
#     button_explore = Button(app,
#                         text = "Browse Files",
#                         command = open_window)
    PushButton(app,command=lambda: open_window(),text="Open explorer",grid=[200,450])
    app.display()
def open_window():
    
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File")
def interactiveSSHShell():
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=user, password=passwd)
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
interactiveSSHShell()
#test1()