from datetime import datetime
from email.policy import default
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.forms import JSONField
from core.models import Entity, TimeStampedModel
from core.utils import NATIONALITIES
from results.utils import DEFAULT_USER_PREFS, LEVELS, LEVEL_GROUPS
from django_resized import ResizedImageField
from django.db import transaction
from utils import OverwiteStorageSystem, range_with_floats

LEVEL_CHOICES = [
    ("S.1", "S.1"),
    ("S.2", "S.2"),
    ("S.3", "S.3"),
    ("S.4", "S.4"),
    ("S.5", "S.5"),
    ("S.6", "S.6"),
]

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

SUBJECT_FIELD_CHOICES = (
    ('Arts', 'Arts'),
    ('Science', 'Science'),
)

PROMOTION_STATUS_CHOICES = [
    ('PENDING', 'PENDING'),
    ('APPROVED', 'APPROVED'),
]

LEVEL_GROUP_CHOICES = tuple(LEVEL_GROUPS.items())

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
PERTENTH_VALIDATOR = [MinValueValidator(0), MaxValueValidator(10)]

P_RESULT_VALIDATOR = [MinValueValidator(4), MaxValueValidator(36)]
O_RESULT_VALIDATOR = [MinValueValidator(8), MaxValueValidator(72)]
A_RESULT_VALIDATOR = [MinValueValidator(1), MaxValueValidator(20)]


def student_picture_upload_location(instance, filename):
    _, extension = filename.split('.')
    return f'students/pictures/{instance.id}.{extension}'


def teacher_picture_upload_location(instance, filename):
    _, extension = filename.split('.')
    return f'teachers/pictures/{instance.id}.{extension}'


def period_default():
    try:
        return Period.objects.latest().id
    except Period.DoesNotExist:
        return None


def default_user_prefs():
    return DEFAULT_USER_PREFS


class Period(TimeStampedModel):
    name = models.CharField(max_length=128)
    start = models.DateField()
    stop = models.DateField()
    is_promotional = models.BooleanField(default=False)
    promotions_opened = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.name


# Create your models here.
class Subject(TimeStampedModel):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128)
    abbr = models.CharField(max_length=8, null=True, blank=True)
    created_from_system = models.BooleanField(default=True)
    is_subsidiary = models.BooleanField(null=True, blank=True)
    is_selectable = models.BooleanField(default=False)
    no_papers = models.IntegerField(default=1)
    field = models.CharField(max_length=16, choices=SUBJECT_FIELD_CHOICES)
    level_group = models.ForeignKey('LevelGroup', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} {self.name}"


class Paper(TimeStampedModel):
    number = models.IntegerField()
    description = models.CharField(max_length=128, null=True, blank=True)
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE,
                                related_name='papers')

    class Meta:
        unique_together = ('number', 'subject')
        ordering = ['subject']

    def __str__(self):
        return f"{self.subject}/{self.number}"


class LevelGroup(TimeStampedModel):
    name = models.CharField(max_length=128, choices=LEVEL_GROUP_CHOICES)
    full = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Level(TimeStampedModel):
    name = models.CharField(max_length=256)
    rank = models.IntegerField(unique=True)
    level_group = models.ForeignKey(LevelGroup, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject',
                                      related_name='levels',
                                      blank=True)
    papers = models.ManyToManyField('Paper', related_name='levels', blank=True)

    def __str__(self):
        return self.name


class ClassRoom(TimeStampedModel):
    name = models.CharField(max_length=64)
    stream = models.CharField(max_length=64, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'stream')
        ordering = ('level', )

    def __str__(self):
        return f"{self.name} {self.stream or ''}"


class Teacher(TimeStampedModel):
    name = models.CharField(max_length=256)
    initials = models.CharField(max_length=8)
    picture = ResizedImageField(upload_to=teacher_picture_upload_location,
                                storage=OverwiteStorageSystem,
                                null=True,
                                blank=True)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='teacher')

    def __str__(self):
        return self.name


class PaperAllocation(TimeStampedModel):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)

    class Meta:
        unique_together = ('teacher', 'class_room', 'paper')
        ordering = ['class_room__level']


class Student(TimeStampedModel):
    index_no = models.CharField(max_length=64, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(null=True)
    house = models.CharField(max_length=64, null=True, blank=True)
    nationality = models.CharField(max_length=128, choices=NATIONALITIES)
    picture = ResizedImageField(upload_to=student_picture_upload_location,
                                storage=OverwiteStorageSystem,
                                null=True,
                                blank=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject',
                                      related_name='students',
                                      blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['class_room__level']

    @property
    def age(self):
        print(self.dob)
        if self.dob:
            delta = datetime.now().year - self.dob.year
            return delta


class AssessmentCategory(TimeStampedModel):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Assessment(TimeStampedModel):
    date = models.DateField()
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    period = models.ForeignKey(Period,
                               on_delete=models.CASCADE,
                               default=period_default)
    is_open = models.BooleanField(default=True)
    assessment_category = models.ForeignKey(AssessmentCategory,
                                            on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ('paper', 'class_room', 'assessment_category')

    def __str__(self):
        return f'{self.class_room} {self.paper}'


class Activity(TimeStampedModel):
    name = models.CharField(max_length=64)
    skills = models.JSONField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    period = models.ForeignKey(Period,
                               on_delete=models.CASCADE,
                               default=period_default)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.class_room} {self.name}'


class ActivityScore(TimeStampedModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0, validators=PERTENTH_VALIDATOR)


class Score(TimeStampedModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0, validators=PERCENTAGE_VALIDATOR)

    class Meta:
        unique_together = ('assessment', 'student')

    def __str__(self):
        return f"{self.student} {self.assessment} - {self.mark}"


class GradingSystem(TimeStampedModel):
    name = models.CharField(max_length=128)
    D1 = models.IntegerField(default=100)
    D2 = models.IntegerField(default=89)
    C3 = models.IntegerField(default=79)
    C4 = models.IntegerField(default=69)
    C5 = models.IntegerField(default=59)
    C6 = models.IntegerField(default=54)
    P7 = models.IntegerField(default=49)
    P8 = models.IntegerField(default=39)
    F9 = models.IntegerField(default=29)
    level_group = models.ForeignKey('LevelGroup',
                                    on_delete=models.CASCADE,
                                    related_name='grading_systems')
    is_default = models.BooleanField(default=True)

    def __str__(self):
        if self.is_default: return f"{self.name} (default)"
        return self.name

    def grade(self, mark):
        if mark <= self.F9: return 9
        elif mark <= self.P8: return 8
        elif mark <= self.P7: return 7
        elif mark <= self.C6: return 6
        elif mark <= self.C5: return 5
        elif mark <= self.C4: return 4
        elif mark <= self.C3: return 3
        elif mark <= self.D2: return 2
        elif mark <= self.D1: return 1


class UserPref(models.Model):
    pref = models.JSONField(default=default_user_prefs)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Report(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    period = models.ForeignKey(Period,
                               on_delete=models.CASCADE,
                               default=period_default)
    class_teacher_comment = models.CharField(max_length=512, blank=True)
    head_teacher_comment = models.CharField(max_length=512, blank=True)
    competency_class_teacher_comment = models.CharField(max_length=512,
                                                        blank=True)
    competency_head_teacher_comment = models.CharField(max_length=512,
                                                       blank=True)
    computation = models.JSONField(null=True)
    aggregates = models.IntegerField(default=72, validators=O_RESULT_VALIDATOR)
    points = models.IntegerField(default=0, validators=A_RESULT_VALIDATOR)
    competency_score = models.FloatField(default=0,
                                         validators=PERTENTH_VALIDATOR)

    level = models.ForeignKey(Level,
                              on_delete=models.CASCADE,
                              related_name='reports')

    promo_from_class_room = models.ForeignKey(ClassRoom,
                                              on_delete=models.CASCADE,
                                              null=True,
                                              related_name='promotions_from')
    promo_to_class_room = models.ForeignKey(ClassRoom,
                                            on_delete=models.CASCADE,
                                            null=True,
                                            related_name='promotions_to')
    promo_comment = models.CharField(max_length=512, null=True, blank=True)
    promo_is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'period', 'level',
                           'promo_from_class_room', 'promo_to_class_room')
        ordering = ['level']

    def __str__(self):
        return f'{self.student} - {self.period}'


class CustomGradingSystem(TimeStampedModel):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_room', 'subject', 'grading_system')


# signals
from django.db.models.signals import post_save, post_delete


def create_student_report(sender, instance, **kwargs):
    if kwargs.get('created'):
        Report.objects.create(**{
            'student': instance,
            'level': instance.class_room.level
        })


def create_student_index_no(sender, instance, **kwargs):
    if not instance.index_no:
        instance.index_no = f'RES/{instance.created_at.year}/{str(instance.id).zfill(4)}'
        instance.save()


def create_subject_papers(sender, instance, **kwargs):
    if kwargs.get('created'):
        no_papers = instance.no_papers
        papers = []
        for n in range(0, no_papers):
            paper = Paper(
                **{
                    'number': n + 1,
                    'description': f'Paper {n+1}',
                    'subject': instance
                })
            paper.save()
            papers.append(paper)
        # papers = Paper.objects.bulk_create([Paper(**{'number': n+1, 'description':f'Paper {n+1}', 'subject':instance}) for n in range(0, no_papers)])
        for level in instance.level_group.level_set.all():
            level.papers.add(*papers)


def enforce_grading_system_one_default(sender, instance, **kwargs):
    defaults = GradingSystem.objects.filter(level_group=instance.level_group,
                                            is_default=True)
    if defaults.count() > 1:
        if not instance.is_default:
            print('making new default')  # make new default
            new_default = GradingSystem.objects.filter(
                level_group=instance.level_group).first()
            if new_default:
                new_default.is_default = True
                new_default.save()
        else:
            print('removing other defaults')  # remove other defaults
            with transaction.atomic():
                GradingSystem.objects.exclude(id=instance.id).filter(
                    is_default=True,
                    level_group=instance.level_group).update(is_default=False)
    elif defaults.count() < 1:
        print('making first default')
        new_default = GradingSystem.objects.filter(
            level_group=instance.level_group).first()
        if new_default:
            new_default.is_default = True
            new_default.save()


def create_paper_allocations(sender, instance, **kwargs):
    levels = instance.subject.level_group.level_set.all()
    for level in levels:
        class_rooms = level.classroom_set.all()
        for class_room in class_rooms:
            PaperAllocation.objects.get_or_create(paper=instance,
                                                  class_room=class_room)


def update_subject_no_papers(sender, instance, **kwargs):
    subject = instance.subject
    subject.no_papers = subject.papers.count()
    subject.save()


post_save.connect(create_paper_allocations, sender=Paper)
post_save.connect(create_student_report, sender=Student)
post_save.connect(create_student_index_no, sender=Student)
post_save.connect(create_subject_papers, sender=Subject)
post_save.connect(enforce_grading_system_one_default, sender=GradingSystem)
post_delete.connect(enforce_grading_system_one_default, sender=GradingSystem)
post_delete.connect(update_subject_no_papers, sender=Paper)
post_save.connect(update_subject_no_papers, sender=Paper)


# initializations
def setup_levels(choices={
    'P': True,
    'O': True,
    'A': True,
}):
    for k, levels in LEVELS.items():
        if len(levels) and choices[k]:
            lg = LevelGroup.objects.create(**{
                'name': k,
                'full': LEVEL_GROUPS[k]
            })
            for each in levels:
                each['level_group'] = lg
                Level.objects.create(**each)
