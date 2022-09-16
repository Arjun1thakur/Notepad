#importing required packages and libraries
from tkinter import *
from tkinter import ttk
from datetime import datetime
from tkinter  import font, messagebox,colorchooser
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import webbrowser
import os


#the root widget
root = Tk()
root.title('GOD Notepad')

ico = Image.open('icon.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

#creating scrollable notepad window
notepad = ScrolledText(root, width = 90, height = 40)
fileName = ''

#defining functions for commands
def cmdNew():
    global fileName
    if len(notepad.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            notepad.delete(0.0, END)
    root.title("GOD Notepad")
# create new tab
def cmdNewWin():
    pass

def cmdOpen():
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()     #t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)
text_url= " "
def cmdSave():     #file menu Save option
    global text_url
    try:
        if text_url:
            content = str(notepad.get(0.0,END))
            with open(text_url,'w',encoding="utf-8") as for_read:
                for_read.write(content)
        else:
            text_url = filedialog.asksaveasfile(mode='w',initialfile = 'Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            content2 = notepad.get(0.0,END)
            text_url.write(content2)
            text_url.close
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!") 
def cmdSaveAs():     #file menu Save As option
    fd = filedialog.asksaveasfile(mode='w',initialfile = 'Untitled.txt',
defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    t = notepad.get(0.0, END)     #t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")

def CustomText():
    messagebox.showinfo(title="Information",message="This feature is under process.")

def cmdUndo(self):
    if self.steps != 0:
        self.steps -= 1
        self.delete(0, END)
        self.insert(END, self.changes[self.steps])

def redo(self, event=None):
    if self.steps < len(self.changes):
        self.delete(0, END)
        self.insert(END, self.changes[self.steps])
        self.steps += 1
def cmdExit():     #file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()

def cmdCut():     #edit menu Cut option
    notepad.event_generate("<<Cut>>")

def cmdCopy():     #edit menu Copy option
    notepad.event_generate("<<Copy>>")

def cmdPaste():     #edit menu Paste option
    notepad.event_generate("<<Paste>>")

def cmdClear():     #edit menu Clear option
    notepad.event_generate("<<Clear>>")
       
def cmdFind():     #edit menu Find option
    notepad.tag_remove("Found",1.0, END)
    find = simpledialog.askstring("Find", "You need help to find something:")
    if find:
        idx = 1.0    #idx stands for index
    while 1:
        idx = notepad.search(find, idx , stopindex = END)
        if not idx:
            break
        lastidx = '%s+%dc' %(idx, len(find))
        notepad.tag_add('Found', idx, lastidx)
        idx = lastidx
    notepad.tag_config('Found', foreground = 'white', background = 'blue')
    notepad.bind("<1>", click)

def cmdreplace():
    def find():
        word = find_input.get()
        notepad.tag_remove("match", 1.0,END)
        matches = 0
        if word:
            start = 1.0
            while True:
                start =notepad.search(word, start,stopindex=END)
                if not start:
                    break
                    end = '%s+%dc' %(start, len(word))
                    notepad.tag_add("match", start,end)
                    start = end
                    notepad.tag_config("match",foreground="red",background="yellow")
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = notepad.get(1.0,END)
        new_content = content.replace(word, replace_text)
        notepad.delete(1.0,END)
        notepad.insert(1.0, new_content)

    find_pop = Toplevel()
    find_pop.geometry("450x200")
    find_pop.resizable(False, False)
    find_pop.title("Find and Replace")
    frame_find = LabelFrame(find_pop,text=" Find and replace words")
    frame_find.pack(pady=30,ipadx=30)

    text_find=Label(frame_find,text="Find")
    find_input = Entry(frame_find,width=30)
    find_button = Button(frame_find, text="Find",command=find)
    text_find.grid(row=0,column=0,padx=4,pady=4)

    text_replace = Label(frame_find,text="Replace")
    replace_input = Entry(frame_find,width=30)
    replace_button = Button(frame_find, text="Replace",command=replace)
    text_replace.grid(row=1,column=0,padx=4,pady=4)

    find_input.grid(row=0,column=1,padx=4,pady=4)
    replace_input.grid(row=1,column=1,padx=4,pady=4)
    find_button.grid(row=2,column=0,padx=8,pady=4)
    replace_button.grid(row=2,column=1,padx=8,pady=4)

def click(event):     #handling click event
    notepad.tag_config('Found',background='white',foreground='black')

def cmdSelectAll():     #edit menu Select All option
    notepad.event_generate("<<SelectAll>>")
    
def cmdTimeDate():     #edit menu Time/Date option
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)
    
def callback(url):
    webbrowser.open_new_tab(url)
def cmdAbout():
    label = messagebox.showinfo("About Notepad", "This notepad created by : Arjun singh")

show_statusbar = BooleanVar()
show_statusbar.set(True)
def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        statusbar.pack_forget()
        show_statusbar = False
    else:
        statusbar.pack(side=BOTTOM)
        show_statusbar = True

show_toolbar = BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        toolbar.pack_forget()
        show_toolbar = False
    else:
        notepad.pack_forget()
        statusbar.pack_forget()
        toolbar.pack(side=TOP,fill=BOTH)
        notepad.pack(fill=BOTH,expand=True)
        statusbar.pack(side=BOTTOM)
        show_toolbar = True
#notepad menu items
notepadMenu = Menu(root)
root.configure(menu=notepadMenu)

#file menu
fileMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='File', menu = fileMenu)

# File menu Opttions
fileMenu.add_command(label='New', command = cmdNew , accelerator = " Ctrl + N")
fileMenu.add_command(label='Open...', command = cmdOpen , accelerator = " Ctrl + O")
fileMenu.add_command(label='Save', command = cmdSave , accelerator = " Ctrl + S")
fileMenu.add_command(label='Save As...', command = cmdSaveAs)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command = cmdExit)

#edit menu
editMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Edit', menu = editMenu)

#Edit menu Options

editMenu.add_command(label='Cut', command = cmdCut, accelerator = " Ctrl + X")
editMenu.add_command(label='Copy', command = cmdCopy, accelerator = " Ctrl + C")
editMenu.add_command(label='Paste', command = cmdPaste, accelerator = " Ctrl + V")
editMenu.add_command(label='Delete', command = cmdClear)
editMenu.add_separator()
editMenu.add_command(label='Find...', command = cmdFind)
editMenu.add_command(label="Replace..",command=cmdreplace)
editMenu.add_separator()
editMenu.add_command(label='Select All', command = cmdSelectAll, accelerator = " Ctrl + A")
editMenu.add_command(label='Time/Date', command = cmdTimeDate)

# View options
ViewMenu = Menu(notepadMenu,tearoff=0)
ViewMenu.add_checkbutton(label="Tool Bar",onvalue= True , variable =  show_toolbar, offvalue = 0,command=hide_toolbar)
ViewMenu.add_checkbutton(label="Status Bar",onvalue= True, variable =  show_statusbar,offvalue = 0,command=hide_statusbar)
notepadMenu.add_cascade(label="View",menu=ViewMenu)

#help menu
helpMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Help', menu = helpMenu)

#toolbar

toolbar = Label(root, background="white")
toolbar.pack(side = TOP,fill=BOTH)
fonts_cat = font.families()
font_family = StringVar()
font_box = ttk.Combobox(toolbar,width = 20 , textvariable= font_family, state= 'readonly')
font_box["values"] = fonts_cat
font_box.current(fonts_cat.index("Courier New"))
font_box.grid(row=0, column =1 ,padx=5)


font_var = IntVar()
font_size = ttk.Combobox(toolbar,width=5,textvariable= font_var, state = "readonly")
font_size["values"]= tuple(range(0,100,2))
font_size.current(5)
font_size.grid(row=0,column=3,padx=5) 

font_now ='Arial'
font_size = 16
def change_font(root):
    global font_now
    font_now  = font_family.get()
    notepad.configure(font = (font_now,font_size))

def change_size(root):
    global font_size
    font_size= font_var.get()
    notepad.configure(font=(font_now,font_size))

""" font_size.bind("<<ComboboxSelected>>",change_size) """
font_box.bind("<<ComboboxSelected>>", change_font)


bold_icon = PhotoImage(file = "Bold.png")
bold_btn = Button(toolbar, image = bold_icon, bd=0, highlightthickness=0,background="white")
bold_btn.grid(row=0,column=4, padx=8)
def bold_fun():
    text_get = font.Font(font=notepad["font"])
    if text_get.actual()["weight"] == "normal":
        notepad.configure(font=(font_now,font_size,"bold"))
    if text_get.actual()["weight"] == "bold":
        notepad.configure(font=(font_now,font_size,"normal"))
bold_btn.configure(command= bold_fun)

italic_icon = PhotoImage(file = "i.png")
italic_btn = Button(toolbar, image = italic_icon, bd=0, highlightthickness=0,background="white")
italic_btn.grid(row=0,column=5,padx=8)

def italic_fun():
    text_get = font.Font(font=notepad["font"])
    if text_get.actual()["slant"] == "roman":
        notepad.configure(font=(font_now,font_size,"italic"))
    if text_get.actual()["slant"] == "italic":
        notepad.configure(font=(font_now,font_size,"roman"))
italic_btn.configure(command= italic_fun)

underline_icon = PhotoImage(file = "underline.png")
underline_btn = Button(toolbar, image = underline_icon, bd=0, highlightthickness=0,background="white")
underline_btn.grid(row=0,column=6,padx=8)

def underline_fun():
    text_get = font.Font(font=notepad["font"])
    if text_get.actual()["underline"] == 0:
        notepad.configure(font=(font_now,font_size,"underline"))
    if text_get.actual()["underline"] == 1:
        notepad.configure(font=(font_now,font_size,"normal"))
underline_btn.configure(command= underline_fun)

overstrike_icon = PhotoImage(file = "overstrike.png")
overstrike_btn = Button(toolbar, image = overstrike_icon, bd=0, highlightthickness=0,background="white")
overstrike_btn.grid(row=0,column=7,padx=8)

def overstrike_fun():
    text_get = font.Font(font=notepad["font"])
    if text_get.actual()["overstrike"] == 0:
        notepad.configure(font=(font_now,font_size,"overstrike"))
    if text_get.actual()["overstrike"] == 1:
        notepad.configure(font=(font_now,font_size,"normal"))
overstrike_btn.configure(command= overstrike_fun)

color_icon = PhotoImage(file = "color.png")
color_btn = Button(toolbar, image = color_icon, bd=0, highlightthickness=0,background="white")
color_btn.grid(row=0,column=8,padx=8)

def color_fun():
    color = colorchooser.askcolor()
    notepad.configure(fg=color[1])
color_btn.configure(command=color_fun)

highlighter_img = PhotoImage(file = "highlighter.png")
highlighter = Button(toolbar, image = highlighter_img, bd=0, highlightthickness=0,background="white",command=CustomText)
highlighter.grid(row=0,column=9,padx=8)

""" def highlighter_fun():
    def printInput():
        inp = notepad.get(1.0, "end-1c")
        notepad.config(inp)
    color = colorchooser.askcolor()
    notepad.configure(background=color[1])
highlighter.configure(command=highlighter_fun) """

alignleft_icon = PhotoImage(file = "alignleft.png")
alignleft_btn = Button(toolbar,image = alignleft_icon, bd=0, highlightthickness=0,background="white")
alignleft_btn.grid(row=0,column=10,padx=8)
def align_left_cmd():
    text_get = notepad.get(1.0,END)
    notepad.tag_config("left",justify=LEFT)
    notepad.delete(1.0,END)
    notepad.insert(INSERT, text_get,"left")
alignleft_btn.configure(command=align_left_cmd)

aligncenter_icon = PhotoImage(file = "aligncenter.png")
aligncenter_btn = Button(toolbar,image = aligncenter_icon, bd=0, highlightthickness=0,background="white")
aligncenter_btn.grid(row=0,column=11,padx=8)
def align_center_cmd():
    text_get = notepad.get(1.0,END)
    notepad.tag_config("center",justify=CENTER)
    notepad.delete(1.0,END)
    notepad.insert(INSERT, text_get,"center")
aligncenter_btn.configure(command=align_center_cmd)

alignright_icon = PhotoImage(file = "alignright.png")
alignright_btn = Button(toolbar,image = alignright_icon, bd=0, highlightthickness=0,background="white")
alignright_btn.grid(row=0,column=12,padx=8)
def align_right_cmd():
    text_get = notepad.get(1.0,END)
    notepad.tag_config("right",justify=RIGHT)
    notepad.delete(1.0,END)
    notepad.insert(INSERT, text_get,"right")
alignright_btn.configure(command=align_right_cmd)

ttk.Separator(toolbar, orient=VERTICAL).grid(column=13, row=0, rowspan=3, sticky='ns')

clock_icon = PhotoImage(file = "clock.png")
clock_btn = Button(toolbar,image = clock_icon, bd=0, highlightthickness=0,background="white",command=cmdTimeDate)
clock_btn.grid(row=0,column=14,padx=15)
# status bar 
statusbar = Label(root , text="Status Bar")
statusbar.pack(side = BOTTOM,fill=BOTH)

text_data = False
def text_count(event = None):
    global text_data
    if notepad.edit_modified():
        text_data = True
        word = len(notepad.get(1.0,"end-1c").split())
        character = len(notepad.get(1.0,"end-1c").replace(" ",""))
        statusbar.config(text = f'Character :{(character) }| Word:{(word)}')
    notepad.edit_modified(False)
notepad.bind("<<Modified>>",text_count)

ttk.Separator(toolbar, orient=VERTICAL).grid(column=18, row=0, rowspan=3, sticky='ns')

search_img = PhotoImage(file="search.png")
link_creator = Label(toolbar, text="Creator info ",background="white")
link_creator.grid(row=0,column=19)
link = Label(toolbar, image=search_img, bd=0, highlightthickness=0,background="white",cursor="hand2")
link.grid(row=0, column=20)  
link.bind("<Button-1>", lambda e:
callback("https://arjun1thakur.github.io/Single-page-detail/"))
#adding options in help menu
helpMenu.add_command(label='About Notepad', command = cmdAbout)
notepad.pack(expand=True,fill=BOTH)
root.mainloop()
