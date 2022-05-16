from rest_framework import viewsets
from ..models import Entity
from ..serializers import EntitySerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

    @action(detail=True, methods=['POST'], name='upload_logo', url_path='logo/upload')
    def upload_logo(self, request, *args, **kwargs):
        logo = request.FILES['picture']
        print('>>>>>>>>>>', kwargs.get('pk'))
        entity = super().get_queryset().filter(id=kwargs.get('pk')).first()
        entity.logo = logo
        entity.save()
        serializer = self.get_serializer(entity)
        return Response(serializer.data)