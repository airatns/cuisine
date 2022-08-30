from rest_framework import mixins, status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action


from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

from .models import User, Subscribe
from .mixins import ListCreateDeleteViewSet
from .serializers import UserListSerializer, UserRegistrSerializer, SubscribeSerializer


class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserRegistrSerializer

    def post(self, request):
        """Функция по созданию нового пользователя.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Функция по выводу на экран данных по всем пользователям.
        """
        user = User.objects.all()
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    """Вывод на экран данных о пользователе по id.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class SubscribeViewSet(viewsets.ModelViewSet):

    @action(detail=True,)
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            subscribe, 
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
