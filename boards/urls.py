from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.board_main, name='main'),
    path('write/', views.board_write, name='write'),
    path('<int:meeting_id>/', views.board_detail, name='detail'),
    path('<int:meeting_id>/edit/', views.board_edit, name='edit'),
    path('<int:meeting_id>/delete/', views.board_delete, name='delete'),
    path('<int:meeting_id>/comment-delete/<int:comment_id>/', views.comment_delete, name='comment-delete'),
    path('<int:meeting_id>/participate/', views.board_participate, name='participate'),
    path('<int:meeting_id>/participate-delete/', views.board_participate_delete, name='participate-delete'),
    path('<int:meeting_id>/gather-done/', views.board_gather_done, name='gather-done'),
    path('<int:meeting_id>/settle/', views.board_settle, name='settle'),
]