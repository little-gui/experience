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

