from django.db import models
from django.utils.text import slugify

from applications.custom_auth.models import Salle


class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name