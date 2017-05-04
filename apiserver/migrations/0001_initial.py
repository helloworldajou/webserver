# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 09:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectionDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eyes', models.FloatField(default=0)),
                ('chin', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('correction_degree', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apiserver.CorrectionDegree')),
            ],
        ),
    ]
