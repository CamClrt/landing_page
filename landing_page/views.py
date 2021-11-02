import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from landing_page.api import check_captcha
from landing_page.email import record_email

from .models import Prospect


class Index(View):
    def get(self, request):
        return render(request, "landing_page/index.html")

    def post(self, request):
        captcha = request.POST.get("g-recaptcha-response")

        if captcha:
            code, r = check_captcha(os.environ.get("GOOGLE"), captcha)

            if code == 200 and r["success"]:
                user_email = request.POST.get("user_email")

                if Prospect.objects.filter(email=user_email):
                    error_msg = "Attention, il semblerait que votre mail soit déjà enregistré."
                    messages.error(request, error_msg)

                else:
                    if user_email:
                        record_email(request, user_email)
                        return redirect("landing_page:index")

                    else:
                        error_msg = "Attention, votre mail n'a pas été renseigné !"
            else:
                error_msg = "Attention, la vérification a échoué !"
        else:
            error_msg = "Attention, le captcha est requis !"

        messages.error(request, error_msg)
        return redirect("landing_page:index")
