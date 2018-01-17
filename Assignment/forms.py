from django import forms

from Registration.models import Subject
from .models import Assignment

subject_list = Subject.objects.all()


class AssignmentForm(forms.ModelForm):
    code = forms.ChoiceField(
        choices=[(i.pk, i.short_form) for i in subject_list]
    )

    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['code']
