from results import models
from .reports import *


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
        "generalRescores": True,
        "aggregates": True,
        "points": True,
        "classTeacher": True,
    }
}

LEVELS = {
    'P': [
        {'rank': 1, 'name':'Primary 1'},
        {'rank': 2, 'name':'Primary 2'},
        {'rank': 3, 'name':'Primary 3'},
        {'rank': 4, 'name':'Primary 4'},
        {'rank': 5, 'name':'Primary 5'},
        {'rank': 6, 'name':'Primary 6'},
        {'rank': 7, 'name':'Primary 7'},
    ],
    'O': [
        {'rank': 8, 'name':'Senior 1'},
        {'rank': 9, 'name':'Senior 2'},
        {'rank': 10, 'name':'Senior 3'},
        {'rank': 11, 'name':'Senior 4'},
    ],
    'A': [
        {'rank': 12, 'name':'Senior 5'},
        {'rank': 13, 'name':'Senior 6'},
    ],
}

LEVEL_GROUPS = {
    'P': 'Primary',
    'O': 'Ordinary',
    'A': 'Advanced',
}

SUBJECTS = [
    {'code':'P510', 'name':'Physics', 'abbr':'PHY', 'field':'Science', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P525', 'name':'Chemistry', 'abbr':'CHE', 'field':'Science', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P530', 'name':'Biology', 'abbr':'BIO', 'field':'Science', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P425', 'name':'Mathematics', 'abbr':'MTC', 'field':'Science', 'no_papers':2, 'level_group': 'A', 'is_selectable': True},
    {'code':'P250', 'name':'Geography', 'abbr':'GEO', 'field':'Arts', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P210', 'name':'History', 'abbr':'HIS', 'field':'Arts', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P245', 'name':'Divinity', 'abbr':'DIV', 'field':'Arts', 'no_papers':3, 'level_group': 'A', 'is_selectable': True},
    {'code':'P220', 'name':'Economics', 'abbr':'ECO', 'field':'Arts', 'no_papers':2, 'level_group': 'A', 'is_selectable': True},
    {'code':'S850', 'name':'Sub ICT', 'abbr':'ICT', 'field':'Science', 'no_papers':2, 'level_group': 'A', "is_subsidiary": True, 'is_selectable': True},
    {'code':'S475', 'name':'Sub Math', 'abbr':'ICT', 'field':'Science', 'no_papers':2, 'level_group': 'A', "is_subsidiary": True, 'is_selectable': True},
    {'code':'S101', 'name':'General Paper', 'abbr':'GP', 'field':'Science', 'no_papers':1, 'level_group': 'A', "is_subsidiary": True},
    
    {'code':'535', 'name':'Physics', 'abbr':'PHY', 'field':'Science', 'no_papers':2, 'level_group': 'O'},
    {'code':'545', 'name':'Chemistry', 'abbr':'CHE', 'field':'Science', 'no_papers':2, 'level_group': 'O'},
    {'code':'553', 'name':'Biology', 'abbr':'BIO', 'field':'Science', 'no_papers':2, 'level_group': 'O'},
    {'code':'456', 'name':'Mathematics', 'abbr':'MTC', 'field':'Science', 'no_papers':2, 'level_group': 'O'},
    {'code':'273', 'name':'Geography', 'abbr':'GEO', 'field':'Arts', 'no_papers':2, 'level_group': 'O'},
    {'code':'241', 'name':'History', 'abbr':'HIS', 'field':'Arts', 'no_papers':2, 'level_group': 'O'},
    {'code':'112', 'name':'English', 'abbr':'ENG', 'field':'Arts', 'no_papers':2, 'level_group': 'O'},
    {'code':'123', 'name':'Computer Studies', 'abbr':'CS', 'field':'Science', 'no_papers':2, 'level_group': 'O', 'is_selectable': True},
    {'code':'645', 'name':'Music', 'abbr':'MUS', 'field':'Arts', 'no_papers':3, 'level_group': 'O', 'is_selectable': True},
    {'code':'789', 'name':'French', 'abbr':'FRE', 'field':'Arts', 'no_papers':2, 'level_group': 'O', 'is_selectable': True},
]