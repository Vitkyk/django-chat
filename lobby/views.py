# coding: utf8
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm

from lobby.models import Message
from rest_framework import viewsets
from serializers import UserSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# utils
def json_response(obj):
    return HttpResponse(json.dumps(obj), content_type="application/json")


def send_message(sender_id, receiver_id, message_text):
    message = Message()
    message.text = message_text
    message.sender = sender_id
    message.receiver = receiver_id
    message.save()


# Views
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


@csrf_exempt
def send_message_api_view(request):
    if not request.method == "POST":
        return json_response({"error": "Please use POST."})

    api_key = request.POST.get("api_key")

    if api_key != settings.API_KEY:
        return json_response({"error": "Please pass a correct API key."})

    try:
        sender = User.objects.get(id=request.POST.get("sender_id"))
    except User.DoesNotExist:
        return json_response({"error": "No such sender."})

    try:
        receiver = User.objects.get(id=request.POST.get("receiver_id"))
    except User.DoesNotExist:
        return json_response({"error": "No such receiver."})

    message_text = request.POST.get("message")

    if not message_text:
        return json_response({"error": "No message found."})

    if len(message_text) > 300:
        return json_response({"error": "The message is too long."})

    send_message(sender.id, receiver.id, message_text)

    return json_response({"status": "ok"})