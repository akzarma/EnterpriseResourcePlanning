import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.utils import timezone

from Dashboard.models import SpecificNotification, GeneralStudentNotification, GeneralFacultyNotification

from General.models import CollegeYear, Shift, BranchSubject, YearBranch, StudentDetail, Semester
from Registration.models import Branch


# notification_type:Either 'specific' or 'general'  (Is case sensitive)

def notify_users(notification_type: str, message: str, heading: str, users_obj: list = None, type: str = 'View',
                 user_type: str = 'Student',
                 action: str = "Nothing for now",
                 division: list = None, for_batch: bool = False, batch: list = None, branch: list = None):
    current_time = timezone.now()
    if notification_type == 'specific':
        notification_objs = []
        for each_user in users_obj:
            notification_objs.append(
                SpecificNotification(user=each_user, action=action, notification=message, heading=heading,
                                     datetime=current_time, type=type))

        SpecificNotification.objects.bulk_create(notification_objs)
    elif notification_type == "general":
        notification_objs = []
        if user_type == 'Student':

            if for_batch:
                # if for_batch:
                for each_batch in batch:
                    notification_objs.append(
                        GeneralStudentNotification(action=action, heading=heading,
                                                   datetime=current_time, notification=message, type=type,
                                                   for_batch=for_batch, batch=each_batch))
            else:
                for each_division in division:
                    notification_objs.append(
                        GeneralStudentNotification(division=each_division, action=action, heading=heading,
                                                   datetime=current_time, notification=message, type=type,
                                                   for_batch=for_batch))
            GeneralStudentNotification.objects.bulk_create(notification_objs)
        elif user_type == 'Faculty':
            for each_branch in branch:
                notification_objs.append(GeneralFacultyNotification(action=action, heading=heading,
                                                                    datetime=current_time, notification=message,
                                                                    type=type, branch=each_branch))
            GeneralFacultyNotification.objects.bulk_create(notification_objs)
        print("General Notification")

    else:
        print("Should not go here:General\\views")


def general(request):
    # branch = Branch.objects.all()
    # year = CollegeYear.objects.all()
    # #
    # # for each_year in year:
    # #     for each_branch in branch:
    # #         YearBranch.objects.create(branch=each_branch, year=each_year)
    # year_branch = YearBranch.objects.filter(branch=branch, year=year)
    #
    # for each in year_branch:
    #     CollegeExtraDetail.objects.create(year_branch=each, division='A', shift=Shift.objects.get(shift=1))
    #     CollegeExtraDetail.objects.create(year_branch=each, division='B', shift=Shift.objects.get(shift=1))
    #     CollegeExtraDetail.objects.create(year_branch=each, division='C', shift=Shift.objects.get(shift=2))

    # college_detail = CollegeExtraDetail.objects.get(branch=Branch.objects.get(branch="Computer"),
    #                                                 year=CollegeYear.objects.get(year="TE"),
    #                                                 division="B",
    #                                                 shift=Shift.objects.get(shift=1))
    # print(college_detail)
    # all_branch_subjects = BranchSubject.objects.all()
    # for each in all_branch_subjects:
    #     each.college_detail = college_detail
    #     each.save()

    # for each in StudentDetail.objects.all():
    #     sem = Semester.objects.get(semester=2)
    #     each.semester = sem
    #     each.save()
    return HttpResponse("DONE")
