# coding: utf8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    class Meta():
        db_table = "message"
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    text = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text