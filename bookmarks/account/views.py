from django.shortcuts import render
from . forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . models import Profile
from django.contrib import messages
# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('login successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('invalid login')
    else:
        form = LoginForm()   
    context = {'form':form}
    return render(request, 'account/login.html', context)

@login_required
def dashboard(request):
    context = {'section':dashboard}
    return render(request, 'account/dashboard.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            context = {'new_user':new_user}
            return render(request, 'account/register_done.html', context)
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'account/register.html', context)    

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
          
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updation your profile')
            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'account/edit.html', context) 
    