from django.urls import path
from . import views


# 设置命名空间
app_name='system'

urlpatterns = [
    path('login_register/',views.login_register,name='login_register'),
    path('unqiue_username/',views.unqiue_username,name='unqiue_username'),
    path('unique_email/',views.unique_email,name='unique_email'),
    path('format_addr/',views.format_addr,name='format_addr'),
    path('send_email/',views.send_email,name='send_email'),
    path('active_accounts/',views.active_accounts,name='active_accounts'),
]