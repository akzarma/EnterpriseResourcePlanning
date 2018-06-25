
from Login.views import login_user


def home(request):
    return login_user(request)

