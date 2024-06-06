from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.board_main, name='main'),
    path('write/', views.board_write, name='write'),
    path('<int:meeting_id>/', views.board_detail, name='detail'),
    path('<int:meeting_id>/edit/', views.board_edit, name='edit'),
    path('<int:meeting_id>/delete/', views.board_delete, name='delete'),
]