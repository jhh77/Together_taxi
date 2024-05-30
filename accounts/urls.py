from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp/', views.signUp, name='signUp'), #회원가입
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), #로그인
    path('signUp/id-check/', views.check_id, name='id-check'), #아이디 중복 검사
    path('signUpComplete/', views.signUpComplete, name='signUpComplete'),
]