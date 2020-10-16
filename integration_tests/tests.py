from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from rest_framework import status
from rest_framework.test import APIClient


class APIStaticLiveServerTestCase(StaticLiveServerTestCase):
    """
    Class to add DRF's APIClient to Django's "auto-collect static files" live server class
    """
    client_class = APIClient


class FunctionalTest(APIStaticLiveServerTestCase):
    """
    Default DRF's JSONRenderer result structure:

    {
    "count": 4,
    "next": "http://127.0.0.1:8000/snippets/?page=2",
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/snippets/1/",
            "id": 1,
            "highlight": "http://127.0.0.1:8000/snippets/1/highlight/",
            "owner": "superuser",
            "title": "S1",
            "code": "from django.urls import path, include\r\nfrom rest_framework.urlpatterns import format_suffix_patterns\r\nfrom snippets import views\r\n\r\nurlpatterns = [\r\n    path('snippets/'        , views.SnippetList.as_view()),\r\n    path('snippets/<int:pk>', views.SnippetDetail.as_view()),\r\n    path('users/'           , views.UserList.as_view()),\r\n    path('users/<int:pk>'   , views.UserDetail.as_view()),\r\n    path('api-auth/'        , include('rest_framework.urls')),\r\n]\r\n\r\nurlpatterns = format_suffix_patterns(urlpatterns)",
            "linenos": false,
            "language": "python",
            "style": "solarized-dark"
        },
        {
            "url": "http://127.0.0.1:8000/snippets/2/",
            "id": 2,
            "highlight": "http://127.0.0.1:8000/snippets/2/highlight/",
            "owner": "superuser",
            "title": "S2",
            "code": "daasdasd",
            "linenos": false,
            "language": "python",
            "style": "solarized-dark"
        },
        {
            "url": "http://127.0.0.1:8000/snippets/3/",
            "id": 3,
            "highlight": "http://127.0.0.1:8000/snippets/3/highlight/",
            "owner": "superuser",
            "title": "S3",
            "code": "lalalala",
            "linenos": false,
            "language": "python",
            "style": "solarized-dark"
        }
    ]
}
    """

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # cls.foo = Foo.objects.create(bar="Test")
        pass

    def test_simulations_get_endpoint(self):
        response = self.client.get("/api/simulations/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        actual_simulations = response.json()["results"]
        self.assertEqual(len(actual_simulations), 3)
