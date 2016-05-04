"""experience URL Configuration

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
from django.views import static
from django.conf import settings
from django.contrib import admin

from geolocation import views as geolocation_views
from twitterbot import views as twitterbot_views
from oportunidades import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="oportunidades_index"),
    url(r'^novo/?$', views.new, name="oportunidades_new"),
    url(r'^mural/?$', views.dashboard, name="oportunidades_dashboard"),
    url(r'^admin/?$', views.admin, name="oportunidades_admin"),
    url(r'^setup/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/?$', views.setup, name="oportunidades_setup"),
    url(r'^empregados/?$', views.empregados, name="oportunidades_empregados"),
    
    url(r'^geolocation/?$', geolocation_views.index, name="geolocation_index"),
    url(r'^twitter/?$', twitterbot_views.index, name="twitterbot_index"),
    
    url(r'^(?P<path>.*)$', static.serve, {'document_root': settings.BASE_DIR, 'show_indexes': True})
]
