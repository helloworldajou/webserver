from django import forms
from models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['correction_degree']
        widget = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widget = {
            'password': forms.PasswordInput(),
        }


class CorrectionDegreeSetForm(forms.ModelForm):
    class Meta:
        model = CorrectionDegree
        fields = '__all__'


class FaceImgForm(forms.ModelForm):
    class Meta:
        model = FaceImage
        exclude = ['uploaded_at', 'user']
