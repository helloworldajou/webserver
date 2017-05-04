from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/correction_degree/', views.CorrectionDegreeView.as_view(), name='index'),
    url(r'join', views.JoinView.as_view(), name='join'),
    url(r'', views.IndexView.as_view(), name='index'),
]