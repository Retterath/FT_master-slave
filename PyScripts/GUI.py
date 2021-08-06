import SFTP_lib
from guizero import *
from tkinter import filedialog
#Convention:
#display_NAME: for initializing the objects
#__NAME: to connect object values to the lib
#__NAME: use camelCase
# lambda function is NOT invoked right then and there
# we can also use .. , args=[] for command
def main():
    app = App(title='File transfer', width=800, height=600)
    
    def display_ping():
        box_ping = Box(app, width=300, height=200, border=1,layout='grid',align='left')
        PushButton(box_ping,command=lambda: __ping(input_box),text="Ping",grid=[0,0])
        input_box = TextBox(box_ping, grid=[10,0])
    def __ping(inputBox):
        SFTP_lib.ping_alex(inputBox.value)
            
#     def display_transfer_file():
#         box_transfer = Box(app, width=300, height=200, border=1, grid=[500,300],layout='grid')
#         #client
#         client_file = Text(box_transfer, text="Client file",grid=[600,500])
#         PushButton(app,command=lambda: __transferFileWindow(text_clientFile),text="Open explorer",grid=[610,500])
#         
#         text_clientFile = TextBox(box_transfer,text="", grid=[600,490])
#         #server
#         server_file = Text(box_transfer, text="Server file", grid=[600,450])
#         text_serverFile = TextBox(box_transfer, grid=[600,440])
#         #file
#         file_name = Text(box_transfer, text="File name", grid=[600,400])
#         text_server_fileName = TextBox(box_transfer, grid=[600,390])
#         
#         transfer_button = PushButton(app, command=__transfer_file,
#                                              args=[text_clientFile, text_serverFile,text_server_fileName],
#                                              text="Transfer", grid=[600,300])
#         PushButton(app,command=lambda: __transferFileWindow(text_clientFile),text="Open explorer",grid=[200,450])
#       
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
        SFTP_lib.transfer_file(clientFile.value, serverFile.value)
    
    def __transferFileWindow():
        
        file_name = filedialog.askopenfilename(initialdir = "/",title = "Select a File")
        #textBox.value = file_name
        SFTP_lib.transfer_file_window()
    
        
    display_transfer_file()
    display_ping()
    app.display()

main()