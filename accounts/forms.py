from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CustomerProfile


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    default_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            CustomerProfile.objects.update_or_create(
                user=user,
                defaults={
                    "phone": self.cleaned_data.get("phone", ""),
                    "default_address": self.cleaned_data["default_address"],
                },
            )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["phone", "default_address"]
        widgets = {"default_address": forms.Textarea(attrs={"rows": 3})}
