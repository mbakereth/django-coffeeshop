from django import forms


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True)
