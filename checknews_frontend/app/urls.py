from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('logado/', views.usuario_logado, name='usuario_logado'),
    path('deslogar_usuario', views.deslogar_usuario, name='deslogar_usuario'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login_usuario/', views.logar_usuario, name='login_usuario'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('listagem/', views.listagem, name='listagem'),
    path('checagem/', views.checagem, name='checagem'),
    path('perfil/', views.perfil, name='perfil'),
    path('sobre/', views.sobre, name='sobre'),
    path('admin/', views.admin, name='admin'),
    path('reset_senha', views.resetar_senha, name='resetar_senha'),
    path('reset_senha/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/recupera_senha/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/recupera_senha/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/recupera_senha/password_reset_complete.html'), name='password_reset_complete'),
]
