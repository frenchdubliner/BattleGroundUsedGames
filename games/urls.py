from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('add/', views.add_game, name='add_game'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('<int:game_id>/delete/', views.delete_game, name='delete_game'),
    path('my-games/', views.my_games, name='my_games'),
    path('admin-games/', views.admin_only_games, name='admin_only_games'),
]
