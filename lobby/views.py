# coding: utf8
from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm


def home(request):
    args = {}
    args.update(csrf(request))
    args["users"] = User.objects.all()
    args["username"] = auth.get_user(request).username
    return render(request, 'lobby/home.html', dictionary=args)


def login(request):
    args = {}
    args.update(csrf(request))
    args["users"] = User.objects.all()
    args["username"] = auth.get_user(request).username
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('lobby/login.html', args)
    else:
        return render_to_response('lobby/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    args["users"] = User.objects.all()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            # auth.authenticate(username=request.user, password=newuser_form.password1)
            # args["username"] = auth.get_user(request).username
            return redirect('/login/')
        else:
            args['form'] = newuser_form
    return render_to_response('lobby/register.html', args)