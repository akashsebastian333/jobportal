from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm



def hehe_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return loginhe(request)

def hehe_register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return register(request)

def loginhe(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')  # redirect to the home page after successful login
        else:
            error_message = "Invalid username or password"
            return render(request, 'auth/login.html', {'error_message': error_message})

    return render(request, 'auth/login.html')


def hehe_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/account/login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            form.save()
            user = authenticate(request, username=username, password=password, email=email)
            if user != None:
                login(request, user)
                return redirect('/dashboard')
        return render(request, 'auth/signup.html', {'form': form})
    return render(request, 'auth/signup.html')