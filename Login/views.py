from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

dict_array = [{
    'userType': 'Student',
    'year': 'TE',
    'branch': 'Computer',
    'division': 'B',

},

    {
        'userType': 'Faculty'
    }]

counter = 0


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
                global counter
                counter += 1
                counter %= 2
                print(str(dict_array[counter]))
                return HttpResponse(str(dict_array[1]))
            else:
                return HttpResponse("{'userType': 'null'}")
        except:
            return HttpResponse("Something is wrong")
    print("inside android")
    return HttpResponse("got")
