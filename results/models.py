from distutils import extension
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from utils import OverwiteStorageSystem, range_with_floats


LEVEL_CHOICES = [
    ("S.1", "S.1"),
    ("S.2", "S.2"),
    ("S.3", "S.3"),
    ("S.4", "S.4"),
    ("S.5", "S.5"),
    ("S.6", "S.6"),
]

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


def student_picture_upload_loacation(instance, filename):
    _, extension = filename.split('.')
    return f'students/pictures/{instance.id}.{extension}'

def teacher_picture_upload_loacation(instance, filename):
    _, extension = filename.split('.')
    return f'teachers/pictures/{instance.id}.{extension}'


class Period(models.Model):
    name = models.CharField(max_length=128)
    start = models.DateField()
    stop = models.DateField()

    def __str__(self):
        return self.name


# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=16, null=True)
    name = models.CharField(max_length=128)
    abbr = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"


class Paper(models.Model):
    number = models.IntegerField()
    description = models.CharField(max_length=128, null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('number', 'subject')
        ordering = ['subject']
        # order_with_respect_to = 'subject'

    def __str__(self):
        return f"{self.subject}/{self.number}"


class Level(models.Model):
    name = models.CharField(max_length=256)
    rank = models.IntegerField(unique=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    # subjects = models.ManyToManyField('Subject', related_name='levels', blank=True)
    papers = models.ManyToManyField('Paper', related_name='levels', blank=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=64)
    stream = models.CharField(max_length=64, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    # assessments = models.ManyToManyField('Assessment', related_name='class_rooms', blank=True)

    class Meta:
        unique_together = ('name', 'stream')
        ordering = ('level',)

    def __str__(self):
        return f"{self.name} {self.stream}"

    # def clean(self):
    #     # make sure that the level of assessments match the level of the class room
    #     if self.id:
    #         assessments = self.assessments.all()
    #         if assessments:
    #             for assessment in assessments:
    #                 if assessment.level != self.level:
    #                     raise ValidationError(f'Assessment "{assessment}" selected is of a different class room level.')


class Teacher(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to=teacher_picture_upload_loacation, storage=OverwiteStorageSystem, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    dob = models.DateField()
    picture = models.ImageField(upload_to=student_picture_upload_loacation, storage=OverwiteStorageSystem, null=True, blank=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Assessment(models.Model):
    date = models.DateField()
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True, default=Period.objects.first().id)

    def __str__(self):
        return f'{self.class_room} {self.paper}'



class Score(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)

    class Meta:
        unique_together = ('assessment', 'student')

    def __str__(self):
        return f"{self.student} {self.assessment} - {self.mark}"


class GradingSystem(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Grade(models.Model):
    category = models.CharField(max_length=64)
    min_mark = models.DecimalField(max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)
    max_mark = models.DecimalField(max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)
    points = models.IntegerField(null=True, blank=True)
    aggregates = models.IntegerField(null=True, blank=True)
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE, related_name='grades')

    class Meta:
        unique_together = ('grading_system', 'min_mark', 'max_mark', 'category')

    def __str__(self):
        return f"{self.category} ({self.min_mark} - {self.max_mark})"
    
    def clean(self):
        grades = self.grading_system.grades.exclude(id=self.id)
        for grade in grades:
            if grade.marks_intersect(self.min_mark, self.max_mark):
                raise ValidationError(f"Mark range {self.min_mark} - {self.max_mark} conflicts with mark range {grade.min_mark} - {grade.max_mark} of grade {grade}.")

        if not (self.points or self.aggregates):
            raise ValidationError("You must specify either points or aggregates")
        if self.min_mark >= self.max_mark:
            raise ValidationError("Max mark must be greater than min mark")

    def marks_intersect(self, min_mark, max_mark):
        return set(range_with_floats(self.min_mark, self.max_mark)).intersection(
            set(range_with_floats(min_mark, max_mark))
        )
        


class TeacherClassRoomPaper(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('teacher', 'class_room', 'paper')


# class TeacherSubjects(models.Model):
# 	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
# 	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


# class StudentSubjects(models.Model):
# 	student = models.ForeignKey(Student, on_delete=models.CASCADE)
# 	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


# class SubjectLevels(models.Model):
# 	level = models.ForeignKey(Level, on_delete=models.CASCADE)
# 	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


# def clean(self):
#         # pass
#         class_rooms = self.class_rooms.all()
#         # make sure class rooms selected belong to the same level
#         print(class_rooms)
#         if len(class_rooms) > 1:
#             levels = list(map(lambda class_room: class_room.level, class_rooms))
#             if levels.count(levels[0]) != len(levels):
#                 raise ValidationError("Class rooms must be from the same level")