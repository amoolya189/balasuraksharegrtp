from django import forms
from .models import IncidentReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['name', 'email', 'relationship', 'victim_name', 'location', 'description', 'proof_files']
class ReportForm(forms.Form):
    parent_email = forms.EmailField(label="Parent's Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    