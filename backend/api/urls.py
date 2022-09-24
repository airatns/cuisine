from django.urls import include, path
from recipes.views import (DownloadShoppingCart, IngredientViewSet,
                           RecipeViewSet, TagViewSet, fav_recipe,
                           shopping_cart)
from rest_framework.routers import DefaultRouter
from users.views import (MeDetail, Subscriptions, UserDetail, UserListCreate,
                         subscribe)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    # по данным эндпоинтам реализуются
    # POST и DELETE-запросы по Подписке на автора
    # GET-запросы на вывод всех Подписок Пользователя
    path('users/<int:author_id>/subscribe/', subscribe, name='subscribe'),
    path('users/subscriptions/',
         Subscriptions.as_view(), name='subscriptions'),

    # по данному эндпоинту реализуются
    # POST и DELETE-запросы на добавление рецептов в Избранное
    path('recipes/<int:recipe_id>/favorite/', fav_recipe, name='favorite'),

    # по данному эндпоинту реализуются
    # POST и DELETE-запросы на добавление рецептов в Список покупок
    path('recipes/<int:recipe_id>/shopping_cart/',
         shopping_cart, name='shopping'),

    # по данному эндпоинту реализуется выгрузка Списка для покупок
    path('recipes/download_shopping_cart/',
         DownloadShoppingCart.as_view(), name='download'),

    # по данным эндпоинтам реализуются
    # GET-запросы к выводу списка Пользователей и
    # Детальной информации о Пользователе,
    # POST-запросы на создание Пользователя
    path('users/', UserListCreate.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='profile'),
    path('users/me/', MeDetail.as_view(), name='me'),

    # по данным стандартным эндпоинтам djoser реализуются
    # POST-запросы на смену пароля
    # /users/set_password/
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

    # по данным эндпоинтам Authtoken реализуются
    # POST-запросы на получение токена
    # /auth/token/login/, /auth/token/logout/
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # здесь генерятся эндпоинты для остальных запросов
    path('', include(router.urls)),
]
