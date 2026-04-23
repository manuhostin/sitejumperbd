import logging
from functools import wraps

import jwt
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def _validate_jwt(token):
    """Decode and verify a Supabase JWT.  Returns the payload dict or None."""
    secret = getattr(settings, 'SUPABASE_JWT_SECRET', '')
    if not secret:
        logger.warning(
            'SUPABASE_JWT_SECRET is not configured; skipping token validation'
        )
        return None
    try:
        return jwt.decode(
            token,
            secret,
            algorithms=[settings.JWT_ALGORITHM],
            options={'verify_signature': True},
        )
    except jwt.ExpiredSignatureError:
        logger.warning('Supabase JWT expired')
    except jwt.InvalidTokenError as exc:
        logger.warning('Supabase JWT invalid: %s', exc)
    except Exception as exc:
        logger.error('Unexpected error validating Supabase JWT: %s', exc)
    return None


class SupabaseAuthMiddleware:
    """
    Middleware to validate Supabase JWT tokens.

    When an Authorization: Bearer <token> header is present the token is
    validated against SUPABASE_JWT_SECRET.  On success, ``request.supabase_user``
    is populated with the decoded payload so downstream views can read
    ``request.supabase_user['sub']`` (user id) and ``request.supabase_user['email']``.

    Routes listed in ``SUPABASE_AUTH_PUBLIC_PATHS`` (settings) are skipped
    entirely.  All other routes that present an invalid/expired token receive a
    401 response.  Routes with *no* Authorization header are passed through
    without error so that unauthenticated endpoints continue to work; individual
    views can use the ``@require_supabase_auth`` decorator to enforce auth.

    Raises ``ImproperlyConfigured`` at startup when ``DEBUG=False`` and
    ``SUPABASE_JWT_SECRET`` is not set, preventing silent auth failures in
    production.
    """

    def __init__(self, get_response):
        if not getattr(settings, 'DEBUG', True) and not getattr(settings, 'SUPABASE_JWT_SECRET', ''):
            raise ImproperlyConfigured(
                'SUPABASE_JWT_SECRET must be set when DEBUG=False. '
                'Add it to your environment variables.'
            )
        self.get_response = get_response
        self.public_paths = getattr(
            settings,
            'SUPABASE_AUTH_PUBLIC_PATHS',
            ['/admin/'],
        )

    def __call__(self, request):
        request.supabase_user = None

        if not self._is_public_path(request.path):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                payload = _validate_jwt(auth_header[7:])
                if payload is None:
                    return JsonResponse(
                        {'error': 'Invalid or expired token'},
                        status=401,
                    )
                request.supabase_user = payload

        return self.get_response(request)

    def _is_public_path(self, path):
        return any(path.startswith(p) for p in self.public_paths)


def require_supabase_auth(view_func):
    """
    Decorator that enforces Supabase JWT authentication on a single view.

    Use this on views that must be protected even when the middleware is
    configured with broad public-path exemptions.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization required'}, status=401)

        payload = _validate_jwt(auth_header[7:])
        if payload is None:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        request.supabase_user = payload
        return view_func(request, *args, **kwargs)

    return wrapped_view
