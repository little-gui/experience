from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404

from oportunidades.models import Login
from utils.decorators import render_to


@render_to('oportunidades.html')
def index(request):
    return {}

@render_to('novo.html')
def new(request):
    return {}

@render_to('mural.html')
def dashboard(request):
    return {}

@render_to('setup.html')
def setup(request, code):
    login = get_object_or_404(Login.objects, code=code)
    user = login.user

    if request.method == "POST":
        password = request.POST.get('password')
        if password == '' or password != request.POST.get('confirm_password'):
            return  {'code': code, 'user': user, 'error': True}
        else:
            user.set_password(password)
            user.save()
            return redirect('oportunidades_admin')

    return {'code': code, 'user': user}

@render_to('admin.html')
def admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('oportunidades_empregados')
        else:
            return {'success': False}

    return {}

@render_to('empregados.html')
def empregados(request):
    return {}

