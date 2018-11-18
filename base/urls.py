from django.urls import path
from . import views



app_name='base'

urlpatterns = [
    path('select_customer_level/',views.select_customer_level,name='select_customer_level')
]