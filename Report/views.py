# import xlsxwriter
# from django.http import HttpResponse
# from django.shortcuts import render
#
# # Create your views here.
# from Registration.forms import StudentForm
# from Registration.models import Student
#
#
# def student_details(request):
#     if request.method == 'POST':
#         all_students = Student.objects.all()
#         workbook = xlsxwriter.Workbook('Students.xlsx')
#         worksheet = workbook.add_worksheet()
#
#         dark_gray = workbook.add_format()
#         dark_gray.set_bg_color('#b2aeae')
#         dark_gray.set_border(1)
#
#         light_gray = workbook.add_format()
#         light_gray.set_border(1)
#         light_gray.set_bg_color('#f1eacf')
#         fields = request.POST.getlist('fields')
#         col = 1
#         row = 1
#         i = 0
#
#         for each_field in fields:
#             worksheet.write(row, col + i, each_field)
#             i += 1
#
#         col = 1
#         row = 3
#         i_row = 0
#         i_col = 0
#
#         for each_student in all_students:
#             i_col = 0
#             for each_field in fields:
#                 try:
#                     if each_field == 'email':
#                         worksheet.write(row + i_row, col + i_col, each_student.user.email, light_gray if i_row%2 ==0 else dark_gray)
#                     elif each_field == 'division':
#                         worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().batch.division.division,
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                     elif each_field == 'year':
#                         worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().batch.division.year.year,
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                     elif each_field == 'batch':
#                         worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().batch.batch_name,
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                     elif each_field == 'branch':
#                         worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().batch.division.branch.branch,
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                     elif each_field == 'roll_number':
#                         worksheet.write(row + i_row, col + i_col, each_student.studentdetail_set.first().roll_number,
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                     else:
#                         worksheet.write(row + i_row, col + i_col, getattr(each_student, each_field),
#                                         light_gray if i_row % 2 == 0 else dark_gray)
#                 except:
#                     pass
#                 i_col += 1
#
#             i_row += 1
#         workbook.close()
#
#         return render(request, 'student_details.html', {'fields': StudentForm,
#                                                         'success': 'Done'})
#
#     elif request.method == 'GET':
#         return render(request, 'student_details.html', {
#             'fields': StudentForm,
#         })
