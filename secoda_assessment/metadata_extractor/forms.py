from django import forms

class DatabaseInfoForm(forms.Form):
    host = forms.CharField(max_length=255, required=True)
    db_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(required=True)
    port = forms.IntegerField(required=True, min_value=1)
