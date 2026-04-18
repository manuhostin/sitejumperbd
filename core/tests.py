from django.conf import settings
from django.test import SimpleTestCase


class DeploymentSettingsTests(SimpleTestCase):
    def test_vercel_regex_enabled_for_cors(self):
        self.assertIn(
            r'^https:\/\/[a-zA-Z0-9-]+\.vercel\.app$',
            settings.CORS_ALLOWED_ORIGIN_REGEXES,
        )

    def test_onrender_host_allowed(self):
        self.assertIn('.onrender.com', settings.ALLOWED_HOSTS)
