from django import forms


class UserForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()


class EventForm(forms.Form):
    event_name = forms.CharField(label="Event Name", max_length=100)
    event_date = forms.DateField(label="Event Date", widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField(
        label="Location",
        max_length=256,
        widget=forms.TextInput(attrs={'id': 'id_location', 'readonly': 'readonly'})
    )
