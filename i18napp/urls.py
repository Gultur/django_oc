from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.test_i18n, name='test_i18n'),

]
