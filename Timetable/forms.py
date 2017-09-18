from django import forms

# from Registration.models import Subject#,Branch
# from .models import Room, TimeTable#, Division
from Registration.models import Subject#, Branch
from Timetable.models import Timetable

room_list = []
#
# for room in Room.objects.filter(branch=0):#Branch.objects.get(branch='Computer')):
#     room_list.append(room)


faculty_list = []

# for faculty in Division.objects.filter(subject=Subject.objects.filter(branch='Computer')):
#     faculty_list.append(faculty)

print(faculty_list)

subject_list = []

# for sub in Subject.objects.filter(branch=Branch.objects.get(branch='Computer')):
#     subject_list.append(sub)


class TimetableForm(forms.ModelForm):
    faculty = forms.ChoiceField(
        choices=[(i, i) for i in faculty_list],
        label='Faculty'
    )

    subject = forms.ChoiceField(
        choices=[(i, i) for i in subject_list],
        label='Subject'
    )
    #
    # division = forms.ChoiceField(
    #     choices=[(division_list[i], division_list[i]) for i in division_list],
    #     label='Division'
    # )

    room = forms.ChoiceField(
        choices=[(i, i) for i in room_list]
    )

    class Meta:
        model = Timetable

        fields = '__all__'
