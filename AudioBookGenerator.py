import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from PyPDF2.utils import PdfReadError
import pyttsx3 as talk
import PyPDF2
import os
import pathlib
    
root = tk.Tk()
root.iconbitmap("E:\\Project\\Audio Book Generator\\Icons\\logo.ico")
root.resizable(width=False, height=False)
root.title("Audio Book Generator")
root.geometry('400x600')
root.configure(bg='#1e1d1d')

filename = ""
voice = tk.StringVar()
speed = tk.IntVar()

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a Book", 
                                          filetypes = (("PDF Files", "*.pdf*"), ("all files", "*.*")))
       
    # Change label contents 
    confirm.configure(fg = 'green', text="Book Selected: "+filename.split('/')[-1])
    

def Convert():
    error_label.configure(fg = "Green", text = "Converting. Please wait!")
    global filename
    global speed
    global voice
    error = False
    path = str(pathlib.Path().absolute())
    path += "\\AudioBooks"
    
    try:
        book = open(filename, "rb")
        pdfReader = PyPDF2.PdfFileReader(book, strict=False)
        pages = pdfReader.getNumPages()
        try:
            start_page = int(start_page_label.get())
            end_page = int(end_page_label.get())    
            if start_page <= 0:
                error_label.configure(fg = "Red", text = "Enter valid Starting page number")
                error = True
            elif end_page > pages:
                error_label.configure(fg = "Red", text = "Enter valid End page number")
                error = True
        except:
            error = True
            error_label.configure(fg = "Red", text = "Enter valid Page Numbers")
    except:
        error = True
        error_label.configure(fg = "Red", text = "Please select a book.")        
    
    
    
    allTexts = ""
    if not error:
        # error_label.configure(fg = "blue", text = "Converting. Please wait!")
        for page in range(start_page - 1, end_page):
            pageObj = pdfReader.getPage(page)
            allTexts += pageObj.extractText()
        
        if not os.path.exists(path):
            os.makedirs(path)
        speaker = talk.init('sapi5')
        voices = speaker.getProperty('voices')
        if voice.get() == "Male":
            speaker.setProperty('voice', voices[0].id)
        else:
            speaker.setProperty('voice', voices[1].id)
        speaker.setProperty('rate', speed.get())
        save = path + "\\" + (filename.split('/')[-1][:-4]) + ".mp3"
        speaker.save_to_file(allTexts, save)
        speaker.runAndWait()
        error_label.configure(fg = "green", text = "Audio Book created Successfully!")
        book.close()


img = ImageTk.PhotoImage(Image.open("E:\\Project\\Audio Book Generator\\Icons\\AudioBook.jpg"))
panel = tk.Label(root, image = img)
panel.place(x = 0, y = 0)
slogan = tk.Label(text = "Listen the book you want to..!", fg = "#E4E7DC", bg = "#1e1d1d", font=("Liberation Mono", 20))
slogan.place(x = 15, y = 205)

title = tk.Label(text = "Let's create one now!", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 15))
title.place(x = 93, y = 240)

label1 = tk.Label(text = "Select a Book", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 15))
label1.place(x = 35, y = 280)
button1 = tk.Button(root, text = "Any PDF File", command = browseFiles, bg='#33302e', fg='silver', width = 20)
button1.place(x = 190, y = 285)

confirm = tk.Label(root, text = "No book is selected!", fg = "grey", bg = "#1e1d1d");
confirm.place(x = 190, y = 310)

label2 = tk.Label(root, text = "Start Page", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 14))
label2.place(x = 40, y = 335)

start_page_label = tk.Entry(root, fg = "silver", bg = "#33302e")
start_page_label.insert(0, 'Enter Starting Page')
start_page_label.place(x = 190, y = 337, width = 150, height = 25)

label3 = tk.Label(root, text = "End Page", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 14))
label3.place(x = 40, y = 375)

end_page_label = tk.Entry(root, fg = "silver", bg = "#33302e")
end_page_label.insert(0, 'Enter Ending Page')
end_page_label.place(x = 190, y = 380, width = 150, height = 25)

label4 = tk.Label(root, text = "Select Voice", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 14))
label4.place(x = 40, y = 420)

voice.set("Male") # default value
select_voice = tk.OptionMenu(root, voice, "Male", "Female")
select_voice.config(bg = "#1e1d1d", fg = 'white', width=18)
select_voice['menu'].config(bg = "#1e1d1d", fg = 'white')
select_voice.place(x = 190, y = 420)

label5 = tk.Label(root, text = "Word / Minute", fg = "silver", bg = "#1e1d1d", font=("Liberation Mono", 14))
label5.place(x = 40, y = 465)

speed.set(200) # default value
select_speed = tk.OptionMenu(root, speed, 125, 150, 175, 200, 225, 250)
select_speed.config(bg = "#1e1d1d", fg = 'white', width = 18)
select_speed['menu'].config(bg = "#1e1d1d", fg = 'white')
select_speed.place(x = 190, y = 465)


submit = tk.Button(root, text = "Convert to Audiobook", command = Convert, bg='#3f2918', fg='white', width = 30, height = 2)
submit.place(x = 90, y = 520)

error_label = tk.Label(root, text = "", bg = "#1e1d1d")
error_label.place(x = 40, y = 570)

name_label = tk.Label(root, text = "- Kaushal Mistry", bg = "#1e1d1d", fg = "#90918c")
name_label.place(x = 300, y = 575)

root.mainloop()