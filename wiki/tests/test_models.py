from django.test import TestCase
from wiki.models import PageVersion, Page
from django.contrib.auth import get_user_model


class PageVersionTest(TestCase):

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="lawrence",
            email="lawrence@gmail.com",
            password="test124"
        )

        self.page = Page.objects.create(slug="page_version_1")

    def test_first_page_version_is_1(self):
        page_version_1 = PageVersion.objects.create(
            title="Version 1",
            content="content of version 1",
            author=self.user,
            page=self.page
        )

        self.assertEquals(1, page_version_1.version)
