# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from models import User, CorrectionDegree
from forms import UserForm


class IndexView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        if request.session.get('username'):
            return render(request, './index.html', {'logged_in': True, 'username': request.session.get('username')})
        else:
            return render(request, './index.html', {'logged_in': False})


class JoinView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('/')
        else:
            return render(request, './join.html')

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            request.session['username'] = user.username
            user.save()
            return render(request, './index.html')
        else:
            return HttpResponseBadRequest()


class CorrectionDegreeView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        user_id = request.POST.__getitem__('user_id')
        user = User.objects.get(e_mail_address=user_id)
        correction_degree = serializers.serialize('json', user.correction_degree)
        return HttpResponse(correction_degree, content_type="application/json")

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(e_mail_address=user_id)
        user.correction_degree.eyes = payload['eyes']
        user.correction_degree.chin = payload['chin']
        user.save()

        return HttpResponse()
