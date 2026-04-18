from core.models import Comment, Game, Like, View


def serialize_game(game: Game) -> dict:
    return {
        "game_id": game.game_id,
        "created_at": game.created_at,
        "updated_at": game.updated_at,
    }


def serialize_game_detail(game: Game) -> dict:
    return {
        "game_id": game.game_id,
        "created_at": game.created_at,
        "updated_at": game.updated_at,
        "statistics": {
            "likes": game.likes.count(),
            "comments": game.comments.count(),
            "views": game.views.count(),
        },
    }


def serialize_comment(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "game_id": comment.game_id,
        "user_id": comment.user_id,
        "text": comment.text,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }


def serialize_like(like: Like) -> dict:
    return {
        "id": like.id,
        "game_id": like.game_id,
        "user_id": like.user_id,
        "created_at": like.created_at,
    }


def serialize_view(view: View) -> dict:
    return {
        "id": view.id,
        "game_id": view.game_id,
        "user_id": view.user_id,
        "ip_address": view.ip_address,
        "created_at": view.created_at,
    }
