from django.urls.conf import include
from django.contrib import admin
from django.urls import path
from social_django import urls as social_django_urls

urlpatterns = [
    path('', include('app.urls', namespace='app')),
    path('admin/', admin.site.urls),
    path('social-auth/', include(social_django_urls, namespace='social'))]