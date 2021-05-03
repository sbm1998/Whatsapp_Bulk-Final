from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Read_csv,Attachment

class Option(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 120}))
    
class Add_number(forms.Form):
    Phone_No = PhoneNumberField()

class Add_csv(forms.ModelForm):
    class Meta:
        model = Read_csv
        fields = ("File",)

class Add_Attachment(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ("File",)
