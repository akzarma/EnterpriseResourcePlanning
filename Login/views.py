from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def login_user(request):
    print("login user")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/dashboard/student/')
        else:
            return HttpResponseRedirect('/login/')
    return render(request, 'login.html')


@csrf_exempt
def login_android(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(username)
            print(password)
            if user:
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        except:
            return HttpResponse("Something is wrong")
    print("inside android")
    return HttpResponse("got")
