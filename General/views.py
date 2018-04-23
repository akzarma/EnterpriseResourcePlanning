from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from General.models import CollegeExtraDetail, CollegeYear, Shift, BranchSubject, YearBranch
from Registration.models import Branch



def general(request):
    branch = Branch.objects.all()
    year = CollegeYear.objects.all()
    #
    # for each_year in year:
    #     for each_branch in branch:
    #         YearBranch.objects.create(branch=each_branch, year=each_year)
    year_branch = YearBranch.objects.filter(branch=branch, year=year)

    for each in year_branch:
        CollegeExtraDetail.objects.create(year_branch=each, division='A', shift=Shift.objects.get(shift=1))
        CollegeExtraDetail.objects.create(year_branch=each, division='B', shift=Shift.objects.get(shift=1))
        CollegeExtraDetail.objects.create(year_branch=each, division='C', shift=Shift.objects.get(shift=2))




    # college_detail = CollegeExtraDetail.objects.get(branch=Branch.objects.get(branch="Computer"),
    #                                                 year=CollegeYear.objects.get(year="TE"),
    #                                                 division="B",
    #                                                 shift=Shift.objects.get(shift=1))
    # print(college_detail)
    # all_branch_subjects = BranchSubject.objects.all()
    # for each in all_branch_subjects:
    #     each.college_detail = college_detail
    #     each.save()
    return HttpResponse("DONE")