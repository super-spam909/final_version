from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from .models import Task



# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='task'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task']=context['task'].filter(user=self.request.user)
        context['count']=context['task'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__startswith = search_input)
            context['search-input']= search_input
        return context 
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name='task'
    template_name ='todo/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name='task'
    success_url = reverse_lazy('task')
    
from django.shortcuts import render, HttpResponse
from django.contrib import auth
from .models import Signup

def custom_login(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, "task", {})
        else:
            return HttpResponse('Invalid login credentials. Please try again.')

    return render(request, "todo/login.html", {})

def custom_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        repeat_password = request.POST['repeatPassword']

        if repeat_password != password:
            return HttpResponse('ERROR , passwords dont match')
        else:
            new_signup = Signup(username=username, name=name, password=password)
            new_signup.save()

    return render(request, "todo/register.html", {})

def home(request, *args, **kwargs):
    return render(request, "task", {})
