from django import forms
from .models import IncidentReport


# Form for users to report an incident
class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['name', 'email', 'relationship', 'victim_name', 'location', 'description', 'proof_files']


# Form for users to send an issue message to parents
class IssueReportForm(forms.Form):
    parent_email = forms.EmailField(label="Parent's Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")
