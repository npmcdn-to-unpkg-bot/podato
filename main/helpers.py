from django.core import mail
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
import sendgrid

from social.pipeline.partial import partial


def send_confirmation_email(strategy, backend, code):
    url = strategy.build_absolute_uri(
        reverse('social:complete', args=(backend.name,), )
    ) + '?verification_code=' + code.code
    url = strategy.request.build_absolute_uri(url)
    message = """Hi!

    Thank you for signing up for Podato.
    To confirm your email address, please click this link:
    """ + url

    client = sendgrid.SendGridClient(settings.SENDGRID_API_KEY, raise_errors=True)
    mail = sendgrid.Mail(to=code.email, subject="Welcome to Podato, please confirm your email address.", text=message, from_name="Podato", from_email="noreply@podato.net")
    client.send(mail)


class BasicUserInfoForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=1, required=True, label="Username")
    email = forms.EmailField(label="Email address", required=True)


@partial
def ensure_required_data(backend, strategy, details=None, is_new=True, *args, **kwargs):
    """Ensure that the user has a username and email address."""
    data = dict(details)
    data.update(backend.strategy.request_data())
    if isinstance(data["username"], list):
        data["username"] = data["username"][0]
    if isinstance(data["email"], list):
        data["email"] = data["email"][0]

    form = BasicUserInfoForm(data)

    if not is_new:
        return {}

    if data["username"] and data["email"] and form.is_valid():
        details.update(form.cleaned_data)
        return {"details": details}

    return render(strategy.request, "ensure_required_data.html", {
        "form": form,
        "backend_name": backend.name
    })