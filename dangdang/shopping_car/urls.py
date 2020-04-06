from django.urls import path
from shopping_car import views

app_name = 'shopping_car'


urlpatterns = [
    path('add_car/', views.add_car, name='add_car'),
    path('shopping_car/', views.shopping_car, name='shopping_car'),
    path('reduce_car/', views.reduce_car, name='reduce_car'),
    path('del_car/', views.del_car, name='del_car'),

]
