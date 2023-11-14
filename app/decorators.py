from django.db import models
from django.dispatch import receiver
import uuslug


def autoslug(fieldname):
    def decorator(model):
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.post_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                slug = uuslug.slugify(f'{source}-{instance.id}')
                if slug:
                    instance.slug = slug
                instance.save()
        return model
    return decorator
