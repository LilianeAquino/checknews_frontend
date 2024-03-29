from django.urls import path
from django.contrib.auth import views as auth_views

from app import views, views_crud

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('logged_user/', views.logged_user, name='logged_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('accounts/profile/', views.login_google, name='login_google'),
    path('change_user_password/', views.change_user_password, name='change_user_password'),
    path('news_listing/', views.news_listing, name='news_listing'),
    path('users_listing/', views.users_listing, name='users_listing'),
    path('models_listing/', views.models_listing, name='models_listing'),
    path('report/news', views.generate_report_news, name='generate_report_news'),
    path('report/users', views.generate_report_users, name='generate_report_users'),
    path('report/metrics', views.generate_report_metrics, name='generate_report_metrics'),
    path('report/feedbacks', views.generate_report_feedbacks, name='generate_report_feedbacks'),
    path('report/tickets', views.generate_report_tickets, name='generate_report_tickets'),
    path('check/', views.news_check, name='news_check'),
    path('process_new/', views.process_form_news, name='process_form_news'),
    path('news_detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('process_new/details/<int:news_id>/', views.process_form_news_details, name='process_form_news_details'),
    path('checked_news/', views.checked_news, name='checked_news'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/<int:user_id>/', views.update_profile_form, name='update_profile_form'),
    path('profile/update/submit/<int:user_id>/', views.update_profile, name='update_profile'),
    path('admin/', views.admin, name='admin'),
    path('about/', views.about, name='about'),
    path('feedbacks_listing/', views.feedbacks_listing, name='feedbacks_listing'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<str:ticket_id>/complete/', views.ticket_complete, name='ticket_complete'),
    path('tips/', views.add_tips, name='add_tips'),
    path('chat/', views.chat, name='chat'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/recover_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/recover_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/recover_password/password_reset_complete.html'), name='password_reset_complete'),
    path('users/delete/<int:user_id>/', views_crud.delete_user, name='delete_user'),
    path('users/update/<int:user_id>/', views_crud.update_user_form, name='update_user_form'),
    path('users/update/submit/<int:user_id>/', views_crud.update_user, name='update_user'),
    path('users/create', views_crud.create_user_form, name='create_user_form'),
    path('users/create/submit', views_crud.create_user, name='create_user')
]
