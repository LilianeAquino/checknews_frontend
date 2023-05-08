from django.urls.conf import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', include('app.urls', namespace='app')),
    path('admin/', admin.site.urls),
]