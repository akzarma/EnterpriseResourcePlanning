from django import forms

from General.models import StudentInternship
from Internship.models import Internship
from Registration.models import Branch


class StudentInternshipForm(forms.ModelForm):
    # branch should be passed as a parameter in form
    internship = forms.ChoiceField(
        choices=[(i.pk, i) for i in Internship.objects.filter(branch=Branch.objects.get(branch='Computer'),
                                                           is_verified=True,
                                                           is_active=True)]
    )

    class Meta:
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        model = StudentInternship

        fields = '__all__'
        exclude = ['is_accepted', 'application_date', 'is_active']
