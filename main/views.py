import json

from django.shortcuts import render
from django.contrib.auth import get_user

def index(request):
    user = get_user(request)
    return render(request, "index.html", {
        "global_data": json.dumps({
            "user": {
                "id": user.id,
                "username": user.get_username()
            }
        })
    })

def email_confirmation_sent(request):
    return render(request, "confirmation_email_sent.html")
