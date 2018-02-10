from django import forms

from Configuration.countryConf import countries
from Configuration.stateConf import states
from General.models import CollegeExtraDetail, CollegeYear, Shift, Semester, FacultySubject
from .models import Faculty, Subject, Student, Branch

semester_list = Semester.objects.all()

branch_list = Branch.objects.all()

subject_list = Subject.objects.all()

faculty_list = Faculty.objects.all()

division_list = CollegeExtraDetail.objects.filter(branch=Branch.objects.get(branch='Computer'))

year_list = CollegeYear.objects.all()

shift_list = Shift.objects.all()


class FacultySubjectForm(forms.ModelForm):
    faculty = forms.ChoiceField(
        choices=[(i.pk, i.initials) for i in faculty_list]
    )

    subject = forms.ChoiceField(
        choices=[(i.pk, i.short_form) for i in subject_list]
    )

    division = forms.ChoiceField(
        choices=[(i.pk, i) for i in division_list]
    )

    def __init__(self, *args, **kwargs):
        super(FacultySubjectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = FacultySubject
        fields = '__all__'
        exclude = ['faculty', 'subject', 'division']


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
        choices=set([(i.division, i.division) for i in division_list])

    )
    year = forms.ChoiceField(
        choices=[(i, i) for i in year_list]
    )

    def __init__(self,*args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field is not 'DOB':
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Student
        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker form-control'}),
        }
        fields = '__all__'
        exclude = ['salary', 'user']


class FacultyForm(forms.ModelForm):
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    current_country = forms.ChoiceField(
        choices=countries
    )
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['DOB', 'teaching_form']:
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Faculty
        widgets = {
            # 'DOB': forms.DateInput(attrs={'class': 'datepicker'}),
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

    semester = forms.ChoiceField(
        choices=[(i, i) for i in semester_list]
    )

    is_practical = forms.BooleanField(required=False)

    class Meta:
        model = Subject
        fields = '__all__'
