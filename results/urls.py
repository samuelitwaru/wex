from wex import router
from .views import *




router.register(r'assessments', AssessmentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'class-rooms', ClassRoomViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'grading-systems', GradingSystemViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'teacher-class-room-subjects', TeacherClassRoomSubjectViewSet)
router.register(r'assessments/(?P<assessment_id>\d+)/scores', ScoreViewSet, basename='scores')
# print(router.urls)

# router.urls += [
#     url(r'assessments/?P<pk>[^/.]+/scores', ScoreViewSet.as_view())
# ]