from unittest.mock import patch

from django.test import SimpleTestCase

from sitejumper import settings


class SettingsConfigurationTests(SimpleTestCase):
    def test_resolve_secret_key_uses_env_value_when_available(self):
        with patch.object(
            settings,
            'env',
            side_effect=lambda key, default='': 'configured-secret' if key == 'SECRET_KEY' else default,
        ):
            self.assertEqual(settings._resolve_secret_key(debug=False), 'configured-secret')

    def test_resolve_secret_key_generates_value_in_production(self):
        with patch.object(
            settings,
            'env',
            side_effect=lambda key, default='': '' if key == 'SECRET_KEY' else default,
        ):
            generated_secret = settings._resolve_secret_key(debug=False)

        self.assertTrue(generated_secret)
        self.assertNotEqual(
            generated_secret,
            'django-insecure-wxl5s1zg!i3q816y4@a8*lvyjs7ll9br+o-#_2a)))akhthisc',
        )

    def test_vercel_origin_regex_is_enabled(self):
        self.assertIn(r'^https://.*\.vercel\.app$', settings.CORS_ALLOWED_ORIGIN_REGEXES)
