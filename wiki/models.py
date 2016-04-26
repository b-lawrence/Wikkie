from django.db import models

# Create your models here.
class Page(models.Model):
    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
