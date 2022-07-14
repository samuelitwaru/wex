from rest_framework import viewsets
from ..models import Promotion, Report
from ..serializers import PromotionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        class_room_pk = self.kwargs.get('class_room_pk')
        if class_room_pk:
            queryset = queryset.filter(current_class_room=class_room_pk)
        params = self.request.query_params
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count':count})

    @action(detail=False, methods=['POST'], name='add', url_path='add')
    def add(self, request, *args, **kwargs):
        data = request.data
        reports = data.get('reports')
        next_class_room = data.get('next_class_room')
        promotions = []
        if reports:
            students = [report.student for report in Report.objects.filter(id__in=reports).all()]
            promotions = []
            for stud in students:
                promotion, created= Promotion.objects.get_or_create(student=stud, current_class_room=stud.class_room, next_class_room_id=next_class_room) 
                promotions.append(promotion)
            print(promotions)
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'], name='approve', url_path='approve')
    def approve(self, request, *args, **kwargs):
        data = request.data
        promotions = data.get('promotions')
        queryset = Promotion.objects.filter(id__in=promotions)
        queryset.update(**{'status': 'APPROVED'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'], name='reject', url_path='reject')
    def reject(self, request, *args, **kwargs):
        data = request.data
        promotions = data.get('promotions')
        queryset = Promotion.objects.filter(id__in=promotions)
        queryset.update(**{'status': 'REJECTED'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)