from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm, RegisterForm, UserProfileForm, CustomPasswordChangeForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'authentication/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful. Welcome!'))
            return redirect('dashboard')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'authentication/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'authentication/profile.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, _('Password changed successfully.'))
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'authentication/change_password.html', context)