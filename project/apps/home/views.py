# coding=UTF-8
from datetime import datetime

from geopy.geocoders import GoogleV3
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.gis import geos, measure
from django.contrib.gis.geoip import GeoIP
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db import IntegrityError
from ipware.ip import get_ip

from utils.decorators import render_to, is_ajax
from project.apps.home.models import Article
from project.settings import formats


@render_to('home/index.html')
def index(request):
    ip = get_ip(request)
    now = datetime.now()
    if ip is not None:
        if 'location' not in request.session:
            info = find_by_ip(ip)
            request.session['location'] = info
        else:
            info = request.session['location']

        current_point = geos.fromstr("POINT(%s %s)" % (info['longitude'], info['latitude']))
        
        distance_from_point = {'km': 5000}
        articles = Article.gis.filter(by_when__gt=now, location__distance_lte=(current_point, measure.D(**distance_from_point)))
        articles = articles.distance(current_point).order_by('distance', 'by_when')
    else:
        articles = Article.objects.filter(by_when__gt=now, )[:10]

    # assert False, articles
    # assert False, create(request)['full_address']

    return { 'articles': articles }


@login_required
@render_to('news/create.html')
def news_create(request):
    if request.method == 'POST':
        article = Article()
        article.by_when = datetime.now()
        for date_format in formats:
            try:
                article.by_when = datetime.strptime('%s %s' % (request.POST['date'], request.POST.get('hour', '12:00')), date_format)
            except ValueError:
                continue

        geocoder = GoogleV3()
        try:
            _, latlon = geocoder.geocode(request.POST.get('address'))
        except (URLError, GQueryError, ValueError):
            pass
        else:
            point = "POINT(%s %s)" % (latlon[1], latlon[0])
            article.location = geos.fromstr(point)
            article.address = request.POST.get('address')

        if len(request.POST.get('address', '').split(',')) != 2:
            return { 'error': True, 'message': 'Digite corretamente on endereço (Cidade, Logradouro)' }
        article.city = request.POST.get('address', '').split(',')[0]
        article.title = request.POST.get('title')
        article.description = request.POST.get('description')
        article.user = request.user
        article.save()

    ip = get_ip(request)
    location = ''
    if ip is not None:
        if 'location' not in request.session:
            info = find_by_ip(ip)
            request.session['location'] = info
        else:
            info = request.session['location']
        location = info['full_address']

    return { 'location': location, 'success': True, 'message': 'Acontecimento incluído com sucesso' }


def find_by_ip(ip):
    # reverse = "long, lat"
    g = GeoIP()
    info = g.city(ip)
    if info == None or ip == '192.168.1.10' or ip == '127.0.0.1':
        longitude, latitude = (-29.9193163, -51.1789279)
    else:
        longitude, latitude = info['longitude'], info['latitude']

    reverse = "%d, %d" % (longitude, latitude)
    geocoder = GoogleV3()
    reverse = geocoder.reverse(reverse)

    city, street = '', ''
    for address in reverse[0].raw['address_components']:
        for address_type in address['types']:
            if address_type == 'route':
                street = address['long_name']

            if address_type == 'locality':
                city = address['long_name']

    full_address = ', '.join([city, street])
    full_address, (lon, lat) = geocoder.geocode(full_address)

    return { 'full_address': full_address, 'city': city, 'street': street, 'longitude': lon, 'latitude': lat }

@render_to("auth/login.html")
def login(request):
    if request.method == 'POST':
        if int(request.POST.get('create', 0)) == 1:
            try:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'])
            except ValueError:
                return { 'error': True, 'message': 'Usuário não pode ser vazio.', 'create': True }
            except IntegrityError:
                return { 'error': True, 'message': 'Usuário já existe.', 'create': True }
            user.set_password(request.POST['password'])
            user.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_active:
                django_login(request, user)
                return redirect('home')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('home')
                else:
                    return { 'warning': True, 'message': 'Usuário inativo.' }
            else:
                return { 'error': True, 'message': 'Usuário ou senha incorretos.' }
    return {}

@is_ajax
def logout(request):
    django_logout(request)
    return redirect('home')

@is_ajax
def point_up(request, article_id):
    Article.objects.filter(id=article_id).update(points=F('points')+1)
    return redirect('home')
