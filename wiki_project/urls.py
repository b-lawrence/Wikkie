"""wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
import wiki.views
from wiki.forms import LoginForm
from django.contrib.auth import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', wiki.views.home_page, name="home"),
    url(r'^new$', wiki.views.new_page, name="new_page"),
    url(r'^login$',
        views.login, {
            'template_name': 'registration/login.html',
            'authentication_form': LoginForm
        }, name="login"),
    url(r'^register$', wiki.views.register_user, name="register"),
    url(r'^([\w,-]+)$', wiki.views.page, name="page"),
    url(r'^([\w,-]+)/(\d+)$', wiki.views.page, name="page_version"),
    url(r'^([\w,-]+)/edit$', wiki.views.page_edit, name="page_edit"),
]
