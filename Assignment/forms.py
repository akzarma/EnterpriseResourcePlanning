from django import forms

from General.models import BranchSubject, FacultySubject, CollegeExtraDetail, Batch
from Registration.models import Subject, Branch
from .models import AssignmentInfo, UploadedAssignment
import datetime

branch_obj = Branch.objects.get(branch='Computer')

subject_list = FacultySubject.objects.filter(division__branch__branch=branch_obj)

batch_list = Batch.objects.filter(division__branch__branch=branch_obj)


class AssignmentInfoForm(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = super().clean()
    #     complete_by = cleaned_data.get("complete_by")
    #     # subject = cleaned_data.get("subject")
    #     if complete_by < datetime.datetime.now():
    #         raise forms.ValidationError(
    #             "'complete_by' date cannot be less than today's date"
    #         )

    group = forms.ChoiceField(
        choices=[('Group A', 'Group A'),('Group B', 'Group B'),('Group C', 'Group C'),('Group D', 'Group D'),
                 ('Group E', 'Group E')]
    )
    subject = forms.ChoiceField(
        choices=[(i.pk, i.subject.short_form) for i in subject_list]
    )

    batch = forms.ChoiceField(
        choices=[(i.pk, i) for i in batch_list]
    )

    class Meta:
        widgets = {
            'issue_date': forms.DateInput(attrs={'class': 'datetimepicker'}),
            'complete_by': forms.DateInput(attrs={'class': 'datetimepicker'}),
        }
        model = AssignmentInfo
        fields = '__all__'
        exclude = ['subject', 'batch']

# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignment
#         fields = '__all__'
#         exclude = ['faculty']
