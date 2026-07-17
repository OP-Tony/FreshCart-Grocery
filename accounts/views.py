from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomerRegistrationForm, ProfileForm
from .models import CustomerProfile


def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("catalog:product_list")
    else:
        form = CustomerRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = CustomerProfile.objects.get_or_create(
        user=request.user, defaults={"default_address": ""}
    )
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, "accounts/profile.html", {"form": form})

# Create your views here.
