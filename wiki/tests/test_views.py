from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from wiki.models import Page, PageVersion


def _create_page(slug, page_versions):
    page_instance = Page.objects.create(slug=slug)
    for page in page_versions:
        PageVersion.objects.create(page=page_instance, **page)
    return page_instance


class ViewsTest(TestCase):

    def setUp(self):
        user_model = get_user_model()
        self.c = Client()
        self.user = user_model.objects.create_user(
            username="lawrence",
            email="lawrence@gmail.com",
            password="test124"
        )

        self.c.post(reverse('login'), {
            'username': 'lawrence',
            'password': 'test124'
        })

        _create_page('test_page_1', [
        {
            'title': "Test page 1",
            'content': "content of test page 1",
            'author': self.user
        }, 
        {
            'title': "Test page 1 version 2",
            'content': "content of test page 1 version 2",
            'author': self.user
        }
        ])
        _create_page('test_page_2', [{
            'title': "Test page 2",
            'content': "content of test page 2",
            'author': self.user
        }])

    def test_homepage_contains_pages_list(self):
        response = self.c.get('/')
        self.assertContains(response, "Test page 1")
        self.assertContains(response, "Test page 2")

    def test_displays_page(self):
        response = self.c.get('/test_page_1')
        self.assertContains(response, 'content of test page 1')

    def test_creates_new_page(self):
        response = self.c.post(reverse('new_page'), {
            'slug': 'test_page_3',
            'title': "Test page 3",
            'content': "content of test page 3"
        })
        self.assertEqual(302, response.status_code)
        pg = Page.objects.get(slug="test_page_3").best_version
        self.assertIsNotNone(pg)
        self.assertEqual("Test page 3", pg.title)

    def test_duplicate_page(self):
        response = self.c.post(reverse('new_page'), {
            'slug': 'test_page_1',
            'title': "Test page 1",
            'content': "content of test page 1"
        })
        self.assertEqual(200, response.status_code)
        self.assertFormError(
            response,
            "page_form",
            "slug",
            "Page with this slug already exists!"
        )

    def test_retrieves_exact_page_version_1(self):
        response = self.c.get('/test_page_1/1')
        self.assertContains(response, 'content of test page 1')

    def test_retrieves_exact_page_version_2(self):
        response = self.c.get('/test_page_1/2')
        self.assertContains(response, 'content of test page 1 version 2')
