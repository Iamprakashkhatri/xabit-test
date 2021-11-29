from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(help_text="Object modified date and time", auto_now=True)
    created_at = models.DateTimeField(help_text="Object created date and time", auto_now_add=True)

    class Meta:
        abstract = True

class Identifier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=511, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Amenities(models.Model):
    parking = models.BooleanField(default=True)
    free_wifi = models.BooleanField(default=True)
    with_kitchen = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Location(models.Model):
    country = models.CharField(max_length=255,default="Nepal")
    street_address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=255, default="")
    state = models.CharField(max_length=255, default="")
    postal_code = models.CharField(max_length=255, default="")

    class Meta:
        abstract = True


