from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Game, Like, Comment, View


@require_http_methods(["GET", "POST"])
@csrf_exempt
def game_list(request):
    """Lista todos os games ou cria um novo"""
    if request.method == 'GET':
        games = Game.objects.all().values('game_id', 'created_at', 'updated_at')
        return JsonResponse(list(games), safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            
            if not game_id:
                return JsonResponse({'error': 'game_id é obrigatório'}, status=400)
            
            game, created = Game.objects.get_or_create(game_id=game_id)
            return JsonResponse({
                'game_id': game.game_id,
                'created': created,
                'created_at': game.created_at,
                'updated_at': game.updated_at
            }, status=201 if created else 200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)


@require_http_methods(["GET"])
def game_detail(request, game_id):
    """Retorna detalhes de um game com estatísticas"""
    game = get_object_or_404(Game, game_id=game_id)
    
    likes_count = game.likes.count()
    comments_count = game.comments.count()
    views_count = game.views.count()
    
    return JsonResponse({
        'game_id': game.game_id,
        'created_at': game.created_at,
        'updated_at': game.updated_at,
        'statistics': {
            'likes': likes_count,
            'comments': comments_count,
            'views': views_count
        }
    })


@require_http_methods(["GET"])
def game_likes(request, game_id):
    """Lista todas as curtidas de um game"""
    game = get_object_or_404(Game, game_id=game_id)
    likes = game.likes.all().values('id', 'user_id', 'created_at')
    return JsonResponse({
        'game_id': game_id,
        'total_likes': game.likes.count(),
        'likes': list(likes)
    })


@require_http_methods(["POST"])
@csrf_exempt
def add_like(request, game_id):
    """Adiciona uma curtida em um game"""
    try:
        game = get_object_or_404(Game, game_id=game_id)
        data = json.loads(request.body) if request.body else {}
        user_id = data.get('user_id')
        
        like, created = Like.objects.get_or_create(game=game, user_id=user_id)
        
        return JsonResponse({
            'game_id': game_id,
            'user_id': user_id,
            'liked': created,
            'message': 'Curtida adicionada' if created else 'Este usuário já curtiu'
        }, status=201 if created else 200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)


@require_http_methods(["DELETE"])
@csrf_exempt
def remove_like(request, game_id):
    """Remove uma curtida de um game"""
    try:
        game = get_object_or_404(Game, game_id=game_id)
        data = json.loads(request.body) if request.body else {}
        user_id = data.get('user_id')
        
        like = Like.objects.filter(game=game, user_id=user_id).first()
        if like:
            like.delete()
            return JsonResponse({
                'game_id': game_id,
                'user_id': user_id,
                'message': 'Curtida removida'
            }, status=200)
        
        return JsonResponse({
            'error': 'Curtida não encontrada'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)


@require_http_methods(["GET"])
def game_comments(request, game_id):
    """Lista todos os comentários de um game"""
    game = get_object_or_404(Game, game_id=game_id)
    comments = game.comments.all().values('id', 'user_id', 'text', 'created_at', 'updated_at')
    return JsonResponse({
        'game_id': game_id,
        'total_comments': game.comments.count(),
        'comments': list(comments)
    })


@require_http_methods(["POST"])
@csrf_exempt
def add_comment(request, game_id):
    """Adiciona um comentário em um game"""
    try:
        game = get_object_or_404(Game, game_id=game_id)
        data = json.loads(request.body)
        user_id = data.get('user_id')
        text = data.get('text')
        
        if not text:
            return JsonResponse({'error': 'text é obrigatório'}, status=400)
        
        comment = Comment.objects.create(game=game, user_id=user_id, text=text)
        
        return JsonResponse({
            'id': comment.id,
            'game_id': game_id,
            'user_id': user_id,
            'text': comment.text,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)


@require_http_methods(["GET"])
def game_views(request, game_id):
    """Lista todas as visualizações de um game"""
    game = get_object_or_404(Game, game_id=game_id)
    views = game.views.all().values('id', 'user_id', 'ip_address', 'created_at')
    return JsonResponse({
        'game_id': game_id,
        'total_views': game.views.count(),
        'views': list(views)
    })


@require_http_methods(["POST"])
@csrf_exempt
def add_view(request, game_id):
    """Registra uma visualização de um game"""
    try:
        game = get_object_or_404(Game, game_id=game_id)
        data = json.loads(request.body) if request.body else {}
        user_id = data.get('user_id')
        ip_address = request.META.get('REMOTE_ADDR')
        
        view = View.objects.create(game=game, user_id=user_id, ip_address=ip_address)
        
        return JsonResponse({
            'id': view.id,
            'game_id': game_id,
            'user_id': user_id,
            'ip_address': ip_address,
            'created_at': view.created_at
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
