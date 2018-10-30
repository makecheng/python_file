from django.urls import path
from . import views


# 设置命名空间
app_name='system'

urlpatterns = [
    path('login_register/',views.login_register,name='login_register'),
    path('system/unique_username/',views.unqiue_username,name='unqiue_username'),
    path('system/unique_email/',views.unique_email,name='unique_email'),
    path('system/format_addr/',views.format_addr,name='format_addr'),
    path('system/send_email/',views.send_email,name='send_email'),
    path('system/active_accounts/',views.active_accounts,name='active_accounts'),
    path('system/login_user/',views.login_user,name='login_user'),
    path('index/',views.index,name='index'),
    path('system/update_password/',views.update_password,name='update_password'),
    path('system/logout/', views.logout, name='logout'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('system/forget_username/',views.forget_username,name='forget_username'),
    path('system/forget_email/',views.forget_email,name='forget_email'),
    path('system/forget_format_addr/', views.forget_format_addr, name='forget_format_addr'),
    path('system/forget_send_email/', views.forget_send_email, name='forget_send_email'),
    path('system/forget_new_pwd/',views.forget_new_pwd,name='forget_new_pwd'),
    path('system/forget_active_accounts/', views.forget_active_accounts, name='forget_active_accounts'),
]