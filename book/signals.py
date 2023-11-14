from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Review


@receiver(post_save, sender=Review)
def update_book_average_rating(sender, instance, **kwargs):
    book = instance.book
    reviews = book.reviews.all()

    if not reviews.exists():
        return

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    book.average_rating = min(round(average_rating, 2), 5.0)
    book.save()
