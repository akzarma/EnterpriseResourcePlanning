from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Research.forms import PublicationForm
from Research.models import Paper


def enter_paper(request):
    user = request.user
    if not user.is_anonymous:
        if user.role == 'Faculty':
            if request.method == "POST":
                form = PublicationForm(request.POST,request.FILES)
                print(form.errors)
                # form.fields['faculty'] = user.faculty

                if form.is_valid():

                    paper_object = form.save(commit=False)
                    paper_object.faculty = user.faculty
                    paper_object.save()
                    return render(request, 'dashboard_faculty.html', {'success': 'Paper successfully submitted'})

                else:
                    return render(request, 'dashboard_faculty.html', {'error':'Form not valid'})
            else:
                form = PublicationForm()
                return render(request, "enter_publication.html", {'form': form})
        else:
            return HttpResponse('Not faculty')
    else:
        return HttpResponseRedirect('/login/')
