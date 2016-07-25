# coding: utf8
from rest_framework import viewsets, exceptions
from django.db.models import Q

from serializers import UserSerializer, MessageSerializer
from django.contrib.auth.models import User
from lobby.models import Message


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        token = request.user.auth_token
        user_id = request.data.get('sender', '')
        user = User.objects.get(id=user_id)
        if user.auth_token != token:
            raise exceptions.PermissionDenied('Wrong token')
        return super(MessageViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return sorted(self.queryset.filter(Q(sender=self.request.user.id) | Q(receiver=self.request.user.id)), key=lambda instance: instance.date)
