from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Period)
admin.site.register(Level)
admin.site.register(LevelGroup)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Paper)
admin.site.register(Student)
admin.site.register(Assessment)
admin.site.register(Score)
admin.site.register(GradingSystem)
admin.site.register(Report)
admin.site.register(TeacherClassRoomPaper)
admin.site.register(UserPref)