from django import forms


class AddCommentForm(forms.Form):
    product_id = forms.IntegerField(required=True)
    comment = forms.CharField(required=True)


class DelCommentForm(forms.Form):
    id = forms.IntegerField(required=True)


class ChangeEmailForm(forms.Form):
    old_email = forms.EmailField(required=True)
    new_email = forms.EmailField(required=True)
    confirm_email = forms.EmailField(required=True)
