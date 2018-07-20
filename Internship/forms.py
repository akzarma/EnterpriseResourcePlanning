from django import forms

from General.models import StudentInternship
from Internship.models import Internship
from Registration.models import Branch


class StudentInternshipForm(forms.ModelForm):
    # branch should be passed as a parameter in form
    internship = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super(StudentInternshipForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update({'autocomplete': 'off', })
        self.fields['end_date'].widget.attrs.update({'autocomplete': 'off', })
        self.fields['internship'] = forms.ChoiceField(
            choices=[(i.pk, i) for i in Internship.objects.filter(branch=Branch.objects.get(branch='Computer'),
                                                                  is_verified=True,
                                                                  is_active=True)])
        self.fields['internship'].widget.attrs.update({'class': 'form-control', })

    class Meta:
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker form-control'}),
            'work_from_home': forms.CheckboxInput(attrs={'class': 'form-control'}),

        }
        model = StudentInternship
        fields = '__all__'
        exclude = ['is_accepted', 'application_date', 'is_active', 'internship']


class InternshipForm(forms.ModelForm):
    branch = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super(InternshipForm, self).__init__(*args, **kwargs)

        self.fields['branch'] = forms.ChoiceField(
            choices=[(i.pk, i) for i in Branch.objects.all()]

        )
        self.fields['branch'].widget.attrs.update({'class': 'form-control', })

        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Internship
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control   '}),
            'address': forms.TextInput(attrs={'class': 'form-control   '}),
            'email': forms.TextInput(attrs={'class': 'form-control   '}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control   '}),
            'website': forms.TextInput(attrs={'class': 'form-control   '}),
            'branch': forms.TextInput(attrs={'class': 'form-control   '}),
        }
        fields = '__all__'
        exclude = ['is_active', 'is_verified', 'branch']
