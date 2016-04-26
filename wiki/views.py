from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import PageForm
from .models import Page


def page(request, slug):
    page = None

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        pass

    return render(request, "page.html", context={
        "page": page,
        "slug": slug})


def home_page(request):
    return render(request, "home.html", context={"title": "Wikkie"})

def page_edit(request, slug):
    page = None

    if request.method == 'GET':
        page_form = PageForm()

    elif request.method == 'POST':
        page_form = PageForm(request.POST)
        saved_page = page_form.save()
        saved_page.slug = slug
        saved_page.save()

    return render(request, "edit_page.html", context={
        "page": page,
        "slug": slug,
        "page_form": page_form})

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        pass
