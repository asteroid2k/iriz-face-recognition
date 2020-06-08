import mongoengine as mongo
import datetime

def global_init():
    mongo.connect('iriz')


class TutorInfo(mongo.Document):
    meta = {'collection': 'tutor_infos'}

    name = mongo.StringField()
    ID = mongo.StringField(unique=True, db_field='tutor_id')
    pin = mongo.StringField()
    courses = mongo.ListField()


class Course(mongo.Document):
    meta = {'collection': 'courses'}

    name = mongo.StringField()
    code = mongo.StringField(unique=True)
    tutor_id = mongo.StringField()
    student_list = mongo.StringField()
    description = mongo.StringField()
    credits = mongo.FloatField()


class AttendanceData(mongo.Document):
    meta = {'collection': 'attendance_infos'}

    course_name = mongo.StringField()
    course_code = mongo.StringField(unique=True)
    data_file = mongo.StringField()
    pop = mongo.FloatField()
    cumm_total = mongo.FloatField()
    num_days = mongo.FloatField()
    day_data = mongo.DictField()
    month_data = mongo.DictField()
    course = mongo.ReferenceField(Course)


class LiveData(mongo.Document):
    meta = {'collection': 'student_logs'}
    ccode = mongo.StringField()
    log = mongo.ListField(default=[])
    isLive = mongo.BooleanField()
    started_at = mongo.DateTimeField(default=datetime.datetime.utcnow)
