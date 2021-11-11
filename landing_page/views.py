import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .api import check_captcha
from .email import send_and_record_email

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
                    error_msg = "Il semblerait que l'on se connaisse déjà !"
                else:
                    if user_email and send_and_record_email(request, user_email):
                        messages.success(request, "Votre mail a bien été enregistré, merci :)")
                        return redirect("landing_page:index")

                    else:
                        error_msg = "Attention, une erreur est survenue !"
            else:
                error_msg = "Mince, la vérification a échoué !"
        else:
            error_msg = "Oups, n'oubliez pas le captcha !"

        messages.error(request, error_msg)
        return redirect("landing_page:index")
