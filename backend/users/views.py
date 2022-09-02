from rest_framework import mixins, status, viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from djoser.views import UserViewSet
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import User, Subscription
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


@api_view(['POST', 'DELETE'])
@action(detail=False, url_path='subscribe')
def subscribe(request, author_id):
    """Метод по созданию и удалению Подписки на автора.
    """
    user = request.user
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
        return Response({
                'message': 'Вы не подписывались на данного автора',
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@action(detail=False, url_path='subscriptions')
def subscriptions(request):
    """Метод по выводу всех Подписок на автора текущего Пользователя.
    """
    user = request.user
    subscriptions = Subscription.objects.filter(user=user)
    serializer = SubscribeSerializer(subscriptions, many=True)
    return Response(serializer.data)
