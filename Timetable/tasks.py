from collections import OrderedDict

import os

import firebase_admin
import xlsxwriter
from celery import shared_task
from firebase_admin import credentials, db

from General.models import CollegeYear, BranchSubject, CollegeExtraDetail, Batch
from Registration.models import Faculty, Branch
from Sync.function import write_to_firebase
from Timetable.models import Time, Timetable, Room


# from Timetable.views import get_excel


@shared_task
def save_timetable_celery(post):
    branch_obj = Branch.objects.get(branch='Computer')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    branch = Branch.objects.get(branch='Computer')
    full_timetable = list(Timetable.objects.filter(branch_subject__college_detail__branch=branch))

    for i in post:
        if i.__contains__('_room_'):
            splitted = i.split('_room_')
            token = splitted[1].split('_')
            time = token[0].split('-')
            start_time = int(time[0].split(':')[0] + time[0].split(':')[1])
            end_time = int(time[1].split(':')[0] + time[1].split(':')[1])

            subject = splitted[0] + '_subject_' + splitted[1]
            subject_short_name = post.get(subject)

            division = token[1]

            day = days[int(token[2]) - 2]

            year = token[3]

            faculty_initials = post.get(splitted[0] + '_teacher_' + splitted[1])

            room_number = post.get(i)

            time = Time.objects.get(starting_time=start_time, ending_time=end_time)
            # day = day
            # subject = Subject.objects.get(
            #     short_form=subject_short_name)  # this has to be changed, should  not get subject with  short_name directly

            # branch = Branch.objects.get(branch='Computer')
            year = CollegeYear.objects.get(year=year)
            college_detail = CollegeExtraDetail.objects.filter(branch=branch, year=year)
            branch_subject = BranchSubject.objects.get(year_branch=college_detail[0],
                                                       subject__short_form=subject_short_name)
            # room = Room.objects.get(room_number=room_number, branch=branch_subject.branch,lab=i)

            faculty = Faculty.objects.get(
                initials=faculty_initials)  # this has to be changed, should not get only with initials. Use faculty_subject_set for that

            division = CollegeExtraDetail.objects.get(division=division, branch=branch_subject.branch,
                                                      year=branch_subject.year)

            if len(token) < 5:  # theory
                timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                     is_practical=False)
                room = Room.objects.get(room_number=room_number, branch=branch_subject.branch, lab=False)

                if timetable:
                    full_timetable.remove(timetable[0])
                    if not timetable[0].faculty == faculty:
                        timetable[0].faculty = faculty
                    if not timetable[0].branch_subject == branch_subject:
                        timetable[0].branch_subject = branch_subject
                    if not timetable[0].room == room:
                        timetable[0].room = room

                    timetable[0].save()
                else:
                    timetable = Timetable(room=room, faculty=faculty, branch_subject=branch_subject, time=time,
                                          day=day, division=division,
                                          is_practical=False)

                    timetable.save()

            else:  # practical
                # batch = token[4]
                batch = Batch.objects.get(division=division, batch_name=token[4])

                timetable = Timetable.objects.filter(time=time, day=day, division=division,
                                                     is_practical=True,
                                                     batch=batch)
                room = Room.objects.get(room_number=room_number, branch=branch_subject.branch, lab=True)

                if timetable:
                    full_timetable.remove(timetable[0])

                    if not timetable[0].faculty == faculty:
                        timetable[0].faculty = faculty
                    if not timetable[0].branch_subject == branch_subject:
                        timetable[0].branch_subject = branch_subject
                    if not timetable[0].room == room:
                        timetable[0].room = room

                    timetable[0].save()
                else:
                    timetable = Timetable(room=room, faculty=faculty, branch_subject=branch_subject, time=time,
                                          day=day, division=division,
                                          is_practical=True, batch=batch)  # batch bhi add karna hai.

                    timetable.save()

    # to_json(request)

    Timetable.objects.filter(id__in=[i.id for i in full_timetable]).delete()

    #
    # write_to_firebase(answer, 'Student')
    # write_to_firebase(faculty_json, 'Faculty')

    ays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    branch_obj = Branch.objects.get(branch='Computer')
    full_timetable = Timetable.objects.filter(branch_subject__college_detail__branch=branch_obj)

    answer = OrderedDict()

    for each in sorted(full_timetable, key=lambda x: (days.index(x.day), x.division.year.number, x.time.starting_time)):
        year = each.branch_subject.year.year
        branch = each.branch_subject.branch.branch

        division = each.division.division

        day = each.day

        time = each.time

        faculty = each.faculty.initials

        room = each.room.room_number
        subject = each.branch_subject.subject.short_form

        if day in answer:
            if year in answer[day]:
                if division in answer[day][year]:
                    if time in answer[day][year][division]:
                        OrderedDict()
                    else:
                        answer[day][year][division][time] = OrderedDict()
                else:
                    answer[day][year][division] = OrderedDict()
                    answer[day][year][division][time] = OrderedDict()
            else:
                answer[day][year] = OrderedDict()
                answer[day][year][division] = OrderedDict()
                answer[day][year][division][time] = OrderedDict()
        else:
            answer[day] = OrderedDict()
            answer[day][year] = OrderedDict()
            answer[day][year][division] = OrderedDict()
            answer[day][year][division][time] = OrderedDict()

        is_practical = each.is_practical

        if is_practical:
            batch = each.batch.batch_name
            if 'is_practical' in answer[day][year][division][time]:
                {}
            else:
                answer[day][year][division][time] = {
                    'is_practical': is_practical
                }

            answer[day][year][division][time][batch] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
            }


        else:
            answer[day][year][division][time] = {
                'faculty': faculty,
                'room': room,
                'subject': subject,
                'is_practical': is_practical
            }

    answer = OrderedDict(sorted(answer.items(), key=lambda x: days.index(x[0])))

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 1

    year_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    subject_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#f0bfff'})
    time_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'color': 'red'})

    practical_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#77abff'})

    full_time = [each.__str__() for each in sorted(Time.objects.all(), key=lambda x: x.starting_time)]

    for each_day in answer.items():

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'red'})

        row = 1
        temp = col

        # each_year_sorted = [each[0] for each in each_day[1].items()]

        for each_year in each_day[1].items():
            for each_division in each_year[1].items():
                worksheet.merge_range(row, temp, row, temp + 1, each_year[0] + each_division[0], year_format)

                each_division_sorted = OrderedDict(sorted(each_division[1].items(), key=lambda x: x[0].starting_time))
                row = 2
                temp_row = row
                for each_time in each_division_sorted.items():

                    temp_row = full_time.index(each_time[0].__str__()) * 8 + row

                    if not each_time[1]['is_practical']:
                        worksheet.merge_range(temp_row, temp, temp_row + 3, temp, str(each_time[1]['room']),
                                              subject_format)
                        worksheet.merge_range(temp_row, temp + 1, temp_row + 3, temp + 1, str(each_time[1]['faculty']),
                                              subject_format)

                        worksheet.merge_range(temp_row + 4, temp, temp_row + 7, temp + 1, each_time[1]['subject'],
                                              subject_format)
                        # temp_row += 8

                    else:
                        for each_key in sorted(each_time[1].keys()):
                            if not each_key == 'is_practical':
                                worksheet.write(temp_row, temp, each_key, practical_format)
                                worksheet.write(temp_row, temp + 1, each_time[1][each_key]['subject'], practical_format)
                                worksheet.write(temp_row + 1, temp, each_time[1][each_key]['room'], practical_format)
                                worksheet.write(temp_row + 1, temp + 1, each_time[1][each_key]['faculty'],
                                                practical_format)
                                temp_row += 2

                temp += 2
                row = 1

        row = 0
        worksheet.merge_range(0, col, 0, temp - 1, each_day[0], merge_format)
        col = temp

    row_offset = 2
    col_offset = 0

    row = 0
    col = 0

    worksheet.write(row, col, 'Time')

    for each_time in full_time:
        worksheet.merge_range(row + row_offset, col + col_offset, row + row_offset + 7, col + col_offset,
                              each_time, time_format)
        worksheet.set_column(col + col_offset, col + col_offset, len(str(each_time)))
        row += 8

    workbook.close()

    return 'Done bro'
