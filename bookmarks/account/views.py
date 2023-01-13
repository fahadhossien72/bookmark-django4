from django.shortcuts import render
from . forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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