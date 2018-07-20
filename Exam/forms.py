from django import forms

from Exam.models import ExamDetail, ExamMaster
from General.models import YearBranch, Semester


class ExamDetailForm(forms.ModelForm):
    # subjects = forms.ModelMultipleChoiceField(queryset=.objects.all(), required=False,
    #                                              widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(ExamDetailForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = ExamMaster.objects.filter(is_active=True)
        self.fields['year'].queryset = YearBranch.objects.filter(is_active=True)
        self.fields['semester'].queryset = Semester.objects.filter(is_active=True)
        for field in self.fields:
            if field not in ['schedule_start_date', 'schedule_end_date']:
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        widgets = {
            'schedule_start_date': forms.DateInput(attrs={'class': 'datepicker form-control'}),
            'schedule_end_date': forms.DateInput(attrs={'class': 'datepicker form-control'}),
        }

        model = ExamDetail
        fields = '__all__'
        exclude = ['is_active']

    def clean(self):
        cleaned_data = super().clean()
        schedule_start_date = cleaned_data.get('schedule_start_date')
        schedule_end_date = cleaned_data.get('schedule_end_date')

        if schedule_end_date and schedule_start_date:
            if schedule_end_date < schedule_end_date:
                raise forms.ValidationError("End date should be less than start date")
