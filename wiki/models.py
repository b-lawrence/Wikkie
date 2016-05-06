from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.conf import settings
from django.dispatch import receiver


# Create your models here.
class Page(models.Model):

    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.best_version.title

    def get_absolute_url(self):
        return reverse("page", args=[self.slug])

    @property
    def best_version(self):
        return self.pageversion_set.filter().order_by("version").last()


class PageVersion(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    version = models.IntegerField(null=False)
    title = models.CharField(max_length=50)
    content = models.TextField(null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=PageVersion)
def save(sender, instance, *args, **kwargs):
    # TODO: Implement versioning logic
    instance.version = 1
