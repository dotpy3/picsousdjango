from rest_framework.response import Response

from perm import models as perm_models
from perm import serializers as perm_serializers
from perm import viewsets


class PermViewSet(viewsets.RetrieveSingleInstanceModelViewSet):
    """
    Perm endpoint
    """
    queryset = perm_models.Perm.objects.all()
    serializer_class = perm_serializers.PermSerializer
    single_serializer_class = perm_serializers.PermWithArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article endpoint
    """
    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer


class UpdateArticleViewSet(viewsets.GenericViewSet):

    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer

    def update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        a = perm_models.Article.objects.get(pk=id)
        a.update_ventes()
        a.get_fresh()
        serializer = self.get_serializer(a)
        return Response(serializer.data)
