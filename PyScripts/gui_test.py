from guizero import *
from tkinter import Grid, ttk #Like the CSS for tkinter
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
        main_frame.grid_columnconfigure(0,weight=1) 
        main_frame.grid_rowconfigure(1, weight=1)
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


        label_a = tk.Label(master=main_frame, text="Im in frame main_frame")
        label_a.grid(row=2, column=2)
        label_b = tk.Label(master=main_frame, text="Im in frame main_frame too")
        label_b.grid(row=2, column=3)


    def show_frame(self, cont):
        frame = self.frames[cont] #key
        frame.tkraise()

#########
# Pages #
#########
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        
        label = tk.Label(self, text="Start Page", font=LARGE_FONT,relief=tk.GROOVE, borderwidth=5) 
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