import json
from operator import attrgetter

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import dateutil.parser

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Exam.forms import ExamDetailForm
from Exam.models import ExamMaster, ExamSubject, ExamDetail, ExamGroupDetail, ExamGroupRoom, ExamSubjectRoom, \
    ExamSubjectStudentRoom, ExamGroup
from General.models import Semester, BranchSubject, CollegeYear, YearBranch, FacultySubject, Division, StudentDetail, \
    StudentSubject
from General.views import notify_users
from Registration.models import Branch, Student
from Registration.views import has_role
from Timetable.models import Room


def exam_register(request):
    class_active = "exam"
    if request.method == 'GET':
        return render(request, 'exam_register.html', {
            'class_active': class_active,

        })

    else:
        exam_name = request.POST.get('exam_name')
        ExamMaster.objects.create(exam_name=exam_name, start_date=datetime.date.today())
        context = {'success': "Successfully registered"}
        return render(request, 'exam_register.html', context)


def exam_detail(request):
    class_active = 'exam'
    if request.method == "GET":
        return render(request, 'exam_detail.html', {
            'class_active': class_active,
            'form': ExamDetailForm
        })
    else:
        form = ExamDetailForm(request.POST)
        if form.is_valid():
            exam_detail_obj = form.save()
            subjects = request.POST.getlist('subject')

            for each_subject in subjects:
                subject = BranchSubject.objects.get(is_active=True, year_branch=exam_detail_obj.year,
                                                    subject__short_form=each_subject).subject
                faculty_initials = request.POST.get(each_subject + '_faculty')

                faculty_obj = FacultySubject.objects.filter(faculty__initials=faculty_initials, is_active=True,
                                                            subject=subject)[0].faculty

                ExamSubject.objects.create(exam=exam_detail_obj, subject=subject, coordinator=faculty_obj,
                                           is_active=True)

            return render(request, 'set_exam_time.html', {
                'subjects': subjects,
                'exam_name': exam_detail_obj.exam.exam_name,
                'branch': exam_detail_obj.year.branch.branch,
                'exam_pk': exam_detail_obj.id,
            })
        else:
            return render(request, 'exam_detail.html', {
                'class_active': class_active,
                'form': form,
                'error': 'Not valid'
            })


def set_exam_time(request):
    user = request.user

    if has_role(user, 'faculty'):
        if request.method == 'POST':
            exam_pk = request.POST.get('exam_pk')
            exam_detail_obj = ExamDetail.objects.get(id=exam_pk)

            subjects = request.POST.getlist('subject')

            # Notify students about exam
            notification_type = 'general'
            message = 'Your ' + exam_detail_obj.exam.exam_name + ' exam has been scheduled from ' + \
                      exam_detail_obj.schedule_start_date.__str__() + ' to ' + exam_detail_obj.schedule_end_date.__str__() + \
                      ' for subjects ' + ", ".join(subjects)
            heading = 'Exam Schedule for ' + exam_detail_obj.exam.exam_name

            year_branch_obj = exam_detail_obj.year
            division = list(Division.objects.filter(is_active=True, year_branch=year_branch_obj))

            notify_users(notification_type=notification_type, message=message, heading=heading, division=division)

            # Add to examsubject
            user_obj = []
            for each_exam_subject in exam_detail_obj.examsubject_set.all():
                each_subject = each_exam_subject.subject.short_form

                exam_start_time = dateutil.parser.parse(request.POST.get('start_' + each_subject))
                exam_end_time = dateutil.parser.parse(request.POST.get('end_' + each_subject))

                each_exam_subject.start_datetime = exam_start_time
                each_exam_subject.end_datetime = exam_end_time

                each_exam_subject.save()
                # each_exam_subject.start_datetime

                # user_obj.append(faculty_obj.user)
                # Notify Faculty about exam
                notification_type = 'specific'
                message = 'You have been selected as Exam coordinator for ' + exam_detail_obj.exam.exam_name + ' exam which is scheduled from ' + \
                          exam_detail_obj.schedule_start_date.__str__() + ' to ' + exam_detail_obj.schedule_end_date.__str__() + \
                          ' for subject ' + each_subject
                heading = 'Exam Schedule for ' + exam_detail_obj.exam.exam_name

                # year_branch_obj = exam_detail_obj.year
                # division = list(Division.objects.filter(is_active=True, year_branch=year_branch_obj))

                # Notify Exam co-ordinator
                notify_users(notification_type=notification_type, message=message, heading=heading,
                             users_obj=[each_exam_subject.coordinator.user],
                             user_type='faculty')

            return redirect('/')


def get_subjects(request):
    if request.is_ajax():
        if request.method == "POST":
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            semester_obj = Semester.objects.get(pk=semester)
            # year_splitted = year.split(' ')
            # branch = year_splitted[0]
            # year = year_splitted[1]
            # branch_obj = Branch.objects.get(branch=branch)
            # year_obj = CollegeYear.objects.get(year=year)
            year_branch_obj = YearBranch.objects.get(pk=year)

            subjects = BranchSubject.objects.filter(year_branch=year_branch_obj, semester=semester_obj, is_active=True)

            subject_faculty_json = {}

            for each_subject in subjects:
                short_form = each_subject.subject.short_form
                facultys = set(FacultySubject.objects.filter(subject=each_subject.subject, is_active=True).values_list(
                    'faculty__initials', flat=True))
                subject_faculty_json[short_form] = list(facultys)

            return HttpResponse(json.dumps(subject_faculty_json))

        else:
            return HttpResponse("Not post")
    else:
        return HttpResponse('Not ajax')


def view_exam(request):
    user = request.user
    if has_role(user, 'student'):
        student_obj = user.student
        student_detail_obj = StudentDetail.objects.get(student=student_obj, is_active=True)
        year_branch_obj = student_detail_obj.batch.division.year_branch
        exam_objs = ExamDetail.objects.filter(is_active=True, year=year_branch_obj)
        exam_subjects = [list(each.examsubject_set.values_list('subject__short_form', flat=True)) for each in exam_objs]
        return render(request, 'view_exam.html', {
            'exams': exam_objs,
            'exam_subjects': exam_subjects
        })


def manage_exam(request):
    user = request.user
    class_active = "exam"
    if user.is_anonymous:
        return redirect('/login/')

    else:
        if has_role(user, 'faculty'):
            all_exams = ExamDetail.objects.all().order_by('-schedule_start_date')

            return render(request, 'manage_exam.html', {
                'class_active': class_active,
                'all_exams': all_exams
            })


def set_rooms(request):
    user = request.user
    if has_role(user, 'faculty'):
        if request.method == 'GET':
            all_exams = list(ExamDetail.objects.filter(is_active=True))
            done_exams = set([each.exam for each in ExamGroupDetail.objects.filter(is_active=True)])
            remaining = list(set(all_exams) - done_exams)
            print(remaining)
            branch_obj = Branch.objects.get(branch='Computer')
            available_rooms = Room.objects.filter(branch=branch_obj)
            return render(request, 'set_rooms.html', {
                'exams': remaining,
                'available_rooms': available_rooms
            })
        elif request.method == 'POST':
            all_exam_id = request.POST.getlist('exam')

            all_room_id = request.POST.getlist('room')



        else:
            return HttpResponse("Something went wrong")

    else:
        return HttpResponse('Access Denied')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def check_availability(request):
    if request.is_ajax():
        all_rooms = set(request.POST.getlist('room[]'))
        all_exams = request.POST.getlist('exam[]')

        print(all_exams)
        print(all_rooms)

        room_objs = [Room.objects.get(room_number=each) for each in all_rooms]
        exam_detail_objs = [ExamDetail.objects.get(pk=each) for each in all_exams]

        min_start_date_obj = min(exam_detail_objs, key=attrgetter('schedule_start_date'))

        max_end_date_obj = max(exam_detail_objs, key=attrgetter('schedule_end_date'))

        final = {}
        room_block = {}

        can_be_done = True

        # For displaying
        exam_json = {}

        for each_date in daterange(min_start_date_obj.schedule_start_date, max_end_date_obj.schedule_end_date):
            current_date_subjects = []
            # Below for loop is to get subjects for this date
            for each_exam in exam_detail_objs:
                all_subs = each_exam.examsubject_set.all()

                for each_sub in all_subs:
                    if each_sub.start_datetime.date() == each_date:
                        current_date_subjects.append(each_sub)

            student_subject_objs = []

            time_slots = set()

            # Get all time_slots fo that day
            for each_sub in current_date_subjects:
                # subject_obj = each_sub.subject
                # student_subject_objs.append(subject_obj.studentsubject_set.filter(is_active = True))
                pair = (each_sub.start_datetime, each_sub.end_datetime)
                time_slots.add(pair)
                all_rooms_for_current_slot = set(ExamSubjectRoom.objects.filter(exam_subject__start_datetime=pair[0],
                                                                                exam_subject__end_datetime=pair[
                                                                                    1]).values_list('room__room_number',
                                                                                                    flat=True))

                for each_room in all_rooms_for_current_slot:
                    if each_room in room_block:
                        room_block[each_room].append(pair)
                    else:
                        room_block[each_room] = [pair]

            for each_slot in time_slots:
                current_slot_subs = list(
                    filter(lambda x: x.start_datetime == each_slot[0] and x.end_datetime == each_slot[1],
                           current_date_subjects))
                students = list(StudentSubject.objects.filter(
                    subject__in=[each.subject for each in current_slot_subs], is_active=True))
                num_of_students = len(students)

                temp_student_dict = {}

                for each_student in students:
                    if each_student.subject_id in temp_student_dict:
                        temp_student_dict[each_student.subject_id].append(each_student)
                    else:
                        temp_student_dict[each_student.subject_id] = [each_student]

                grouped_students = []

                for subject_id, value in temp_student_dict.items():
                    grouped_students.extend(value)

                # To get available rooms
                all_available_rooms = []
                for each_room in all_rooms:
                    to_add = True
                    if each_room in room_block:
                        for sl in room_block[each_room]:
                            if (sl[0] <= each_slot[0] <= sl[1]) or (sl[1] <= each_slot[1] <= sl[1]):
                                to_add = False
                                break
                    if to_add:
                        all_available_rooms.append(each_room)

                single_capacity = sum(
                    Room.objects.get(room_number=each_room).capacity for each_room in all_available_rooms)
                print(single_capacity)
                print(num_of_students)
                if 2 * single_capacity < num_of_students:

                    print('Please select more rooms')
                    can_be_done = False
                    exam_json = {'type': 'Failure',
                                 'message': 'Please Select more rooms.'}
                    return HttpResponse(json.dumps(exam_json))
                elif single_capacity >= num_of_students:

                    # Schedule for all subjects in this slot
                    # for each_subject in current_slot_subs:
                    #     students = StudentSubject.objects.filter(subject=each_subject,is_active=True)
                    #     num = len(students)
                    counter = 0

                    final[each_slot] = {'exam_subject': current_slot_subs}
                    for each_room in all_available_rooms:
                        room_obj = Room.objects.get(room_number=each_room)
                        if each_room in room_block:
                            room_block[each_room].append(each_slot)
                        else:
                            room_block[each_room] = [each_slot]

                        if counter + room_obj.capacity > len(grouped_students):
                            final[each_slot][each_room] = grouped_students[counter:len(grouped_students)]
                        else:
                            final[each_slot][each_room] = grouped_students[counter:room_obj.capacity]
                        counter += room_obj.capacity

                        if counter > len(grouped_students):
                            break

                    print('Can be generated sequentially')
                else:
                    print('yet to write')
        exam_subject_student_room_to_create = []

        if can_be_done:
            print('can be done')
            exam_json = {'type': 'Success',
                         'message': 'Please view the schedule.'}
            for slot, values in final.items():
                exam_subject_objs = final[slot]['exam_subject']
                for room, students in final[slot].items():
                    if room != 'exam_subject':
                        for abc in students:
                            current_exam_subject = list(filter(lambda x: x.subject == abc.subject, exam_subject_objs))
                            if current_exam_subject.__len__() > 1:
                                return HttpResponse('Same exams are being scheduled at the same time.')
                            else:
                                current_exam_subject = current_exam_subject[0]
                                curr_exam_subject_room = ExamSubjectRoom.objects.create(
                                    exam_subject=current_exam_subject,
                                    room=Room.objects.get(
                                        room_number=room))

                                # if curr_exam_subject_room not in exam_subject_room_to_create:
                                #     exam_subject_room_to_create.append(curr_exam_subject_room)
                                exam_subject_student_room_to_create.append(
                                    ExamSubjectStudentRoom(student_subject=abc,
                                                           exam_subject_room=curr_exam_subject_room))
            # ExamSubjectRoom.objects.bulk_create(exam_subject_room_to_create)
            ExamSubjectStudentRoom.objects.bulk_create(exam_subject_student_room_to_create)

            # For sending notification
            student_subject_json = {}

            for each in exam_subject_student_room_to_create:
                branch = each.exam_subject_room.exam_subject.exam.year.branch.branch
                exam_name = each.exam_subject_room.exam_subject.exam.exam.exam_name
                date = each.exam_subject_room.exam_subject.start_datetime.strftime('%Y-%m-%d')
                start_time = each.exam_subject_room.exam_subject.start_datetime.strftime('%H:%M')
                end_time = each.exam_subject_room.exam_subject.start_datetime.strftime('%H:%M')
                time_slot = start_time + '-' + end_time
                student = each.student_subject.student.gr_number
                room = each.exam_subject_room.room.room_number

                if branch in exam_json:
                    if exam_name in exam_json[branch]:
                        if date in exam_json[branch][exam_name]:
                            if time_slot in exam_json[branch][exam_name][date]:
                                if room in exam_json[branch][exam_name][date][time_slot]:
                                    exam_json[branch][exam_name][date][time_slot][room].append(student)
                                else:
                                    exam_json[branch][exam_name][date][time_slot][room] = [student]
                            else:
                                exam_json[branch][exam_name][date][time_slot] = {}
                                exam_json[branch][exam_name][date][time_slot][room] = [student]

                        else:
                            exam_json[branch][exam_name][date] = {}
                            exam_json[branch][exam_name][date][time_slot] = {}
                            exam_json[branch][exam_name][date][time_slot][room] = [student]
                    else:
                        exam_json[branch][exam_name] = {}
                        exam_json[branch][exam_name][date] = {}
                        exam_json[branch][exam_name][date][time_slot] = {}
                        exam_json[branch][exam_name][date][time_slot][room] = [student]
                else:
                    exam_json[branch] = {}
                    exam_json[branch][exam_name] = {}
                    exam_json[branch][exam_name][date] = {}
                    exam_json[branch][exam_name][date][time_slot] = {}
                    exam_json[branch][exam_name][date][time_slot][room] = [student]

            return HttpResponse(json.dumps(exam_json))
        else:
            print('cannot be done')

    elif request.method=='POST':
        exam_group_pk = request.POST.get('exam_group')

        exam_group_obj = ExamGroup.objects.filter(pk=exam_group_pk)

        if exam_group_obj.__len__()<1:
            return HttpResponse('Not Found')

        exam_group_obj = exam_group_obj[0]

        exam_group_detail_objs = exam_group_obj.examgroupdetail_set.all()
        exam_detail_objs = [each.exam for each in exam_group_detail_objs]








@csrf_exempt
def android_types_of_exam(request):
    if request.method == 'POST':
        gr_number = request.POST.get('gr_number')
        student_obj = Student.objects.get(gr_number=gr_number)
        student_subjects = StudentSubject.objects.filter(student=student_obj, is_active=True)
        exams = ExamSubject.objects.filter(
            subject__in=[each_subejct for each_subejct in student_subjects]).values_list('exam__exam__exam_name')

        return HttpResponse(exams)


    else:
        return HttpResponse('Not a POST request')
