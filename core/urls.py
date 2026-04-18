from django.urls import path
from . import views

urlpatterns = [
    # Games
    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    
    # Likes
    path('games/<int:game_id>/likes/', views.game_likes, name='game_likes'),
    path('games/<int:game_id>/like/', views.add_like, name='add_like'),
    path('games/<int:game_id>/unlike/', views.remove_like, name='remove_like'),
    
    # Comments
    path('games/<int:game_id>/comments/', views.game_comments, name='game_comments'),
    path('games/<int:game_id>/comment/', views.add_comment, name='add_comment'),
    
    # Views
    path('games/<int:game_id>/views/', views.game_views, name='game_views'),
    path('games/<int:game_id>/view/', views.add_view, name='add_view'),
]
