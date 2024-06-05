from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.board_main, name='main'),
    path('write/', views.board_write, name='write')
]