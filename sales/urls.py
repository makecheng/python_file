from django.urls import path
from . import views


# 命名空间
app_name='sales'

urlpatterns = [
    path('sales_chance_index/',views.sales_chance_index,name='sales_chance_index'),
    path('select_sales_chance_list/',views.select_sales_chance_list,name='select_sales_chance_list'),
    path('create_sale_chance/',views.create_sale_chance,name='create_sale_chance'),
    path('select_sale_chance_by_id/',views.select_sale_chance_by_id,name='select_sale_chance_by_id'),
    path('update_sale_chance/',views.update_sale_chance,name='update_sale_chance'),
    path('delect_sale_chance/',views.delect_sale_chance,name='delect_sale_chance'),
    path('cus_dev_plan_index/',views.cus_dev_plan_index,name='cus_dev_plan_index'),
    path('select_sale_chance_for_cus_dev_plan/',views.select_sale_chance_for_cus_dev_plan,name='select_sale_chance_for_cus_dev_plan'),
    path('select_sc_by_id/<int:sale_chance_id>/', views.select_sc_by_id, name='select_sc_by_id'),
    path('select_cus_dev_plan_by_sale_chance_id/<int:sale_chance_id>/',views.select_cus_dev_plan_by_sale_chance_id,name='select_cus_dev_plan_by_sale_chance_id'),
    path('create_cus_dev_plan/<int:sale_chance_id>/',views.create_cus_dev_plan,name='create_cus_dev_plan'),
    path('update_cus_dev_plan/',views.update_cus_dev_plan,name='update_cus_dev_plan'),
    path('delete_cus_dev_plan/',views.delete_cus_dev_plan,name='delete_cus_dev_plan'),
    path('update_dev_result/',views.update_dev_result,name='update_dev_result'),
]