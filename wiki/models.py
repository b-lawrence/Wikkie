from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Max


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

    def __str__(self):
        return "version {0} of {1}".format(self.version, self.title)


@receiver(pre_save, sender=PageVersion)
def increment_page_version(sender, instance, *args, **kwargs):
    recent_version = (instance.page.pageversion_set.
                      aggregate(Max("version"))['version__max'])
    if recent_version:
        instance.version = recent_version + 1
    else:
        instance.version = 1
