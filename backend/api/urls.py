from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientsViewSet, TagsViewSet
from users.views import UserDetail, UserListCreate


router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    # по данным эндпоинтам реализуются GET-запросы к /users/, /users/<int:pk>/
    # и POST-запросы к /users/
    path('users/', UserListCreate.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='profile'),

    # по данным эндпоинтам реализуются стандартные эндпоинты djoser
    # GET-запросы к /users/me/ и
    # POST-запросы к /users/set_password/
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

    # по данным эндпоинтам реализуются эндпоинты Authtoken
    # POST-запросы к /auth/token/login/, /auth/token/logout/
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('', include(router.urls)),

]