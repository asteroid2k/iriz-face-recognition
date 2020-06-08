import os
import logcsv
import pandas as pd

# base path
BASE = os.path.join('C:\\', 'xampp', 'htdocs',
                    'project', 'iriz_backend', 'public')

attfile = os.path.join(BASE, 'AttendanceData', 'CPEN406_attendance.csv')

df = pd.read_csv(attfile)
logcsv.add_day("12/04/2020", df)
logcsv.add_record("10628439", "12/04/2020", df)
logcsv.add_record("10656987", "12/04/2020", df)
logcsv.add_record("11258874", "12/04/2020", df)
logcsv.add_record("10223322", "12/04/2020", df)
logcsv.add_day("15/04/2020", df)
logcsv.add_record("10628439", "15/04/2020", df)
logcsv.add_record("10656987", "15/04/2020", df)
logcsv.add_record("11258874", "15/04/2020", df)
logcsv.add_record("10223322", "15/04/2020", df)
logcsv.add_day("20/04/2020", df)
logcsv.add_record("10628439", "20/04/2020", df)
logcsv.add_record("10656987", "20/04/2020", df)
logcsv.add_record("11258874", "20/04/2020", df)
logcsv.add_record("10223322", "20/04/2020", df)
logcsv.add_day("23/04/2020", df)
logcsv.add_record("10628439", "23/04/2020", df)
logcsv.add_record("10215588", "23/04/2020", df)
logcsv.add_record("10656987", "23/04/2020", df)
logcsv.add_record("10236587", "23/04/2020", df)
logcsv.add_record("10656987", "23/04/2020", df)
logcsv.add_record("11258874", "23/04/2020", df)
logcsv.add_record("10223322", "23/04/2020", df)
df = logcsv.calc_total(df)
df.to_csv(attfile, index=False)
r, c = df.shape
print(len(df.columns) - 2)
