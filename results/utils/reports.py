from results import models


def wrap_aggr(aggr):
    if aggr <= 2:
        return f'D{aggr}'
    elif aggr <= 6:
        return f'C{aggr}'
    elif aggr <= 8:
        return f'P{aggr}'
    elif aggr == 9:
        return f'F{aggr}'


def compute_subject_grade(aggregates=[8, 8, 3]):
    '''computes the letter grade for a subject i.e A,B,C,D,E,O and F using the provided aggregates e.g [8,8,3]'''
    n = len(aggregates)
    if n:
        # get worst
        worst = max(aggregates)
        # get how may times worst appears
        n_worst = aggregates.count(worst)

        if n > 2:
            if worst <= 3:
                if n_worst == 1: return "A"
                else: return "B"
            elif worst <= 4:
                if n_worst == 1: return "B"
                else: return "C"
            elif worst <= 5:
                if n_worst == 1: return "C"
                else: return "D"
            elif worst <= 6:
                if n_worst == 1: return "D"
                else: return "E"
            elif worst <= 7:
                if n_worst == 1: return "E"
                else: return "O"
            elif worst <= 8:
                if n_worst == 1:
                    other = aggregates.copy()
                    other.remove(worst)
                    if max(other) <= 6: return "E"
                return "O"
            elif worst <= 9:
                if n_worst == 1:
                    return "O"
                elif n_worst == 2:
                    other = aggregates.copy()
                    other.remove(worst)
                    other.remove(worst)
                    other = other[0]
                    # and not sci subj
                    if other <= 7:
                        return "O"
                return "F"
        elif n > 1:
            if worst <= 2: return "A"
            elif worst <= 3: return "B"
            elif worst <= 4: return "C"
            elif worst <= 5: return "D"
            elif worst <= 6: return "E"
            elif (worst == 7 or worst == 8) and sum(aggregates) <= 12:
                return "E"
            elif (worst == 7 or worst == 8) and sum(aggregates) <= 16:
                return "O"
            elif worst == 9 and sum(aggregates) <= 16:
                return "O"
    return "F"


def compute_student_report(student, grading_system, period):
    '''
    - generates a computed report object for the specified student, using the specified grading system, in the specified period
    - returns a model report object and a computed report object i.e (report, computed_report)
    '''
    report, created = models.Report.objects.get_or_create(period=period,
                                                          student=student)
    computed_report = ComputedReport(student, report, [])
    subjects = models.Subject.objects.filter(
        is_selectable=False,
        level_group=student.class_room.level.level_group).union(
            student.subjects.all())
    for subject in subjects:
        custom_grading_system = models.CustomGradingSystem.objects.filter(
            class_room=student.class_room, subject=subject).first()
        if custom_grading_system:
            grading_system = custom_grading_system.grading_system
        subject_report = SubjectReport(grading_system, subject, [], [])
        papers = subject.papers.all()
        papers = student.class_room.level.papers.filter(subject=subject)
        allocation = models.PaperAllocation.objects.filter(
            paper=papers.first(), class_room=student.class_room).first()

        if allocation: subject_report.teacher = allocation.teacher
        else: subject_report.teacher = None
        if len(papers) == 0:
            continue
        for paper in papers:
            assessment_ids = [
                assessment.id
                for assessment in models.Assessment.objects.filter(
                    paper=paper, period=period, class_room=student.class_room)
            ]
            scores = [
                score.mark for score in models.Score.objects.filter(
                    assessment__in=assessment_ids, student=student)
            ]
            paper_report = PaperReport(grading_system, paper, scores)
            subject_report.papers.append(paper_report)

        activities = [
            activity for activity in models.Activity.objects.filter(
                class_room=student.class_room, subject=subject, period=period)
        ]
        scores = models.ActivityScore.objects.filter(
            student=student, activity__in=[act.id for act in activities])
        subject_report.activity_scores = scores
        subject_report.scores_string = ', '.join([f'{score.mark}' for score in scores])
        print(subject_report.scores_string)
        for activity in activities:
            # scores = [score.mark for score in activity.activityscore_set.filter(student=student).all()]
            score = models.ActivityScore.objects.filter(
                activity=activity, student=student).first()
            if score: mark = score.mark
            else: mark = 0
            activity_report = ActivityReport(activity, mark)
            subject_report.activities.append(activity_report)
        subject_report.set_values()
        computed_report.add_subject_report(subject_report)
    computed_report.set_values()
    report.points = computed_report.points
    report.aggregates = computed_report.aggregates
    report.competency_score = computed_report.average_scores
    report.save()
    return report, computed_report


class ComputedReport:
    '''
    A student report object having all information to be presented on the report

    Attributes:
        student         - model Student object
        report          - model Report object
        subject_reports - list of SubjectReport objects
        points          - total computed points for all subjects
        aggregates      - total computed aggregates for all subjects
        average         - computed average for all subjects
    '''
    subject_reports = []
    points = 0
    aggregates = 0
    average = 0

    def __init__(self, student, report, subject_reports=[]):
        self.student = student
        self.report = report
        self.subject_reports = subject_reports

    def add_subject_report(self, subject_report):
        self.subject_reports.append(subject_report)

    def __set_points(self):
        self.points = sum([subj.points for subj in self.subject_reports])

    def __set_aggregates(self):
        compulsories = []
        optionals = []
        for subj in self.subject_reports:
            if subj.subject.is_selectable: optionals.append(subj.aggregate)
            else: compulsories.append(subj.aggregate)
        compulsories.sort()
        optionals.sort()
        if len(optionals) and len(optionals) >= 2:
            compulsories.extend(optionals[:2])
        else:
            compulsories.extend(optionals)
        if len(compulsories) >= 8:
            self.aggregates = sum(compulsories[:8])
        else:
            self.aggregates = sum(compulsories)

    def __set_average(self):
        self.average = sum([subj.average for subj in self.subject_reports
                            ]) / len(self.subject_reports)

    def __set_total_scores(self):
        self.total_scores = sum(
            [subj.activity_score for subj in self.subject_reports])

    def __set_average_scores(self):
        self.average_scores = round(
            self.total_scores / len(self.subject_reports), 2)

    def set_values(self):
        self.__set_average()
        self.__set_aggregates()
        self.__set_points()
        self.__set_total_scores()
        self.__set_average_scores()


class SubjectReport:
    subject = None
    papers = []
    activities = []
    skills = ''
    remarks = ''
    activity_scores = []
    # scores = []

    def __init__(self, grading_system, subject=None, papers=[], activities=[]):
        self.grading_system = grading_system
        self.subject = subject
        self.papers = papers
        self.activities = activities

    def __set_average(self):
        try:
            self.average = round(
                sum([paper.average
                     for paper in self.papers]) / len(self.papers), 2)
        except ZeroDivisionError:
            self.average = 0

    def __set_aggregate(self):
        self.aggregate = self.grading_system.grade(self.average)

    def __set_letter_grade(self):
        self.letter_grade = compute_subject_grade([
            self.grading_system.grade(paper.average) for paper in self.papers
        ])

    def __set_points(self):
        mapper = {
            "A": 6,
            "B": 5,
            "C": 4,
            "D": 3,
            "E": 2,
            "O": 1,
            "F": 0,
        }
        if self.subject.is_subsidiary:
            mapper = {
                "A": 1,
                "B": 1,
                "C": 1,
                "D": 1,
                "E": 1,
                "O": 1,
                "F": 0,
            }
        self.points = mapper[self.letter_grade]

    def __set_subject_teacher_initals(self):
        if isinstance(self.teacher, models.Teacher):
            self.subject_teacher_initials = self.teacher.initials
        else:
            self.subject_teacher_initials = ''

    def __set_activity_total_scores(self):
        self.activity_total_scores = sum(
            [score.mark for score in self.activity_scores])
        
    def __set_activity_scores(self):
        self.scores = [score.mark for score in self.activity_scores]

    def __set_activity_average_score(self):
        try:
            self.activity_average_score = round(
                self.activity_total_scores / len(self.activity_scores),
                2
                )
        except ZeroDivisionError:
            self.activity_average_score = 0

    def __set_activity_score(self):
        self.activity_score = round(self.activity_average_score / 10 * 3, 1)

    def __set_activity_score_identifier(self):
        if self.activity_score >= 0.9 and self.activity_score <= 1.49:
            self.activity_score_identifier = "Basic"
        elif self.activity_score >= 1.5 and self.activity_score <= 2.49:
            self.activity_score_identifier = "Moderate"
        elif self.activity_score >= 2.5 and self.activity_score <= 3:
            self.activity_score_identifier = "Outstanding"
        else:
            self.activity_score_identifier = ''

    def set_values(self):
        self.__set_average()
        self.__set_aggregate()
        self.__set_letter_grade()
        self.__set_points()
        self.__set_subject_teacher_initals()
        self.__set_activity_scores()
        self.__set_activity_total_scores()
        self.__set_activity_average_score()
        self.__set_activity_score()
        self.__set_activity_score_identifier()


class PaperReport:
    paper = None
    scores = []

    def __init__(self, grading_system, paper, scores):
        self.grading_system = grading_system
        self.paper = paper
        self.description = paper.description
        self.scores = scores
        self.total = self.__compute_total()
        self.average = self.__compute_average()
        self.score = self.__compute_score()
        self.descriptor = self.__compute_descriptor()
        self.aggregate = self.grading_system.grade(self.average)

    @property
    def scores_string(self):
        return str(self.scores).lstrip('[').rstrip(']')

    def __compute_aggregates(self):
        return [self.grading_system.grade(score) for score in self.scores]

    def __compute_total(self):
        return sum(self.scores)

    def __compute_average(self):
        try:
            return self.total / len(self.scores)
        except ZeroDivisionError:
            return 0

    def __compute_score(self):
        return round(self.average / 100 * 3, 1)

    def __compute_descriptor(self):
        if self.score >= 0.9 and self.score <= 1.49:
            return "Basic"
        elif self.score >= 1.5 and self.score <= 2.49:
            return "Moderate"
        elif self.score >= 2.5 and self.score <= 3:
            return "Outstanding"
        return ''


class ActivityReport:
    activity = None
    scores = []

    def __init__(self, activity, mark):
        self.activity = activity
        self.name = activity.name
        self.mark = mark
        self.score = self.__compute_score()
        self.descriptor = self.__compute_descriptor()

    def __compute_score(self):
        return round(self.mark / 10 * 3, 1)

    def __compute_descriptor(self):
        if self.score >= 0.9 and self.score <= 1.49:
            return "Basic"
        elif self.score >= 1.5 and self.score <= 2.49:
            return "Moderate"
        elif self.score >= 2.5 and self.score <= 3:
            return "Outstanding"
        return ''
