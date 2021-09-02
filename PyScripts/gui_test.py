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
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    lbl = ttk.Label(popup, text=msg, font=NORM_FONT)
    lbl.pack(side="top", fill="x", pady=10)
    btn1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    btn1.pack()


class tk_test(tk.Tk):
    def __init__(self, *args, **kwargs): #Runs on initialisation (load stuff)
        #args: pass as much crap as you want (passing through values)
        #kwargs: key-word-arguments (passing through dictionaries)
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "FT_Master-Slave")
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command= lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)
        #frames are like containers, sections to seperate widgets on the screen
        self.frames = {}

        for F in (StartPage,PageOne,PageTwo):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew ")
        
        self.show_frame(StartPage)

        frame_a = tk.Frame()
        frame_b = tk.Frame()

        label_a = tk.Label(master=frame_a, text="Im in frame A")
        label_a.pack()
        label_b = tk.Label(master=frame_b, text="Im in frame B")
        label_b.pack()

        frame_a.pack()
        frame_b.pack()


    def show_frame(self, cont):
        frame = self.frames[cont] #key
        frame.tkraise()

#########
# Pages #
#########
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside frame

        button1 = ttk.Button(self, text="Use password",
                            command = lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text="Use key",
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page one", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Page two",
                            command=lambda: controller.show_frame(PageOne))

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page two", font=LARGE_FONT) 
        label.pack(pady=10, padx=10) #Padding outside label

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Page one",
                            command = lambda: controller.show_frame(PageOne))
        button2.pack()

app = tk_test()
app.geometry("1920x1080")
app.mainloop()