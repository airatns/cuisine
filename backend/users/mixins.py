from rest_framework import mixins, viewsets


<<<<<<< HEAD
class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
=======
class ListCreateDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
>>>>>>> f99d897ed80fb1a723404e87fe907df84773456e
