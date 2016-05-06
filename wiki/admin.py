from django.contrib import admin
from .models import Page

# Register your models here.


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title', 'author', 'updated_at')
