from django.shortcuts import get_object_or_404
from recipes.pagination import RecipePagination
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import (SubscribeSerializer, UserDetailSerializer,
                          UserListSerializer, UserRegistrSerializer)


class UserListCreate(generics.ListCreateAPIView, PageNumberPagination):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def post(self, request):
        """Функция по созданию нового пользователя.
        """
        serializer = UserRegistrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Функция по выводу на экран данных по всем пользователям.
        """
        users = User.objects.all()
        results = self.paginate_queryset(users,)
        serializer = UserListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data,)


class UserDetail(generics.RetrieveAPIView):
    """Вывод на экран данных о пользователе по id.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


# class MeDetail(generics.RetrieveAPIView):
#     """Вывод на экран данных о текущем Пользователе.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request):
#        current_user = (
#            get_object_or_404(User, username=request.user.username)
#         serializer = UserListSerializer(current_user,)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class MeDetail(viewsets.ModelViewSet):
    """Вывод на экран данных о текущем Пользователе.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@action(detail=False, url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,),)
def subscribe(request, author_id):
    """Метод по созданию и удалению Подписки на автора.
    """
    user = request.user
    if user.is_anonymous:
        return Response({
            'message': 'Пожалуйста, войдите в Вашу учетную систему',
        }, status=status.HTTP_401_UNAUTHORIZED)

    author = get_object_or_404(User, pk=author_id)
    if request.method == 'POST':
        if user == author:
            return Response({
                'message': 'На себя подписаться нельзя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({
                'message': 'Вы уже подписаны на этого автора'
            }, status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            subscription, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        subscription = Subscription.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response({
                'message': 'Вы отписались от данного автора',
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'message': 'Вы не подписывались на данного автора'},
            status=status.HTTP_400_BAD_REQUEST
        )


class Subscriptions(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = RecipePagination

    def get(self, request):
        """Метод по выводу всех Подписок на автора текущего Пользователя.
        """
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        results = self.paginate_queryset(subscriptions,)
        serializer = SubscribeSerializer(
            results,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data,)
