import resaveCsv
import os
from tkinter import ttk
from tkinter import messagebox, Canvas, Label, Tk

# Root dir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')


def submit():
    cc = course_field.get()
    cc = cc.upper()
    feedback, flag = resaveCsv.update_list(cc)
    if flag:
        messagebox.showinfo("Update DB Prompt", feedback)
    else:
        messagebox.showerror("Update DB Prompt", feedback)


# GUI config
gui = Tk()
gui.title('Update Course List')
WIDTH = 300
HEIGHT = 200

Canvas(gui, height=HEIGHT, width=WIDTH).pack()
entry_frame = ttk.LabelFrame(gui, text='Update List')
footer_frame = ttk.LabelFrame(gui, text='Iriz Inc')

course_field = ttk.Entry(entry_frame)
clbl = Label(entry_frame, text='Course Code:', font='13')
button = ttk.Button(entry_frame, text='>> Start >>', command=submit)
entry_frame.place(anchor='n', relx=0.5, rely=0.05,
                  relheight=0.85, relwidth=0.9)
footer_frame.place(anchor='n', relx=0.5, rely=0.92,
                   relheight=0.08, relwidth=0.99)
button.place(anchor='n', relx=0.5, rely=0.6, relheight=0.3, relwidth=0.35)
clbl.place(anchor='n', relx=0.5, rely=0.02)
course_field.place(anchor='n', relx=0.5, rely=0.21,
                   relheight=0.21, relwidth=0.4)


def begin():
    if __name__ == '__main__':
        gui.mainloop()
