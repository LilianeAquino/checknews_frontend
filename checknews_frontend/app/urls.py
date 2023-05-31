from django.contrib.auth import views as auth_views
from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('logged_user/', views.logged_user, name='logged_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('change_user_password/', views.change_user_password, name='change_user_password'),
    path('news_listing/', views.news_listing, name='news_listing'),
    path('users_listing/', views.users_listing, name='users_listing'),
    path('models_listing/', views.models_listing, name='models_listing'),
    path('report/news', views.generate_report_news, name='generate_report_news'),
    path('report/users', views.generate_report_users, name='generate_report_users'),
    path('check/', views.news_check, name='news_check'),
    path('process_new/', views.process_form_news, name='process_form_news'),
    path('checked_news/', views.checked_news, name='checked_news'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin, name='admin'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/recover_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/recover_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/recover_password/password_reset_complete.html'), name='password_reset_complete'),
]
