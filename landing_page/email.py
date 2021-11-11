import logging
import os
from smtplib import SMTPException

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Prospect

logger = logging.getLogger(__name__)


def send_and_record_email(email):
    # send a email alert with user_email info
    try:
        send_mail("New user", email, os.environ.get("EMAIL_CONTACT"), [os.environ.get("EMAIL_USER")])
    except SMTPException as e:
        logging.error(e)

    # record it in DB
    try:
        Prospect.objects.create(email=email)
    except ValidationError as e:
        logger.error(e)

    return "Votre mail a bien été enregistré, merci :)"
