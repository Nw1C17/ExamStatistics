from django.shortcuts import render
from django import views
import json
import pandas as pd
import datetime


from .forms import LoginForm, RegistrationForm, TemplateBuilderForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login

from main.models import *
from django.contrib.auth import get_user_model

from .services import tempBuildContext, reportContext, mainContext, profileContext

User = get_user_model()


class HomePage(views.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return render(request, 'main/home.html', mainContext.getContext(request))
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'main/login.html', context)

class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'main/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'main/login.html', context)

class RegistrationView(views.View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'main/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'main/registration.html')


class TemplateBuilderView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/templateBuilder.html', tempBuildContext.getContext(request))

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return tempBuildContext.requestAjax(request)
        return tempBuildContext.postData(request)

class ProfileView(views.View):
    def get(self, request, *args, **kwargs):
        # temp = list(UserTemplates.objects.filter(user=request.user).values_list('id', 'name'))
        # context = {
        #     'username': request.user.username,
        #     'first_name': request.user.first_name,
        #     'last_name': request.user.last_name,
        #     'email': request.user.email,
        #     'templates': temp
        # }
        return render(request, 'main/profile.html', profileContext.getContext(request))

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return profileContext.requestAjax(request)


class ReportView(views.View):
    def get(self, request, *args, **kwargs):
        data = reportContext.getContext(request, kwargs)
        # return render(request, 'main/report.html', data)
        #return JsonResponse(data)
        return render(request, 'main/preview.html', data)


