from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown import markdown
import bleach

from .forms import PageForm
from .models import Page


def home_page(request):
    return render(request, "home.html", context={"title": "Wikkie"})


def page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None

    allowed_tags = bleach.ALLOWED_TAGS + ['p', 'h1', 'h2', 'h3']
    page_content = bleach.clean(markdown(page.content), tags=allowed_tags) if page else None
    page_title = page.title if page else slug

    return render(request, "page.html", context={
        "page": page,
        "slug": slug,
        "page_title": page_title,
        "page_content": page_content})


def page_edit(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = Page(slug=slug)

    if request.method == 'GET':
        page_form = PageForm(instance=page)
    elif request.method == 'POST':
        page_form = PageForm(request.POST, instance=page)
        if page_form.is_valid():
            page_form.save()
            return redirect("page", slug)

    return render(request, "edit_page.html", context={
        "slug": slug,
        "page_title": page.title or page.slug,
        "page_form": page_form})
