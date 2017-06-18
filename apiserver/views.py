# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from apiserver.face_identifier import identifier, FaceIdentifier
from forms import *


class IndexView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        logged_in_user = request.session.get('username')
        if logged_in_user:
            user = User.objects.filter(username=logged_in_user)[0]
            return render(request, './index.html', {
                'eyes': user.correction_degree.eyes,
                'chin': user.correction_degree.chin,
                'logged_in': True
            })

        return render(request, './index.html', {'message': "You have to sign in!"})


class JoinView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        if request.session.get('username'):
            return redirect('/')
        else:
            return render(request, './join.html')

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if User.objects.filter(username=user.username):
                return render(request, './join.html')

            request.session['username'] = user.username
            user.correction_degree = CorrectionDegree.objects.create()
            user.save()
            return redirect('/')
        else:
            return HttpResponseBadRequest()


class LoginView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        if request.session.get('username'):
            return redirect('/', {'message': 'You already logged in'})
        return render(request, './login.html')

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_info = login_form.save(commit=False)
            if User.objects.get(username=login_info.username, password=login_info.password):
                request.session['username'] = login_info.username
                return redirect('/')

        return redirect('/login', {'message': 'Wrong information'})


class LogoutView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        if request.session.get('username'):
            request.session.flush()
        return redirect('/')


class CorrectionDegreeView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logged_in_user = request.session.get('username')
        if logged_in_user:
            return render(request, './correction_degree_set.html', {'logged_in': True})
        return render(request, './index.html', {'message': "You have to sign in!"})

    def post(self, request, *args, **kwargs):
        logged_in_user = request.session.get('username')
        user = User.objects.filter(username=logged_in_user)[0]
        form = CorrectionDegreeSetForm(request.POST)

        correction_degree = form.save(commit=False)
        user.correction_degree.eyes = correction_degree.eyes
        user.correction_degree.chin = correction_degree.chin
        user.correction_degree.save()
        user.save()

        return redirect('/')


class APICorrectionDegreeView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username)[0]
        payload = user.correction_degree.return_json()
        return JsonResponse(payload)

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        payload = json.loads(request.body.decode('utf-8'))
        user.correction_degree.eyes = payload.get("eyes", 1)
        user.correction_degree.chin = payload.get("chin", 90)
        user.correction_degree.save()
        user.save()

        return HttpResponse('/')


class APISelfieView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, './selfie.html')

    def post(self, request, *args, **kwargs):
        return render(request, './selfie.html')


class APISelfieTrainingView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # TODO: Initiate Training!!!
        username = kwargs.get('username')
        identifier.train_svm(username)

        return render(request, './selfie.html')

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        face_img_form = FaceImgForm(request.POST, request.FILES)
        payload = {"message": u"Invalid"}
        if face_img_form.is_valid():
            face_img = face_img_form.save(commit=False)
            face_img.user = User.objects.get_or_create(username=username)[0]
            face_img.save()
            payload = {"message": u"Done at"+face_img.file.path}
            FaceIdentifier.process_frame(request.FILES['file'], username)

        return render(request, './selfie.html', payload)


class APISelfieIdentificationView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, './selfie.html')

    def post(self, request, *args, **kwargs):
        face_img_form = FaceImgForm(request.POST, request.FILES)
        if face_img_form.is_valid():
            face_img = face_img_form.save()

            person = identifier.predict(face_img.file.path)

            username = person.decode('utf-8')
            user = User.objects.get_or_create(username=username)[0]
            if user.correction_degree is None:
                user.correction_degree = CorrectionDegree.objects.create()
                user.save()

            payload = {"username": username}
            payload.update(user.correction_degree.return_json())
            return JsonResponse(payload)

        return HttpResponseBadRequest()


class FlushView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Render test page
    def get(self, request, *args, **kwargs):
        User.objects.all().delete()
        CorrectionDegree.objects.all().delete()
        return redirect('/')
