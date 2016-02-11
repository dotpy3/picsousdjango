from rest_framework import viewsets
from rest_framework.response import Response


class RetrieveSingleInstanceModelViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.single_serializer_class(instance)
        return Response(serializer.data)
