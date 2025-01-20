from django import forms
from .models import UserAddress


class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        # Extract the request object during form initialization
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get('address_id')

        # Ensure the request object is available and the user is authenticated
        if not self.request or not self.request.user.is_authenticated:
            raise forms.ValidationError("User authentication is required.")

        user = self.request.user
        try:
            # Check if the address exists and belongs to the current user
            address = UserAddress.objects.get(id=address_id, user=user)
        except UserAddress.DoesNotExist:
            raise forms.ValidationError(
                "Invalid address for the requested user.")

        return address.id  # Return the validated address ID
