import json
import urllib

from django.shortcuts import render
from django.contrib.auth import get_user
from django.core.urlresolvers import reverse
from django.conf import settings


def index(request):
    user = get_user(request)

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

def email_confirmation_sent(request):
    return render(request, "confirmation_email_sent.html")

