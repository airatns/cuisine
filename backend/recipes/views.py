from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredients, Tags
from .serializers import IngredientsSerializer, TagsSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
