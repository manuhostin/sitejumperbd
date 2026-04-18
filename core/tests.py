from unittest.mock import patch

from django.test import SimpleTestCase
from django.core.exceptions import ImproperlyConfigured

from sitejumper import settings


class SettingsConfigurationTests(SimpleTestCase):
    def test_resolve_secret_key_uses_env_value_when_available(self):
        with patch.object(
            settings,
            'env',
            side_effect=lambda key, default='': 'configured-secret' if key == 'SECRET_KEY' else default,
        ):
            self.assertEqual(settings._resolve_secret_key(debug=False), 'configured-secret')

    def test_resolve_secret_key_requires_value_in_production(self):
        with patch.object(
            settings,
            'env',
            side_effect=lambda key, default='': '' if key == 'SECRET_KEY' else default,
        ):
            with self.assertRaises(ImproperlyConfigured):
                settings._resolve_secret_key(debug=False)

    def test_vercel_origin_regex_is_enabled(self):
        self.assertIn(r'^https://.*\.vercel\.app$', settings.CORS_ALLOWED_ORIGIN_REGEXES)
