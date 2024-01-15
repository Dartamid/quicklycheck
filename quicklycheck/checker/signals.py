from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from .models import Blank, TempBlank


@receiver(post_delete, sender=Blank)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=TempBlank)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
