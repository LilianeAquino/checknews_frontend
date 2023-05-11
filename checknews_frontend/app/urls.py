from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('listagem/', views.login, name='listagem'),
    path('checagem/', views.login, name='checagem'),
    path('perfil/', views.login, name='perfil'),
    path('sobre/', views.login, name='sobre'),
    path('admin/', views.login, name='admin'),
]
