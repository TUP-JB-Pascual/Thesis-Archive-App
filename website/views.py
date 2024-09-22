from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

from .forms import RegisterUserForm, ThesisForm
from .models import Thesis

def home(request):
    context = {}
    return render(request, 'home.html', context)

def login_user(request):
    context = {}
    # Check to see if logging in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(email)
        print(password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.success(request, "Incorrect Credentials. Try Again.")
            return redirect('login')
    else:
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "You have Logged Out.")
    return redirect('home')

def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "You have Succesfully Registered.")
            return redirect('login')
    else:
        form = RegisterUserForm()
        context['form'] = form
    return render(request, 'register.html', context)

def publish(request):
    context = {}
    if request.method == 'POST':
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, "Upload Successful.")
            form.save()
            return redirect('publish')
    else:
        form = ThesisForm()
        context['form'] = form
    return render(request, 'publish.html', context)

def thesis_list(request):
    thesis_list = Thesis.objects.all()
    context = {'thesis_list': thesis_list}
    return render(request, 'thesis_list.html', context)
