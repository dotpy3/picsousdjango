from rest_framework.response import Response
from rest_framework.viewsets import *


class RetrieveSingleInstanceModelViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.single_serializer_class(instance)
        return Response(serializer.data)
