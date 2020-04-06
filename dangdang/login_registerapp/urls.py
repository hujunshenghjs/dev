from django.urls import path
from login_registerapp import views

app_name = 'login_registerapp'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_logic/', views.register_logic, name='register_logic'),
    path('login/', views.login, name='login'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('captcha/', views.captcha, name='captcha'),
    path('checkname/', views.checkname, name='checkname'),
    path('check_captcha/', views.check_captcha, name='check_captcha'),
    path('register_ok/', views.register_ok, name='register_ok'),
    path('sign_out/', views.sign_out, name='sign_out'),

]
