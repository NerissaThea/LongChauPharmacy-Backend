from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Prescription, UserProfile

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['file']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'address', 'phone']

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.userprofile.full_name = self.cleaned_data['full_name']
            user.userprofile.address = self.cleaned_data['address']
            user.userprofile.phone = self.cleaned_data['phone']
            user.userprofile.save()
        return user

class CheckoutForm(forms.Form):
    delivery_method = forms.ChoiceField(choices=[('delivery', 'Delivery'), ('pickup', 'Pick Up')])
    payment_method = forms.ChoiceField(choices=[('cod', 'Cash on Delivery'), ('bank', 'Bank Transfer')])
    prescription_file = forms.FileField(required=False)  # only if needed
