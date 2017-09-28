"""splatnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from . import views, settings

urlpatterns = [
	url(r'^post/?$', views.PostEndpoint),
	url(r'^$', views.Index, name='Index'),
	url(r'^(?P<PId>[0-9]+)$', views.PlayerIndex, name='PlayerIndex'),
	url(r'^(?P<PId>[0-9]+)/(?P<session>[0-9]+)$', views.SessionSummary, name='SessionSummary'),
	url(r'^admin/', admin.site.urls),
]
