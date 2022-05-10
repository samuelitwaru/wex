from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Level)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Assessment)
admin.site.register(Score)
admin.site.register(GradingSystem)
admin.site.register(Grade)
admin.site.register(TeacherClassRoomSubject)