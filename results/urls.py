from wex import router
from .views import *
from rest_framework.authtoken import views


router.register(r'users', UserViewSet)
router.register(r'user-prefs', UserPrefViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'papers', PaperViewSet)
router.register(r'class-rooms', ClassRoomViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'level-groups', LevelGroupViewSet)
router.register(r'grading-systems', GradingSystemViewSet)
# router.register(r'grades', GradeViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'teacher-class-room-papers', TeacherClassRoomPaperViewSet)
router.register(r'assessments/(?P<assessment_id>\d+)/scores', ScoreViewSet, basename='scores')
