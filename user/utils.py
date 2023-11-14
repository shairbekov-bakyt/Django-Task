import random
from django.conf import settings


def generate_random_digits(length=settings.USER.get("CODE_LENGTH", 6)):
    digits = [str(random.randint(0, 9)) for _ in range(length)]
    return ''.join(digits)
