# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.db import models


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


class Image(models.Model):
    uploader = models.ForeignKey(User)
    file = models.FileField()
    users_in_img = ArrayField(User, null=True, blank=True)

