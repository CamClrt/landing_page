from django.db import models
from model_utils.models import TimeStampedModel


class Prospect(TimeStampedModel):
    """
    Model for potential future users
    """

    email = models.EmailField("email", blank=True)

    def __str__(self):
        return self.email
