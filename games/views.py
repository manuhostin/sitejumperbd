import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.models import Comment, Game, Like, View as GameView
from .serializers import (
	serialize_comment,
	serialize_game,
	serialize_game_detail,
	serialize_like,
	serialize_view,
)


@method_decorator(csrf_exempt, name="dispatch")
class GameListView(View):
	def get(self, request):
		games = Game.objects.all()
		return JsonResponse([serialize_game(game) for game in games], safe=False)

	def post(self, request):
		try:
			data = json.loads(request.body or "{}")
		except json.JSONDecodeError:
			return JsonResponse({"error": "JSON inválido"}, status=400)

		game_id = data.get("game_id")
		if not game_id:
			return JsonResponse({"error": "game_id é obrigatório"}, status=400)

		game, created = Game.objects.get_or_create(game_id=game_id)
		response = serialize_game(game)
		response["created"] = created
		return JsonResponse(response, status=201 if created else 200)


class GameDetailView(View):
	def get(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		return JsonResponse(serialize_game_detail(game), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CommentListView(View):
	def get(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		comments = [serialize_comment(comment) for comment in game.comments.all()]
		return JsonResponse(
			{
				"game_id": pk,
				"total_comments": len(comments),
				"comments": comments,
			},
			status=200,
		)

	def post(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		try:
			data = json.loads(request.body or "{}")
		except json.JSONDecodeError:
			return JsonResponse({"error": "JSON inválido"}, status=400)

		text = data.get("text")
		if not text:
			return JsonResponse({"error": "text é obrigatório"}, status=400)

		comment = Comment.objects.create(
			game=game,
			user_id=data.get("user_id"),
			text=text,
		)
		return JsonResponse(serialize_comment(comment), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class LikeView(View):
	def post(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		try:
			data = json.loads(request.body or "{}")
		except json.JSONDecodeError:
			return JsonResponse({"error": "JSON inválido"}, status=400)

		like, created = Like.objects.get_or_create(game=game, user_id=data.get("user_id"))
		return JsonResponse(
			{
				"game_id": pk,
				"user_id": like.user_id,
				"liked": created,
				"message": "Curtida adicionada" if created else "Este usuário já curtiu",
			},
			status=201 if created else 200,
		)


@method_decorator(csrf_exempt, name="dispatch")
class ViewCreateView(View):
	def post(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		try:
			data = json.loads(request.body or "{}")
		except json.JSONDecodeError:
			return JsonResponse({"error": "JSON inválido"}, status=400)

		view = GameView.objects.create(
			game=game,
			user_id=data.get("user_id"),
			ip_address=request.META.get("REMOTE_ADDR"),
		)
		return JsonResponse(serialize_view(view), status=201)


class LikeListView(View):
	def get(self, request, pk):
		game = get_object_or_404(Game, game_id=pk)
		likes = [serialize_like(like) for like in game.likes.all()]
		return JsonResponse(
			{
				"game_id": pk,
				"total_likes": len(likes),
				"likes": likes,
			},
			status=200,
		)
