# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models

import os


def get_upload_path(instance, filename):
    if instance.user:
        return os.path.join(
            "data/faces/raw", "%s" % instance.user.username, filename)
    else:
        return os.path.join(
            "data/faces/raw", "%s" % "temp", filename)


class CorrectionDegree(models.Model):
    eyes = models.FloatField(default=0)
    chin = models.FloatField(default=0)

    def return_json(self):
        return {
            'eyes': self.eyes,
            'chin': self.chin
        }


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    correction_degree = models.OneToOneField(CorrectionDegree, blank=True, null=True)


class FaceImage(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    file = models.ImageField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(null=True, blank=True)
