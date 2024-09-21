from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, ThesisForm
from django.http import FileResponse

def home(request):
    context = {}
    # Check to see if logging in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.success(request, "Incorrect Credentials. Try Again.")
            return redirect('home')
    else:
        return render(request, 'home.html', context)

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
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = RegisterUserForm()
        context['form'] = form
    return render(request, 'register.html', context)

def publish(request):
    context = {}
    if request.method == 'POST':
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            '''
            published_date = form.cleaned_data.get('published_date')
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            pdf_file = form.cleaned_data.get('pdf_file')
            '''
            form.save()
        else:
            context['form'] = form
    else:
        form = ThesisForm()
        context['form'] = form
    return render(request, 'publish.html', context)