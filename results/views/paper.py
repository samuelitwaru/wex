from rest_framework import viewsets
from ..models import Paper, PaperAllocation
from ..serializers import PaperSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        count = self.queryset.count()
        return Response({'count':count})


@api_view(['GET'])
def get_teacher_allocated_papers(request, teacher_pk):
    class_room_paper_ids = [class_room_paper.paper_id for class_room_paper in PaperAllocation.objects.filter(teacher=teacher_pk)]
    queryset = Paper.objects.filter(id__in=class_room_paper_ids)
    params = request.GET
    if params:
        queryset = queryset.filter(**params.dict())
    serializer = PaperSerializer(queryset.all(), many=True)
    return Response(serializer.data)
