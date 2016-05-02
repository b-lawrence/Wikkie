from django.db import models

# Create your models here.
class Page(models.Model):

    def __str__(self):
        return "<Page: slug={}".format(self.slug)

    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
