from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^confirmation_email$', views.email_confirmation_sent, name="confirmation_email"),
    url(r'^oauth_callback$', views.oauth_callback, name="oauth_callback"),
    url(r'^/logout', views.logout_user),
    url(r'^.*$', views.index, name='index')
]