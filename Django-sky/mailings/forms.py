from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Client, Mailing


class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MailingForm(forms.ModelForm):

    start_datetime = forms.DateField(widget=DateInput)
    stop_datetime = forms.DateField(widget=DateInput)

    class Meta:
        model = Mailing
        fields = ['start_datetime', 'stop_datetime', 'periodicity', 'status']



class CombinedMailingForm(forms.Form):
    start_datetime = forms.DateField(widget=DateInput)
    stop_datetime = forms.DateField(widget=DateInput)
    periodicity = forms.ChoiceField(choices=Mailing.PERIODICITY_CHOICES)
    status = forms.ChoiceField(choices=Mailing.STATUS_CHOICES)
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
