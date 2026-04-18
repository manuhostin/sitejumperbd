from django.urls import path

from . import views

urlpatterns = [
    path("games/", views.GameListView.as_view(), name="games_list"),
    path("games/<int:pk>/", views.GameDetailView.as_view(), name="games_detail"),
    path("games/<int:pk>/comments/", views.CommentListView.as_view(), name="games_comments"),
    path("games/<int:pk>/like/", views.LikeView.as_view(), name="games_like"),
    path("games/<int:pk>/likes/", views.LikeListView.as_view(), name="games_likes"),
    path("games/<int:pk>/views/", views.ViewCreateView.as_view(), name="games_views"),
]
