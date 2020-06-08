import math
import os
import mongohelper as myh
import mongoengine as mg
import pandas as pd
import time

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')
# initialize MongoDb Connection
myh.global_init()
attfile = ''


# parse and get compile unique student ids from student list


def get_class_list(course_code=None):
    course_list = parse_list(course_code)
    if course_list is None:
        return None
    else:
        course_list = list(dict.fromkeys(course_list))
        return course_list


# parse student list


def parse_list(course_code):
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


# add new student to records from student list


def add_newstudents_from_list(ccde, df):
    slist = get_class_list(ccde)
    r = df.shape[0]
    students = [a for a in df['ID'].values]
    newstu = [s for s in slist if s not in students]
    df.drop([r - 1], axis=0, inplace=True)
    for idn in newstu:
        df = df.append({'ID': str(idn)}, ignore_index=True)
    df = df.append({'ID': 'Dtotal'}, ignore_index=True)
    return df


# calculate daily totals and total attendance for each student


def calc_total(df):
    df.iloc[-1, 1:-1] = df.iloc[:-1, 1:-1].sum(axis=0)
    df['Ototal'] = df.iloc[:, 1:-1].sum(axis=1)
    return df


def sort_df(df):
    df.sort_values(by='ID', inplace=True)
    df.drop_duplicates(subset='ID', keep=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def populate(adat, cc):
    adat.course_code = cc
    adat.data_file = attfile
    try:
        dataframe = pd.read_csv(attfile)

    except FileNotFoundError:
        print('File Not Found')
        return f"{cc} Attendance file not found", False
    # PermissionError
    else:
        print('Performing Calculations and Sorting')
        calc_total(dataframe)
        sort_df(dataframe)
        dataframe.to_csv(attfile, index=False)
        print('Done..')
        # print(dataframe)
        r, c = dataframe.shape
        print('Saving to database')
        adat.pop = len(dataframe.index) - 1
        adat.cumm_total = dataframe.iloc[r - 1, c - 1]
        adat.num_days = len(dataframe.columns) - 2
        adat.day_data = extract_day_totals(dataframe)
        adat.month_data = extract_month_totals(dataframe)
        adat.save()
        print('DONE..')
        return f"Successfully Updated Database Records for {cc}", True


def update_db(course=None):
    new = False
    if course is None:
        print('[FAILED:SaveData]  No course name')
        return '[FAILED:SaveData]  No course name', False
    else:
        global attfile
        attfile = os.path.join(BASE, 'AttendanceData', course + '_attendance.csv')
        if not os.path.exists(attfile) or not os.path.isfile(attfile):
            print('file not found')
            return f'Attendance File not found', False

    try:
        try:
            corz = myh.Course.objects(code__iexact=course).get()
        except mg.DoesNotExist:
            print(f'Course({course}) not found')
            return f'Course({course}) not found', False

        attdata = myh.AttendanceData.objects(course_code__iexact=course).get()
        print('Fetching records from Database')
    except mg.DoesNotExist:
        print('Records not Found in Database')
        new = True
    else:
        print('Using existing records')
        res = populate(attdata, course)
        return res

    if new:
        print('Creating New Records in Database')
        attdata = myh.AttendanceData()
        res = populate(attdata, course)
        return res


def update_list(course):
    atfl = os.path.join(BASE, 'AttendanceData', course + '_attendance.csv')
    if os.path.exists(atfl) and os.path.isfile(atfl):
        df = pd.read_csv(atfl)
        df = add_newstudents_from_list(course, df)
        calc_total(df)
        sort_df(df)
        df.to_csv(atfl, index=False)
        update_db(course)
        print('Attendance File Updated Successfully')
        return f'Attendance File for {course} Updated Successfully', True
    else:
        print('No attendance file')
        return f'Attendance File not found', False


def extract_day_totals(df):
    r, c = df.shape
    df = df.drop(columns=['ID', 'Ototal'])
    df = df.fillna(0)
    days = [x for x in df.columns]
    print(days)
    tots = df.iloc[-1, :].values
    tots = [tot for tot in tots]
    print(tots)
    info = {d: v for d, v in zip(days, tots)}
    return info


def extract_month_totals(df):
    df = df.fillna(0)
    df = df.drop(columns=['ID', 'Ototal'])
    cols = [x for x in df.columns]
    old = []
    info = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
    for x in cols:
        for i in range(1, 13):
            if x in old:
                continue
            dd, mm, yy = x.split('/')
            if int(mm) == i:
                info[str(i)] += df.loc[:, x].values[-1]
                old.append(x)

    info = {k: v for k, v in info.items() if v != 0.0}
    return info
