from wex import router
from .views import *
from rest_framework.authtoken import views
from rest_framework_nested import routers
from django.urls import path, include
# from django.conf.urls import url



router.register(r'user-prefs', UserPrefViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'assessment-categories', AssessmentCategoryViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'papers', PaperViewSet)
router.register(r'class-rooms', ClassRoomViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'level-groups', LevelGroupViewSet)
router.register(r'grading-systems', GradingSystemViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'activity-scores', ActivityScoreViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'custom-grading-systems', CustomGradingSystemViewSet)
router.register(r'paper-allocations', PaperAllocationViewSet)

nested_teachers_router = routers.NestedSimpleRouter(router, r'teachers', lookup='teacher')
nested_teachers_router.register(r'assessments', AssessmentViewSet, basename='teacher-assessments')
nested_teachers_router.register(r'class-rooms', ClassRoomViewSet, basename='teacher-class-rooms')

nested_assessments_router = routers.NestedSimpleRouter(router, r'assessments', lookup='assessment')
nested_assessments_router.register(r'scores', ScoreViewSet, basename='assessment-scores')
nested_assessments_router.register(r'scores/download', ScoreViewSet, basename='assessment-scores-download')

nested_activities_router = routers.NestedSimpleRouter(router, r'activities', lookup='activity')
nested_activities_router.register(r'scores', ActivityScoreViewSet, basename='activity-scores')
nested_activities_router.register(r'scores/download', ActivityScoreViewSet, basename='activity-scores-download')

nested_levels_router = routers.NestedSimpleRouter(router, r'levels', lookup='level')
nested_levels_router.register(r'class-rooms', ClassRoomViewSet, basename='level-class-rooms')
# nested_levels_router.register(r'subjects', SubjectViewSet, basename='level-subjects')

nested_level_groups_router = routers.NestedSimpleRouter(router, r'level-groups', lookup='level_group')
nested_level_groups_router.register(r'subjects', SubjectViewSet, basename='level-group-subjects')

nested_class_rooms_router = routers.NestedSimpleRouter(router, r'class-rooms', lookup='class_room')
nested_class_rooms_router.register(r'students', StudentViewSet, basename='class-room-students')
nested_class_rooms_router.register(r'promotions', ReportViewSet, basename='class-room-promotions')


nested_url_patterns = [
    path('api/', include(nested_teachers_router.urls)),
    path('api/', include(nested_assessments_router.urls)),
    path('api/', include(nested_activities_router.urls)),
    path('api/', include(nested_levels_router.urls)),
    path('api/', include(nested_class_rooms_router.urls)),
    path('api/', include(nested_level_groups_router.urls)),
    path(r'api/teachers/<int:teacher_pk>/allocated-class-rooms/', get_teacher_allocated_class_rooms),
    path(r'api/teachers/<int:teacher_pk>/allocated-class-rooms/<int:class_room_pk>/', get_teacher_allocated_class_room),
    path(r'api/teachers/<int:teacher_pk>/allocated-papers/', get_teacher_allocated_papers),
    path(r'api/teachers/<int:teacher_pk>/subjects/', get_teacher_subjects),
    path(r'api/teachers/<int:teacher_pk>/allocated-class-rooms/<int:class_room_pk>/subjects/', get_teacher_allocated_class_room_subjects),

]