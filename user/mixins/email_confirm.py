from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.core.mail import send_mail

from user.utils import generate_random_digits


class UserEmailConfirmMixin(models.Model):
    confirmation_code = models.CharField(verbose_name="Email confirmation code", max_length=6, blank=True,
                                         null=True)
    code_send_date = models.DateTimeField(verbose_name="Code sent date", blank=True, null=True)
    confirmed_date = models.DateTimeField(verbose_name="Date email was confirmed", blank=True, null=True)

    is_confirmed = models.BooleanField(verbose_name="Почта подтвержден", default=0)

    def send_confirmation_code(self):

        User = get_user_model()

        if not isinstance(self, User):
            return False

        wait_time = timedelta(minutes=settings.USER.get("LAST_CODE_REQUESTED_TIME", 3))
        if self.code_send_date and self.code_send_date + wait_time >= datetime.now(self.code_send_date.tzinfo):  # type: ignore
            return ValidationError(settings.USER.get("WAIT_RESPONSE", ""))

        confirmation_code = generate_random_digits()

        self.confirmation_code = confirmation_code
        self.code_send_date = datetime.now()
        self.save()

        send_mail(
            subject="Подтверждение Почты",
            message=f"Ваш код для подтверждение {self.confirmation_code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email, ],  # type: ignore
        )
        return True
