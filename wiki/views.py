from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from markdown import markdown
import bleach

from . import forms
from .models import Page


def home_page(request):
    pages = Page.objects.all()
    # TODO: Render page authors along with pages
    return render(request, "wiki/home.html", context={
        "title": "Wikkie",
        "pages": pages})


def page(request, slug, version=None):
    try:
        page = Page.objects.get(slug=slug).best_version
    except Page.DoesNotExist:
        page = None

    if page:
        allowed_tags = bleach.ALLOWED_TAGS + ['p', 'h1', 'h2', 'h3']
        processed_page_content = bleach.clean(
            markdown(page.content),
            tags=allowed_tags
        )
        page.content = processed_page_content
        # TODO: Display author's name on the page decs page.

    return render(request, "wiki/page.html", context={
        "slug": slug,
        "page": page
    })


@login_required
def new_page(request):
    if request.method == 'GET':
        page_form = forms.NewPageForm()
    elif request.method == 'POST':
        page_form = forms.NewPageForm(request.POST)
        if page_form.is_valid():
            cleaned_form_data = page_form.cleaned_data
            page_form_instance_on_save = page_form.save(commit=False)
            page_form_instance_on_save.page = Page.objects.create(
                slug=cleaned_form_data['slug']
            )
            page_form_instance_on_save.author = request.user
            page_form_instance_on_save.save()
            return redirect("page", cleaned_form_data['slug'])

    return render(request, "wiki/edit_page.html", context={
        "page_title": "Create a new wiki page.",
        "page_form": page_form})


@login_required
def page_edit(request, slug):
    try:
        page = Page.objects.get(slug=slug)
        page_version = page.best_version
    except Page.DoesNotExist:
        page, page_version = None, None

    if request.method == 'GET':
        page_form = forms.PageForm(instance=page_version)
    elif request.method == 'POST':
        page_form = forms.PageForm(request.POST)
        if page_form.is_valid():
            page_form_instance_on_save = page_form.save(commit=False)
            page_form_instance_on_save.page = page or Page.objects.create(
                slug=slug
            )
            page_form_instance_on_save.save()
            return redirect("page", slug)

    return render(request, "wiki/edit_page.html", context={
        "page": page,
        "page_form": page_form})


def register_user(request):
    if request.method == 'GET':
        signup_form = forms.SignupForm()
    elif request.method == 'POST':
        signup_form = forms.SignupForm(request.POST)
        if signup_form.is_valid():
            form_data = signup_form.cleaned_data
            user_model = get_user_model()
            user_model.objects.create_user(**form_data)
            user = authenticate(**form_data)
            login(request, user)
            return redirect("home")

    return render(request, "registration/signup.html", context={
        "signup_form": signup_form})
