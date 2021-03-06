# coding: utf8
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from lobby.models import Message
from api import MessageViewSet, UserViewSet


def home(request):
    args = {}
    args.update(csrf(request))
    args["tornado_host"] = settings.TORNADO_HOST
    args["tornado_port"] = settings.TORNADO_PORT
    args["sender_id"] = auth.get_user(request).id
    args["username"] = auth.get_user(request).username
    return render(request, 'lobby/home.html', dictionary=args)


def login(request):
    args = {}
    args.update(csrf(request))
    args["username"] = auth.get_user(request).username

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "User not found!!!"
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

    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            return redirect('/login/')
        else:
            args['form'] = newuser_form
    return render_to_response('lobby/register.html', args)


def room(request, receiver_id):
    args = {}
    args["tornado_host"] = settings.TORNADO_HOST
    args["tornado_port"] = settings.TORNADO_PORT
    args["username"] = auth.get_user(request).username
    sender_id = auth.get_user(request).id
    args["messages"] = sorted(Message.objects.filter(Q(sender=sender_id, receiver=receiver_id) | Q(sender=receiver_id, receiver=sender_id)), key=lambda instance: instance.date)
    args["sender_id"] = sender_id
    args["receiver_id"] = receiver_id
    args["receiver"] = User.objects.get(id=receiver_id)
    return render(request, 'lobby/room.html', dictionary=args)
