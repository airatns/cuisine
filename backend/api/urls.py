from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from users.views import UserViewSet


router = DefaultRouter()
# router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]