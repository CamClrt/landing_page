import logging
import os

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Prospect

logger = logging.getLogger(__name__)


def record_email(request, email):
    # send a email alert with user_email info
    send_mail("New user", email, os.environ.get("EMAIL_CONTACT"), [os.environ.get("EMAIL_USER")], fail_silently=True)

    # record it in DB
    try:
        Prospect.objects.create(email=email)
    except ValidationError as e:
        logger.error(e)

    return messages.success(request, "Votre mail a bien été enregistré, merci :)")
