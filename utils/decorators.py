"""
Decorators for easing function views usage.

Usage:

@render_to('path/to/template.html')
def my_cool_view(request):
    my_var = 'Cool!'
    return {'myvar':myvar}
"""
from django.core.urlresolvers import resolve

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.http import HttpResponse
from django.template import RequestContext, loader


def is_ajax(function):
    def verify(request, *args, **kargs):
        #if request.is_ajax():
        if True:
            output = function(request, *args, **kargs)

            if isinstance(output, dict) or isinstance(output, list):
                response = HttpResponse(dumps(output), mimetype="application/javascript")

                if 'Vary' in response:
                    del response['Vary']

                response['Expires'] = 'Mon, 26 Jul 1997 05:00:00 GMT'
                response['Pragma'] = 'no-cache'
                response['Cache-Control'] = 'no-cache, must-revalidate'

                return response
            else:
                return output
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    return verify

def render_to(tpl, *args, **kw):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, dict):
                return render_to_response(tpl, output, context_instance=RequestContext(request))
            else:
                return output
        return wrapper
    return renderer

