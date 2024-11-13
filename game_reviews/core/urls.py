# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account_details, name='account_details'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('games/', views.game_list, name='game_list'),
    path('game/create/', views.create_game, name='create_game'),  # Add this line if missing
    path('game/edit/<int:game_id>', views.edit_game, name='edit_game'),
    path('game/delete/<int:game_id>', views.delete_game, name='delete_game'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
