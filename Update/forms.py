from django import forms

from Configuration.countryConf import countries
from Configuration.stateConf import states
from Registration.models import Faculty, Subject, Student



class StudentUpdateForm(forms.ModelForm):
    current_country = forms.ChoiceField(
        choices=countries
    )
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    # state_choices = states[0].split(',')
    caste_type = forms.CharField(disabled=True)
    # current_state = forms.ChoiceField(choices=state_choices)
    # permanent_state = forms.ChoiceField(choices=state_choices)

    # Setting branch only as Comp and Mech fot VU
    DOB = forms.CharField(disabled=True)
    branch = forms.ChoiceField(
        choices=[('Computer', 'Computer'),
                 ('Mechanical', 'Mechanical')], disabled=True
    )
    gr_number = forms.CharField(disabled=True)
    programme = forms.ChoiceField(choices=[('B.Tech', 'B.Tech'),
                                           ('M.Tech', 'M.Tech')], disabled=True)
    # branch = forms.ChoiceField(
    #     choices=[('Computer', 'Computer'), ('IT', 'IT'), ('EnTC', 'EnTC'), ('Mechanical', 'Mechanical'),
    #              ('Civil', 'Civil')])
    admission_type = forms.ChoiceField(
        choices=[('CAP-I', 'CAP-I'), ('CAP-II', 'CAP-II'), ('CAP-III', 'CAP-III'), ('CAPIV', 'CAPIV'),
                 ('Institute Level', 'Institute Level')], disabled=True
    )
    shift = forms.ChoiceField(
        choices=[('1', 'First-Shift'), ('2', 'Second-Shift')], disabled=True
    )

    class Meta:
        model = Student

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        fields = '__all__'
