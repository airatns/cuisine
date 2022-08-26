from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserDetail, UserListCreate


router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    # по данным эндпоинтам реализуются 
    # GET-запросы к /users/, /users/<int:pk>/ и
    # POST-запросы к /users/
    path('users/', UserListCreate.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='profile'),

    # по данным стандартным эндпоинтам djoser реализуются
    # GET-запросы к /users/me/ и
    # POST-запросы к /users/set_password/
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

    # по данным эндпоинтам Authtoken реализуются
    # POST-запросы к /auth/token/login/, /auth/token/logout/
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # здесь генерятся эндпоинты для остальных запросов
    path('', include(router.urls)),

]