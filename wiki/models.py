from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Page(models.Model):

    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return "slug={}".format(self.slug)

    def get_absolute_url(self):
        return reverse("page", args=[self.slug])
