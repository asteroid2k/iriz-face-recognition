from ctypes import windll

import mongohelper as myh
import mongoengine as mg
import pandas as pd
import os
from tkinter import ttk
from tkinter import Menu, Listbox, END, IntVar, Canvas, Label, Tk
import time
import recognize_video
import multiprocessing
import logcsv

# Root dir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# msg tags for user
msgtags = ['[SUCCESS]:', '[INFO]:', '[ERROR]:']

# connect to database
myh.global_init()

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')
# GUI config
gui = Tk()
WIDTH = 500
HEIGHT = 600
pnlim = 6
idlim = 8


# --------------------------------------------HELPER FUNCTIONS----------------------------------------------------------

# Create directories for attendance data and student list for each course


def helper_init():
    sl = os.path.join(BASE, 'StudentList')
    ad = os.path.join(BASE, 'AttendanceData')
    if not os.path.isdir(sl):
        logger(f'{msgtags[1]}making student list dir...')
        os.makedirs(sl)
        logger(f'{msgtags[0]}done')
    if not os.path.isdir(ad):
        logger(f'{msgtags[1]}making attendance list dir...')
        os.makedirs(ad)
        logger(f'{msgtags[0]}done')


# Build csv file with student list


def build_csv(course_code=None, student_list=None):
    cc = str(course_code) + '_attendance.csv'
    filecsv = os.path.join(BASE, 'AttendanceData', cc)
    if student_list is None:
        logger(f'{msgtags[1]}Empty Student List')
    else:
        if os.path.exists(filecsv) and os.path.isfile(filecsv):
            logger(f'{msgtags[1]}Loading Csv file')
            df = pd.read_csv(filecsv)
            logger(f'{msgtags[0]}Done')
            return df
        else:
            logger(f'{msgtags[1]}Building Csv file')
            data = dict()
            data['ID'] = student_list
            df = pd.DataFrame(data)
            df.sort_values(by='ID', inplace=True)
            df.drop_duplicates(subset='ID', keep=False, inplace=True)
            df['Ototal'] = None
            df = df.append({'ID': 'Dtotal'}, ignore_index=True)
            df = calc_total(df)
            df.to_csv(filecsv, index=False)
            logger(f'{msgtags[0]}Done')
        return df


# calculate daily totals and total attendance for each student


def calc_total(df):
    df.iloc[-1, 1:-1] = df.iloc[:-1, 1:-1].sum(axis=0)
    df['Ototal'] = df.iloc[:, 1:-1].sum(axis=1)
    return df


# parse and get compile unique student ids from student list


def get_class_list(course_code=None):
    course_list = parse_list(course_code)
    if course_list is None:
        logger(f'{msgtags[2]}{course_code} Student list was not found')
        return None
    else:
        course_list = list(dict.fromkeys(course_list))
        return course_list


# parse student list


def parse_list(course_code):
    logger(f'{msgtags[1]}Parsing Student list')
    cc = str(course_code) + '_list.txt'
    clist = os.path.join(BASE, 'StudentList', cc)
    course_list = list()
    if os.path.exists(clist) and os.path.isfile(clist):
        with open(clist, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    course_list.append(line)
        return course_list
    else:
        return None


# add new student to records


def add_student(idn, df):
    r = df.shape[0]
    students = df['ID']
    if idn not in students:
        df.drop([r - 1], axis=0, inplace=True)
        df = df.append({'ID': str(idn)}, ignore_index=True)
        df = df.append({'ID': 'Dtotal'}, ignore_index=True)
        return df


# Sort entries by ID


def sort_df(df):
    df.sort_values(by='ID', inplace=True)
    df.drop_duplicates(subset='ID', keep=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# construct csv


def construct_file(course_code):
    clit = get_class_list(course_code)
    if clit is not None:
        build_csv(course_code, clit)


def check_list(ccode):
    cc = str(ccode) + '_list.txt'
    clist = os.path.join(BASE, 'StudentList', cc)
    if os.path.exists(clist) and os.path.isfile(clist):
        logger(f'{msgtags[0]}Course List found.....')
        return True
    else:
        logger(f'{msgtags[2]}Course List not found.....')
        logger(f'..............Exiting............')
        return False


# def mytest():
#     course = 'CPEN419'
#     filename = course + '_attendance.csv'
#     csvv = os.path.join(BASE, 'AttendanceData', filename)
#     construct_file(course)
#     dataframe = pd.read_csv(csvv)
#     add_day("02/02/2020", dataframe)
#     add_record("10628439", "02/02/2020", dataframe)
#     add_record("10656987", "02/02/2020", dataframe)
#     add_record("11258874", "02/02/2020", dataframe)
#     add_record("10223322", "02/02/2020", dataframe)
#     add_day("04/02/2020", dataframe)
#     add_record("10628439", "04/02/2020", dataframe)
#     add_record("10656987", "04/02/2020", dataframe)
#     add_record("11258874", "04/02/2020", dataframe)
#     add_record("10223322", "04/02/2020", dataframe)
#     add_day("08/02/2020", dataframe)
#     add_record("10628439", "08/02/2020", dataframe)
#     add_record("10656987", "08/02/2020", dataframe)
#     add_record("11258874", "08/02/2020", dataframe)
#     add_record("10223322", "08/02/2020", dataframe)
#     add_day("12/02/2020", dataframe)
#     add_record("10628439", "12/02/2020", dataframe)
#     add_record("10215588", "12/02/2020", dataframe)
#     add_record("10656987", "12/02/2020", dataframe)
#     add_record("10236587", "12/02/2020", dataframe)
#     add_record("10656987", "12/02/2020", dataframe)
#     add_record("11258874", "12/02/2020", dataframe)
#     add_record("10223322", "12/02/2020", dataframe)
#     calc_total(dataframe)
#     dataframe.to_csv(csvv, index=False)
#
#     print(dataframe)
#     exit(9000)


# -----------------------------------------------GUI FUNCTIONS---------------------------------------------------------
def run_face(c):
    time.sleep(0.2)
    recognize_video.init(c)


def submit():
    helper_init()
    idn = ID.get()
    pn = pin.get()
    sub = checkvar.get()
    ccde = course_field.get().upper()
    proceed = validate(idn, pn, ccde)
    if proceed:
        try:
            course = myh.Course.objects(code__iexact=ccde).get()
        except mg.DoesNotExist:
            logger(f"{msgtags[2]}Course with code '{ccde}' not found")
        else:
            try:
                tutor = myh.TutorInfo.objects(ID=idn).get()
            except mg.DoesNotExist:
                logger(f"{msgtags[2]}No Tutor with ID '{idn}' exists")
            else:
                if tutor.pin != pn:
                    logger(f"{msgtags[2]}Invalid Pin")
                else:
                    if not sub and ccde not in tutor.courses:
                        logger(
                            f"{msgtags[2]}{tutor.name} does not take {ccde}...")
                        logger(
                            "...Check the checkbox above if you are a substitute Tutor")
                    else:
                        mm = 'as sub Tutor' if sub else ''
                        logger(f"____________________BOOT____________________")
                        logger(
                            f"{msgtags[1]}initialising {course.name}: {ccde} {mm}")
                        a = check_list(ccde)
                        # Start RFID and FACE Detection

                        gui.update()
                        if a:
                            construct_file(ccde)
                            logger(f"____________________Lauching Iriz____________________")
                            gui.update()

                            loggerprocess = multiprocessing.Process(target=logcsv.bootlogger, args=(ccde,))
                            faceprocess = multiprocessing.Process(target=run_face, args=(ccde,))
                            faceprocess.start()
                            loggerprocess.start()
                            gui.update()
                            gui.after(100)
                            faceprocess.join()
                            loggerprocess.join()


def validate(idn, pn, ccde):
    if len(ccde) < 5:
        course_val.config(fg='red', text=f'Not enough characters')
    else:
        course_val.config(fg='green', text=f'Ok')

    if len(idn) < idlim or len(idn) > idlim:
        id_val.config(fg='red', text=f'ID must be {idlim} digits')
        return False
    else:
        id_val.config(fg='green', text='Ok')
    if len(pn) < pnlim or len(pn) > pnlim:
        pin_val.config(fg='red', text=f'Pin must be {pnlim} digits')
        return False
    else:
        pin_val.config(fg='green', text='Ok')
    return True


def logger(txt):
    log.insert(END, txt)


def openUdb():
    import GoeyUpdateDB
    GoeyUpdateDB.begin()


def openUlt():
    import GoeyUpdateList
    GoeyUpdateList.begin()


# ------------------------------------------------GUI-------------------------------------------------------------------
# Gooey   GOOOOEEEYYY             #GOOOOOOOOOEEEEEEEEEYYYYYYYYY

checkvar = IntVar()
menubar = Menu(gui)
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Update DB", command=openUdb)
filemenu.add_command(label="Update CourseList", command=openUlt)
filemenu.add_command(label="Exit", command=gui.quit)
menubar.add_cascade(label="File", menu=filemenu)
# Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="How-to")
filemenu.add_separator()
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)

Canvas(gui, height=HEIGHT, width=WIDTH).pack()
entry_frame = ttk.LabelFrame(gui, text='Info')
log_frame = ttk.LabelFrame(gui, text='Log')
footer_frame = ttk.LabelFrame(gui, text='Iriz Inc')
log_scroll = ttk.Scrollbar(log_frame)
log = Listbox(
    log_frame, yscrollcommand=log_scroll.set, font='Courier 9')
log_scroll.config(command=log.yview)

checkb = ttk.Checkbutton(
    entry_frame, text='Substitute Tutor?', variable=checkvar)

button = ttk.Button(entry_frame, text='>> Start >>', command=submit)
course_field = ttk.Entry(entry_frame)
pin = ttk.Entry(entry_frame)
ID = ttk.Entry(entry_frame)
entry_frame.place(anchor='n', relx=0.5, rely=0.05,
                  relheight=0.44, relwidth=0.75)
log_frame.place(anchor='n', relx=0.5, rely=0.52, relheight=0.38, relwidth=0.95)
footer_frame.place(anchor='n', relx=0.5, rely=0.92,
                   relheight=0.08, relwidth=0.99)
menu_bar = Menu(entry_frame)

clbl = Label(entry_frame, text='Course Code:')
idlbl = Label(entry_frame, text='ID:')
pinlbl = Label(entry_frame, text='PIN:')
id_val = Label(entry_frame, text='Enter 8 digit ID',
               font='Verdana 7 italic')
pin_val = Label(entry_frame, text='Enter 6 digit pin code',
                font='Verdana 7 italic')
course_val = Label(entry_frame, text='Enter Course Code',
                   font='Verdana 7 italic')

button.place(anchor='n', relx=0.5, rely=0.815, relheight=0.18, relwidth=0.25)
idlbl.place(anchor='n', relx=0.078, rely=0.015)
ID.place(anchor='n', relx=0.25, rely=0.11, relheight=0.15, relwidth=0.4)
id_val.place(anchor='n', relx=0.25, rely=0.26)
pinlbl.place(anchor='n', relx=0.69, rely=0.015)
pin.place(anchor='n', relx=0.8, rely=0.11, relheight=0.15, relwidth=0.3)
pin_val.place(anchor='n', relx=0.8, rely=0.26)
clbl.place(anchor='n', relx=0.162, rely=0.4)
course_field.place(anchor='n', relx=0.251, rely=0.5,
                   relheight=0.15, relwidth=0.4)
course_val.place(anchor='n', relx=0.251, rely=0.655,
                 relheight=0.10, relwidth=0.4)
checkb.place(anchor='n', relx=0.75, rely=0.55)
log_scroll.place(anchor='n', relx=0.976, rely=0.01, relheight=0.99)
log.place(anchor='n', relx=0.48, rely=0.028, relheight=0.94, relwidth=0.945)

# display the menu
gui.config(menu=menubar)
if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    gui.mainloop()
