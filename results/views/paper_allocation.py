from rest_framework import viewsets
from ..models import PaperAllocation
from ..serializers import PaperAllocationSerializer
from ..filters import PaperAllocationFilter
from django_filters import rest_framework as filters

class PaperAllocationViewSet(viewsets.ModelViewSet):
    queryset = PaperAllocation.objects.all()
    serializer_class = PaperAllocationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PaperAllocationFilter

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        f = PaperAllocationFilter(self.request.GET, queryset=queryset)
        queryset = f.queryset
        # params = self.request.query_params
        # if params:
        #     queryset = queryset.filter(**params.dict())
        return queryset