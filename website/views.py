from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import reverse_lazy

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

class ThesisPublishView(CreateView):
    model = Thesis
    template_name = 'thesis_publish.html'
    form_class = ThesisForm
    #messages.success(request, "Upload Successful.")

class ThesisListView(ListView):
    model = Thesis
    template_name = 'thesis_list.html'

class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ThesisDetailView(XFrameOptionsExemptMixin, DetailView):
    model = Thesis
    template_name = 'thesis_detail.html'
    
class ThesisUpdateView(UpdateView):
    model = Thesis
    template_name = 'thesis_update.html'
    form_class = ThesisForm
    
class ThesisDeleteView(DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')
