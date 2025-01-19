from django import forms


class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
