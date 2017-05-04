# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
