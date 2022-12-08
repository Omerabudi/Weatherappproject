from django import forms
from django.core import validators

class FormName(forms.Form):
    name= forms.CharField()
    email= forms.EmailField()
    verify_email=forms.EmailField(label='enter your email again')
    password= forms.CharField(widget=forms.PasswordInput())   
    def clean(self):
        all_Clean_Data=super().clean()
        if not ('email' in all_Clean_Data.keys() and 'verify_email' in all_Clean_Data.keys()):
            raise forms.ValidationError("Please fill all fields.")
        else:
            email=all_Clean_Data['email']
            v_email=all_Clean_Data['verify_email']
            if email!=v_email:
                raise(forms.ValidationError("make sure emails match!"))
