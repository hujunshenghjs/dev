from django.urls import path
from home import views

app_name = 'home'


urlpatterns = [
    path('index/', views.index, name='index'),
    path('book_list/', views.book_list, name='book_list'),
    path('book_details/', views.book_details, name='book_details'),

]
