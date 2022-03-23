from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, \
    permission_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import requests
import json

from .models import *
from .forms import *

def index(request):
    html = '''<html>
    <head><title>CS Thirdparty Site</title></head>
    <body>
        <h1>CS Thirdparty Site</h1>
        <p><a href="http://10.50.0.2/">Go to Coffeeshop (HTTP)</a></p>
        <p><a href="https://10.50.0.2/">Go to Coffeeshop (HTTPS)</a></p>
        </body>
    </html>
    '''
    return HttpResponse(html, content_type="text/html")


@require_http_methods(["GET"])
@csrf_exempt
def youhavewon(request):

    context = {}
    return render(request, 'csthirdparty/youhavewon.html', context)

# this version is for browsers that implement the new cookie recommendation of
# defaulting SameSite to None and requiring Secure.  For these browsers, the above
# view will not work.
@require_http_methods(["GET"])
@csrf_exempt
def youhavewonssl(request):

    context = {}
    return render(request, 'csthirdparty/youhavewonssl.html', context)

def iframe(request):

    context = {}
    return render(request, 'csthirdparty/iframe.html', context)


def cookies(request, cookie):
    try:
        cookies = Cookies(cookies=cookie, add_date=datetime.now())
        cookies.save()
    except Exception as e:
        print(e)
    html = '''<html>
    <head><title>Coffeeshop</title></head>
    <body></body>
    </html""
    '''
    return HttpResponse(html, content_type="text/html")


@require_http_methods(["GET"])
def gettest(request):
    return JsonResponse({'status': 'ok'})


@require_http_methods(["GET"])
def credtest(request):
    response = JsonResponse({'status': 'ok', 'cookies': str(request.COOKIES)})
    response.set_cookie('corstest', 'ivebeenset', samesite='None')
    return response


@require_http_methods(["POST"])
@csrf_exempt
def posttest(request):
    try:
        json_data = json.loads(request.body)
        value = json_data['value']
        # value = request.POST["value"]
        postdata = PostTest(value=value, add_date=datetime.now())
        postdata.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'fail'})


# OAuth callback that just send the code in a JSON
def oauthcallback(request):
    context = {}
    return JsonResponse({'code': request.GET['code']})
