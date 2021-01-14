import json

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect

from .decorators import locker
from .services import shorten_url_service
from utils import http_response


@ensure_csrf_cookie
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html', {})


@csrf_protect
@require_http_methods(['POST'])
@locker
def create(request):
    body = json.loads(request.body)
    scheme = request.is_secure() and 'https' or 'http'
    new_url = shorten_url_service.create_url(body.get('ori_url', ''), scheme)
    return http_response.json_response_success({'new_url': new_url})


@require_http_methods(['POST'])
def show_url(request):
    body = json.loads(request.body)
    url = shorten_url_service.get_original_url(body.get('ori_url', ''))
    return http_response.json_response_success({'ori_url': url})


@csrf_protect
@require_http_methods(['GET'])
@locker
def redirect_shorten_url(request, uri, *args, **kwargs):
    url = shorten_url_service.get_original_url(request.build_absolute_uri(uri))
    return redirect(url)
