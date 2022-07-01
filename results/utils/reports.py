from results import models


def compute_subject_aggregates(scores=[60, 45, 79]):
    grading_system = models.GradingSystem.objects.first()
    aggregates = []
    for mark in scores:
        aggregates.append(grading_system.grade(mark))
    return aggregates

def compute_subject_grade(aggregates=[8,8,3]):
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
        else:
            if worst <= 2: return "A"
            elif worst <= 3: return "B"
            elif worst <= 4: return "C"
            elif worst <= 5: return "D"
            elif worst <= 6: return "E"
            elif( worst == 7 or worst == 8) and sum(aggregates) <= 12: return "E"
            elif( worst == 7 or worst == 8) and sum(aggregates) <= 16: return "O"
            elif worst==9 and sum(aggregates) <= 16: return "O"
    return "F"
        

def compute_student_report(student, grading_system, period):
    report, created = models.Report.objects.get_or_create(period=period, student=student)
    computed_report = ComputedReport(report, [])
    subjects = models.Subject.objects.filter(is_selectable=False, level_group=student.class_room.level.level_group).union(student.subjects.all())
    for subject in subjects:
        subject_report = SubjectReport(grading_system, subject, [], [])
        papers = subject.papers.all()
        for paper in papers:
            assessment_ids = [assessment.id for assessment in models.Assessment.objects.filter(paper=paper, period=period, class_room=student.class_room)]
            scores = [score.mark for score in models.Score.objects.filter(assessment__in=assessment_ids, student=student)]
            paper_report = PaperReport(grading_system, paper, scores)
            subject_report.papers.append(paper_report)

        activities = [activity for activity in models.Activity.objects.filter(class_room=student.class_room, subject=subject, period=period)]
        for activity in activities:
            score = models.ActivityScore.objects.filter(activity=activity, student=student).first()
            if score: mark = score.mark
            else: mark = 0
            activity_report = ActivityReport(activity, mark)
            subject_report.activities.append(activity_report)
        subject_report.set_values()
        computed_report.add_subject_report(subject_report)
    computed_report.set_values()
    report.points = computed_report.points
    report.aggregates = computed_report.aggregates
    report.save()
    return report, computed_report



class ComputedReport:
    subject_reports = []
    points = 0
    aggregates = 0
    average = 0
    
    def __init__(self, report, subject_reports=[]):
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
        self.average = sum([subj.average for subj in self.subject_reports])/len(self.subject_reports)
    
    def set_values(self):
        self.__set_average()
        self.__set_aggregates()
        self.__set_points()


class SubjectReport:
    subject = None
    papers = []
    activities = []
    def __init__(self, grading_system, subject=None, papers=[], activities=[]):
        self.grading_system = grading_system
        self.subject = subject
        self.papers = papers
        self.activities = activities

    def __set_average(self):
        try:
            self.average = sum([paper.average for paper in self.papers])/len(self.papers)
        except ZeroDivisionError:
            self.average = 0
    def __set_aggregate(self):
        self.aggregate = self.grading_system.grade(self.average)
    def __set_letter_grade(self):
        self.letter_grade = compute_subject_grade(
            [self.grading_system.grade(paper.average) for paper in self.papers]
            )
    def __set_points(self):
        mapper = {"A":6,"B":5,"C":4,"D":3,"E":2,"O":1,"F":0,}
        if self.subject.is_subsidiary:
            mapper = {"A":1,"B":1,"C":1,"D":1,"E":1,"O":1,"F":0,}
        self.points = mapper[self.letter_grade]
    def set_values(self):
        self.__set_average()
        self.__set_aggregate()
        self.__set_letter_grade()
        self.__set_points()
    

class PaperReport:
    paper = None
    scores = []
    def __init__(self, grading_system, paper, scores):
        self.grading_system = grading_system
        self.paper = paper
        self.scores = scores
        self.total = self.__compute_total()
        self.average = self.__compute_average()
        self.score = self.__compute_score()
        self.descriptor = self.__compute_descriptor()
    def __compute_aggregates(self):
        return [self.grading_system.grade(score) for score in self.scores]
    def __compute_total(self):
        return sum(self.scores)
    def __compute_average(self):
        try:
            return self.total/len(self.scores)
        except ZeroDivisionError:
            return 0
    def __compute_score(self):
        return round(self.average/100*3, 1)
    def __compute_descriptor(self):
        if self.score >= 0.9 and self.score <= 1.49:
            return "Basic"
        elif self.score >= 1.5 and self.score <= 2.49:
            return "Moderate"
        elif self.score >= 2.5 and self.score <= 3:
            return "Outstanding"


class ActivityReport:
    paper = None
    scores = []
    def __init__(self, activity, mark):
        self.activity = activity
        self.mark = mark
        self.score = self.__compute_score()
        self.descriptor = self.__compute_descriptor()
    def __compute_score(self):
        return round(self.mark/10*3, 1)
    def __compute_descriptor(self):
        if self.score >= 0.9 and self.score <= 1.49:
            return "Basic"
        elif self.score >= 1.5 and self.score <= 2.49:
            return "Moderate"
        elif self.score >= 2.5 and self.score <= 3:
            return "Outstanding"
    

