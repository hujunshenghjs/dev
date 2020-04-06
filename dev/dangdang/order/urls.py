from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('indent_page/', views.indent_page, name='indent_page'),
    path('select_address/', views.select_address, name='select_address'),
    path('submit_address/', views.submit_address, name='submit_address'),
    path('indent_ok/', views.indent_ok, name='indent_ok'),
]
