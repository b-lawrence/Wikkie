from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import bleach

from . import forms
from .models import Page


def home_page(request):
    pages = Page.objects.all()
    return render(request, "wiki/home.html", context={
        "title": "Wikkie",
        "pages": pages})


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


@login_required
def new_page(request):
    if request.method == 'GET':
        page_form = forms.NewPageForm()
    elif request.method == 'POST':
        page_form = forms.NewPageForm(request.POST)
        if page_form.is_valid():
            page_form.save()
            return redirect("page", page_form.cleaned_data['slug'])

    return render(request, "wiki/edit_page.html", context={
        "page_title": "Create a new wiki page.",
        "page_form": page_form})


@login_required
def page_edit(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = Page(slug=slug)

    if request.method == 'GET':
        page_form = forms.PageForm(instance=page)
    elif request.method == 'POST':
        page_form = forms.PageForm(request.POST, instance=page)
        if page_form.is_valid():
            page_form.save()
            return redirect("page", slug)

    return render(request, "wiki/edit_page.html", context={
        "page_title": page.title or page.slug,
        "page_form": page_form})


def register_user(request):
    if request.method == 'GET':
        signup_form = forms.SignupForm()
    elif request.method == 'POST':
        signup_form = forms.SignupForm(request.POST)
        if signup_form.is_valid():
            form_data = signup_form.cleaned_data
            User.objects.create_user(**form_data)
            user = authenticate(**form_data)
            login(request, user)
            return redirect("home")

    return render(request, "registration/signup.html", context={
        "signup_form": signup_form})
