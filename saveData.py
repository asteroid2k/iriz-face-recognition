import os
import mongohelper as myh
import mongoengine as mg
import pandas as pd

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')
# initialize MongoDb Connection
myh.global_init()
attfile = ''


def populate(adat, c):
    adat.course_code = c
    adat.data_file = attfile
    try:
        dataframe = pd.read_csv(attfile)
        print(dataframe)
    except FileNotFoundError:
        print('File Not Found')
    # PermissionError
    else:
        r, c = dataframe.shape
        adat.pop = len(dataframe.index) - 1
        adat.cumm_total = dataframe.iloc[r - 1, c - 1]
        adat.num_days = len(dataframe.columns) - 2
        adat.save()


def main(course=None):
    new = False
    if course is None:
        print('No course name')
    else:
        global attfile
        attfile = os.path.join(BASE, 'AttendanceData', course + '_attendance.csv')
    try:
        attdata = myh.AttendanceData.objects(course_code__iexact=course).get()
        print('YES')
    except mg.DoesNotExist:
        print('NO')
        new = True
    else:
        print('found')
        populate(attdata, course)

    if new:
        print('new')
        attdata = myh.AttendanceData()
        populate(attdata, course)

