import json
import urllib

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.conf import settings


def index(request):
    user = request.user

    return render(request, "index.html", {
        "global_data": json.dumps({
            "user": {
                "id": user.id,
                "username": user.get_username()
            },
            "authorize_url": reverse("oauth2_provider:authorize") + "?" + urllib.urlencode({
                "client_id": settings.OAUTH_WEB_APP_ID,
                "response_type": "token"
            })
        })
    })


def logout_user(request):
    """Log out the current user."""
    next = request.GET.get("next") or "/"
    logout(request)
    return redirect(next)


def email_confirmation_sent(request):
    return render(request, "confirmation_email_sent.html")


def oauth_callback(request):
    return render(request, "oauth_callback.html", {"title": "Redirecting..."})

