import os
import datetime
import pandas as pd
import time
import mongohelper as myh
import mongoengine as mg

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')

lp = os.path.join('C:\\', 'xampp', 'htdocs',
                  'project', 'iriz_backend', 'public', 'ZZ990434309id093404.txt')
plist = []
myh.global_init()
log_id = '5e84ed38533a0000ad000712'


def log_csv(ccode):
    # log path
    logpath = os.path.join('C:\\', 'xampp', 'htdocs',
                           'project', 'iriz_backend', 'public', ccode + 'studentlog.txt')
    course = ccode
    attfile = os.path.join(BASE, 'AttendanceData', course + '_attendance.csv')
    # Check if attendance file is available
    if os.path.exists(attfile) and os.path.isfile(attfile):
        # get attendance dataframe
        dataframe = pd.read_csv(attfile)

        date = datetime.datetime.now()
        date = f'{date.day}/{date.month}/{date.year}'

        # add day
        add_day(date, dataframe)
        with open(logpath) as logfile:
            for line in logfile:
                line = line.strip()
                if line and len(line) == 8:
                    if line not in plist:
                        print(f'logging {line}')
                        add_record(line, date, dataframe)
                        plist.append(line)
                        edit_livedata(course, line)

        calc_total(dataframe)
        sort_df(dataframe)
        dataframe.to_csv(attfile, index=False)


#  add isPresent record for student on day x


def add_record(id_field, date, df):
    if date in df.columns and len(id_field) == 8:
        df.loc[df['ID'].str.contains(id_field), date] = 1
    return df


# add new day for attendance to record


def add_day(date, df):
    if date not in df.columns:
        df.insert(df.shape[1] - 1, date, None, False)
    return df


# calculate daily totals and total attendance for each student


def calc_total(df):
    df.iloc[-1, 1:-1] = df.iloc[:-1, 1:-1].sum(axis=0)
    df['Ototal'] = df.iloc[:, 1:-1].sum(axis=1)
    return df


# Sort entries by ID


def sort_df(df):
    df.sort_values(by='ID', inplace=True)
    df.drop_duplicates(subset='ID', keep=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def bootlogger(course_code):
    # log path
    logpath = os.path.join('C:\\', 'xampp', 'htdocs',
                           'project', 'iriz_backend', 'public', course_code + 'studentlog.txt')
    if not os.path.exists(logpath) and not os.path.isfile(logpath):
        f = open(logpath, 'w')
        f.close()
    while True:
        print('Starting logger')
        log_csv(course_code)
        print('logger sleeping')
        time.sleep(5)


def edit_livedata(ccde, idx):
    new = False
    global log_id
    try:

        corz = myh.LiveData.objects(pk=log_id).get()

    except mg.DoesNotExist:
        print(f'Live data for ({ccde}) not found')
        new = True
    else:
        print('using existing live data')
        corz.isLive = True
        log = corz.log
        log.append(idx)
        corz.log = log
        corz.save()

    if new:
        log = []
        log.append(idx)
        print('creating new live data')
        corz = myh.LiveData()
        corz.ccode = ccde
        corz.isLive = True
        corz.log = log
        corz.save()
        log_id = corz.id
        with open(lp, 'w') as file:
            file.write(str(corz.id))


def end_livedata(ccde):
    _id = '5e84ed38533a0000ad000712'
    with open(lp, 'r') as file:
        _id = file.readline().strip()
    try:
        corz = myh.LiveData.objects(pk=_id).get()

    except mg.DoesNotExist:
        print(f'Live data for ({ccde}) not found.could not end')
        print('id', _id)
    else:
        print('ending existing live data')
        corz.isLive = False
        corz.save()
        open(lp, 'w').close()
