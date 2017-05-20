from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/correction_degree/', views.APICorrectionDegreeView.as_view(), name='index'),
    url(r'^selfie/identify', views.APISelfieIdentificationView.as_view(), name='selfie'),
    url(r'^correction_degree/', views.CorrectionDegreeView.as_view(), name='index'),
    url(r'user/logout', views.LogoutView.as_view(), name='logout'),
    url(r'user/login', views.LoginView.as_view(), name='login'),
    url(r'user/join', views.JoinView.as_view(), name='join'),
    url(r'all/flush', views.FlushView.as_view(), name='flush'),
    url(r'', views.IndexView.as_view(), name='index'),
]