from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app', include('app.urls')),
    path('', RedirectView.as_view(url='/app/', permanent=True))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
