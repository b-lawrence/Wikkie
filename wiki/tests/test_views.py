from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from wiki.models import Page, PageVersion


class ViewsTest(TestCase):

    def setUp(self):
        self.c = Client()
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="lawrence",
            email="lawrence@gmail.com",
            password="test124"
        )

        self.c.post(reverse('login'), {
            'username': 'lawrence',
            'password': 'test124'
        })

        pages = [
            {
                'slug': 'test_page_1',
                'title': "Test page 1",
                'content': "content of test page 1",
                'author': user
            },
            {
                'slug': 'test_page_2',
                'title': "Test page 2",
                'content': "content of test page 2",
                'author': user
            }
        ]

        for page in pages:
            pg_instance = Page.objects.create(slug=page.pop('slug'))
            PageVersion.objects.create(page=pg_instance, **page)

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
