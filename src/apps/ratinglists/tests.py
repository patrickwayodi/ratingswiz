"""
Run the test as follows:
python manage.py test apps.ratinglists.tests

# Add this in settings.py in order to disable django-debug-toolbar when running tests
if not TESTING:
    # Application definitions
    # https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS =
"""


from django.test import Client, TestCase


class GameDetailTestCase(TestCase):

    """
    https://docs.djangoproject.com/en/4.2/topics/testing/tools.html
    """

    fixtures = [
        "games.json",
    ]

    def setUp(self):

        # Every test needs a client.
        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0")

    def test_game_detail(self):

        # Issue a GET request.
        response = self.client.get("/game/1/")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

