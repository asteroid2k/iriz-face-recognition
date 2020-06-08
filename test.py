# import mongoengine
# import mongohelper as myh
#
# mongoengine.connect('test')
# aa = myh.Course()
# aa.name = 'a course'
# aa.code = 'test111'
# aa.tutor_id = '1999999'
# aa.student_list = 'sdfda/sdfsdaf/ds'
# mybool = False
# try:
#     aa.save()
# except mongoengine.NotUniqueError:
#     print('already dey')
#     mybool = True
#
# if mybool:
#     aa = myh.Course.objects(code__iexact='test111').get()
#     aa.name = 'edited course'
#     aa.code = 'test999'
#     aa.tutor_id = '1999999'
#     aa.student_list = 'sdfda/sdfsdaf/ds'
#     aa.save()

