from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Registration.models import Faculty
from Research.forms import ResearchForm
from Research.models import Paper


def handle_uploaded_file(file):
    pass


def enter_paper(request):
    if request.method == "POST":
        print(request.POST)
        form = ResearchForm(request.POST, request.FILES)

        if form.is_valid():
            paper = form.save(commit=False)
            faculty = Faculty.objects.get(user=User.objects.get(first_name=form.cleaned_data.get('faculty_name')))
            paper.faculty = faculty
            paper.save()

            # paper = Paper.objects.create(faculty=faculty, publication_year=form.cleaned_data.get('publication_year'),
            #                              publication_date=form.cleaned_data.get('publication_date'),
            #                              type=form.cleaned_data.get('type'), title=form.cleaned_data.get('title'),
            #                              conference_name=form.cleaned_data.get('conference_name'),
            #                              conference_type=form.cleaned_data.get('conference_type'),
            #                              peer_reviewed=form.cleaned_data.get('peer_reviewed'),
            #                              publication_medium=form.cleaned_data.get('publication_medium'),
            #                              isbn=form.cleaned_data.get('isbn'), domain=form.cleaned_data.get('domain'),
            #                              funds_received_from_college=form.cleaned_data.get(
            #                                  'funds_received_from_college'),
            #                              other_info=form.cleaned_data.get('other_info'),
            #                              )
            return HttpResponse("Saved")

        else:
            print(form.errors)
            return render(request, 'research.html', {
                'form': form
            })

    else:
        form = ResearchForm()
        faculty = []
        for i in Faculty.objects.all():
            faculty.append(i)
        return render(request, 'research.html', {
            'form': form,
            'faculty': faculty
        })
