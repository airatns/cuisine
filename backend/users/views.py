from rest_framework import mixins, status, viewsets, generics
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserListSerializer, UserRegistrSerializer


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
