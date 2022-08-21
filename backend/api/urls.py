from django.urls import include, path

from users.views import UserDetail, UserListCreate


urlpatterns = [
    # по данным эндпоинтам реализуются GET-запросы к /users/, /users/<int:pk>/
    # и POST-запросы к /users/
    path('users/', UserListCreate.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='profile'),

    # по данным эндпоинтам реализуются стандартные эндпоинты djoser
    # POST-запросы к /users/me/, /users/set_password/
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

    # по данным эндпоинтам реализуется эндпоинты Authtoken
    # POST-запросы к /auth/token/login/, /auth/token/logout/
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]