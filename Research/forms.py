from django import forms

from Research.models import Paper


class PublicationForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')],
        widget=forms.RadioSelect
    )

    level = forms.ChoiceField(
        choices=[('National', 'National'), ('International', 'International')],
        widget=forms.RadioSelect
    )

    conference_attended = forms.ChoiceField(
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.RadioSelect,
        required=False
    )

    first_author = forms.ChoiceField(
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.RadioSelect,
    )

    medium = forms.ChoiceField(
        choices=[('Journal', 'Journal'), ('Conference', 'Conference')],
        widget=forms.RadioSelect,
    )

    paper_with = forms.ChoiceField(
        choices=[('BE Student', 'BE Student'), ('ME Student', 'ME Student'), ('PhD Student', 'PhD Student'),
                 ('Self', 'Self')]
    )

    distribution = forms.ChoiceField(
        choices=[('Online', 'Online'), ('Print', 'Print')],
        widget=forms.RadioSelect
    )

    peer_reviewed = forms.ChoiceField(
        choices=[('True','Yes'),('False','No')],
        widget = forms.RadioSelect
    )

    class Meta:
        model = Paper

        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'})
        }

        fields = '__all__'
        exclude = ['is_conference']
