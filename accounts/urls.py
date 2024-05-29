from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp/', views.sign_up, name='signUp'),
    path('login/', views.login, name='login'),
    path('signUp/id-check/', views.check_id, name='id-check'),
]