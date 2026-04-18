import re

from django.conf import settings
from django.test import SimpleTestCase


class DeploymentSettingsTests(SimpleTestCase):
    def test_vercel_regex_enabled_for_cors(self):
        self.assertIn(
            r'^https:\/\/[a-zA-Z0-9_-]+\.vercel\.app$',
            settings.CORS_ALLOWED_ORIGIN_REGEXES,
        )

    def test_vercel_regex_matches_valid_origin(self):
        pattern = settings.CORS_ALLOWED_ORIGIN_REGEXES[0]
        self.assertIsNotNone(re.match(pattern, 'https://meu-front.vercel.app'))

    def test_vercel_regex_rejects_invalid_origin(self):
        pattern = settings.CORS_ALLOWED_ORIGIN_REGEXES[0]
        self.assertIsNone(re.match(pattern, 'https://meu-front.example.com'))

    def test_onrender_host_allowed(self):
        self.assertIn('.onrender.com', settings.ALLOWED_HOSTS)
