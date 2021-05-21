import os

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render

from landing_page.api import check_captcha


def index(request):
    if request.method == "POST":
        captcha = request.POST.get("g-recaptcha-response")

        if captcha:
            code, r = check_captcha(
                os.environ.get("GOOGLE"),
                captcha,
            )

            if code == 200 and r["success"]:
                user_email = request.POST.get("user_email")

                if user_email:
                    send_mail(
                        "A new potential user",
                        user_email,
                        "contact@la-plateforme-a-caractere-associatif.fr",
                        ["camille.clarret@gmail.com"],
                        fail_silently=True,
                    )
                    messages.success(
                        request, "Merci, votre mail a bien été transmis. A bientôt !"
                    )
                else:
                    email_empty = "Attention, il semblerait que votre mail \
                    n'ait pas été renseigné."
                    messages.error(request, email_empty)
            else:
                api_error = "Il semblerait que notre vérification auprès \
                    des services de Google ait échouée. Pourriez-vous \
                    saisir à nouveau votre email ?"
                messages.error(request, api_error)
        else:
            captcha_empty = "Attention, il semblerait que le captcha n'ait \
                pas été coché. Pour finaliser l'envoie, celui-ci est requis"
            messages.error(request, captcha_empty)
    else:
        messages.info(request, "")

    return render(request, "landing_page/index.html")
