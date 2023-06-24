from django import forms

class TumorDetectionForm(forms.Form):
    image = forms.ImageField()
