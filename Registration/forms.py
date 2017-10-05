from django import forms

from Configuration.countryConf import countries
from Configuration.stateConf import states
from General.models import CollegeExtraDetail, CollegeYear, Shift
from .models import Faculty, Subject, Student, Branch

branch_list = []

for branch in Branch.objects.all():
    branch_list.append(branch)

division_list = []

for div in CollegeExtraDetail.objects.filter(branch=Branch.objects.get(branch='Computer')).values_list('division',
                                                                                                       flat=True):
    division_list.append(div)

year_list = []

for year in CollegeYear.objects.all():
    year_list.append(year)

shift_list = []

for shift in Shift.objects.all():
    shift_list.append(shift)


class StudentForm(forms.ModelForm):
    current_country = forms.ChoiceField(
        choices=countries
    )
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    email = forms.EmailField()
    # state_choices = states[0].split(',')
    # current_state = forms.ChoiceField(choices=state_choices)
    # permanent_state = forms.ChoiceField(choices=state_choices)
    widgets = {
        'DOB': forms.DateInput(attrs={'class': 'datepicker'})
    }
    # Setting branch only as Comp and Mech fot VU
    branch = forms.ChoiceField(
        choices=[(i, i) for i in branch_list]
    )
    programme = forms.ChoiceField(choices=[('B.Tech', 'B.Tech'),
                                           ('M.Tech', 'M.Tech')])
    # branch = forms.ChoiceField(
    #     choices=[('Computer', 'Computer'), ('IT', 'IT'), ('EnTC', 'EnTC'), ('Mechanical', 'Mechanical'),
    #              ('Civil', 'Civil')])
    admission_type = forms.ChoiceField(
        choices=[('CAP-I', 'CAP-I'), ('CAP-II', 'CAP-II'), ('CAP-III', 'CAP-III'), ('CAPIV', 'CAPIV'),
                 ('Institute Level', 'Institute Level')]
    )
    shift = forms.ChoiceField(
        choices=[(i, i) for i in shift_list]
    )

    division = forms.ChoiceField(
        choices=[(i, i) for i in division_list]
    )
    year = forms.ChoiceField(
        choices=[(i, i) for i in year_list]
    )

    class Meta:
        model = Student

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        fields = '__all__'
        exclude = ['salary','user']

class FacultyForm(forms.ModelForm):
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    current_country = forms.ChoiceField(
        choices=countries
    )
    email = forms.EmailField()
    class Meta:
        model = Faculty
        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker'}),
            'teaching_from': forms.DateInput(attrs={'class': 'datepicker'})
        }
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    branch = forms.ChoiceField(
        choices=[('Computer', 'Computer'), ('IT', 'IT'), ('EnTC', 'EnTC'), ('Mechanical', 'Mechanical'),
                 ('Civil', 'Civil')])
    year = forms.ChoiceField(
        choices=[('FE', 'FE'), ('SE', 'SE'), ('TE', 'TE'), ('BE', 'BE'), ]
    )

    class Meta:
        model = Subject
        fields = '__all__'
