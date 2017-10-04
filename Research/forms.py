from django import forms

from Registration.models import Faculty
from Research.models import Paper

faculty_list = []

for i in Faculty.objects.all():
    faculty_list.append(i.user.first_name)


class ResearchForm(forms.ModelForm):
    faculty_name = forms.ChoiceField(
        choices=[(i, i) for i in faculty_list]
    )

    # widgets = {
    #     'publication_date': forms.DateInput(attrs={'class': 'datepicker'})
    # }

    type = forms.ChoiceField(
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')]
    )
    conference_type = forms.ChoiceField(
        choices=[('National', 'National'), ('International', 'International')]
    )
    peer_reviewed = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')]
    )
    publication_medium = forms.ChoiceField(
        choices=[('Online', 'Online'), ('Print', 'Print')]
    )

    class Meta:
        model = Paper
        widgets = {
            'publication_date': forms.DateInput(attrs={'class': 'datepicker'})
        }
        fields = '__all__'
