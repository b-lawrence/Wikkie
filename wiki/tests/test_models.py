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

        self.page = Page.objects.create(slug="new_page")
        self.page_version_1 = PageVersion.objects.create(
            title="Version 1",
            content="Content of version 1",
            author=self.user,
            page=self.page
        )

    def test_first_page_version_is_1(self):
        self.assertEquals(1, self.page_version_1.version)

    def test_page_version_increments_by_1(self):
        page_version_2 = PageVersion.objects.create(
            title="Version 2",
            content="Content of version 1 just changed",
            author=self.user,
            page=self.page
        )
        self.assertEquals(2, page_version_2.version)
