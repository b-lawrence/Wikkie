from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown import markdown
import bleach

from .forms import PageForm, NewPageForm
from .models import Page


def home_page(request):
    return render(request, "wiki/home.html", context={"title": "Wikkie"})


def page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None

    allowed_tags = bleach.ALLOWED_TAGS + ['p', 'h1', 'h2', 'h3']
    page_content = bleach.clean(markdown(page.content), tags=allowed_tags) if page else None
    page_title = page.title if page else slug

    return render(request, "wiki/page.html", context={
        "page": page,
        "slug": slug,
        "page_title": page_title,
        "page_content": page_content})


def new_page(request):
    if request.method == 'GET':
        page_form = NewPageForm()
    elif request.method == 'POST':
        page_form = NewPageForm(request.POST)
        if page_form.is_valid():
            page_form.save()
            return redirect("page", page_form.cleaned_data['slug'])

    return render(request, "wiki/edit_page.html", context={
        "page_title": "Create a new wiki page.",
        "page_form": page_form})


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

    return render(request, "wiki/edit_page.html", context={
        "page_title": page.title or page.slug,
        "page_form": page_form})
