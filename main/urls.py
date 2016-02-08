from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'/confirmation_email', views.email_confirmation_sent, name="confirmation_email"),
    url(r'.*', views.index, name='index'),
]