# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models

import datetime


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
    user = models.ForeignKey(User)
    file = models.ImageField(upload_to="/user")
    uploaded_at = models.DateTimeField(null=True, blank=True)

    @receiver(pre_save)
    def set_datetime(self):
        # TODO: 한국시간 설정
        self.uploaded_at = datetime.datetime


