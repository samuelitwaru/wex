DEFAULT_USER_PREFS = {
    "report_columns": {
        "code": True,
        "subject": True,
        "competency": True,
        "assessments": True,
        "total": True,
        "average": True,
        "score": True,
        "descriptor": True,
        "generalSkills": True,
        "generalRemarks": True,
        "aggregates": True,
        "points": True,
        "classTeacher": True,
    }
}

def grade(grade_tuple=(8,8,3)):
    # get worst
    worst = max(grade_tuple)
    # get how may times worst appears
    n_worst = grade_tuple.count(worst)
    