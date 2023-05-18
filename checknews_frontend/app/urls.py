from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('logado/', views.usuario_logado, name='usuario_logado'),
    path('deslogar_usuario', views.deslogar_usuario, name="deslogar_usuario"),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('listagem/', views.listagem, name='listagem'),
    path('checagem/', views.checagem, name='checagem'),
    path('perfil/', views.perfil, name='perfil'),
    path('sobre/', views.sobre, name='sobre'),
    path('admin/', views.admin, name='admin'),
]
