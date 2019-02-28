from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import UsersRegistrationForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def registration_view(request):
    if request.method =='POST':
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Your account has been created successfully. Now, you can login to your account')
            return HttpResponseRedirect('/login')
    else:
        form = UsersRegistrationForm()
    return render(request, 'usersapp/register.html', {'form':form})
@login_required
def user_profile_view(request):
    return render(request, 'usersapp/profile.html')


@login_required
def update_profile_view(request):
    if request.method =='POST':
        userupdate =UserUpdateForm(request.POST, instance=request.user)
        profileupdate = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if userupdate.is_valid() and  profileupdate.is_valid():
            userupdate.save()
            profileupdate.save()
            messages.success(request, f'Your account has been updated successfully!')
            return HttpResponseRedirect('/profile')
    else:
        userupdate =UserUpdateForm(instance=request.user)
        profileupdate = ProfileUpdateForm(instance = request.user.profile)
    return render(request, 'usersapp/profileupdate.html', {'userupdate': userupdate, 'profileupdate': profileupdate})
