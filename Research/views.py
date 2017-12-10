from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Research.forms import PublicationForm
from Research.models import Paper


def enter_paper(request):
    if request.method == "POST":
        form = PublicationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponse("Saved")
    else:
        form = PublicationForm()
        return render(request, "enter_publication.html", {'form': form})
