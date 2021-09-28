
import tkinter as tk


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('PanedWindow Demo')
root.geometry('300x200')

# change style to classic (Windows only) 
# to show the sash and handle
style = ttk.Style()
style.theme_use('classic')

# paned window
pw = ttk.PanedWindow(orient=tk.HORIZONTAL)

# Left listbox
left_list = tk.Listbox(root)
left_list.grid(row=0, column=0, sticky="ew")
pw.add(left_list)

# Right listbox
right_list = tk.Listbox(root)
right_list.grid(row=0, column=0, sticky="ew")
pw.add(right_list)

# place the panedwindow on the root window
#pw.pack(fill=tk.BOTH, expand=True)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# right_list.rowconfigure(0, weight=1)
# right_list.columnconfigure(0, weight=1)

# left_list.rowconfigure(0, weight=1)
# left_list.columnconfigure(0, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
# pw.columnconfigure(0, weight=1)
# pw.rowconfigure(0, weight=1)
# pw.rowconfigure(0, weight=1)
# pw.rowconfigure(1, weight=1)
# right_list.grid_rowconfigure(0, weight=1)
# right_list.grid_columnconfigure(0, weight=1)

# left_list.grid_columnconfigure(0, weight=1)
# left_list.grid_rowconfigure(0, weight=1)
# pw.grid_columnconfigure(0, weight=1)
# pw.grid_rowconfigure(0, weight=1)

pw.grid(row=0, column=0, sticky="nsew")
root.mainloop()