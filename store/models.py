from django.db import models
import uuid
import random
from django.utils.text import slugify

from common.models import TimeStampedModel,Identifier,Amenities,Location

class Company(Identifier,Location):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pan = models.PositiveIntegerField()
    company_bills_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    company_code = models.CharField(max_length=200, unique=True)
    vat_required = models.BooleanField(default=1)
    logo = models.ImageField(upload_to="product/image", blank=True, null=True)

    class Meta:
        verbose_name = "Comany"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        if not self.company_bills_code:
            name_list = self.name.split()

            if len(name_list) > 1:
                company_bills_code =  ''.join([x[0].upper() for x in name_list ]) + str(self.pan)
            else:
                company_bills_code = name_list[0][0].upper() + name_list[0][-2:] + str(self.pan)

            self.company_bills_code = company_bills_code

        if not self.company_code:
            self.company_code = str(self.name)
        
        return super(Company,self).save(*args, **kwargs)

class Store(Identifier,Location,Amenities):
    contact_number=models.CharField(max_length=12)
    latitude = models.FloatField()
    longitude = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="store")
    franchise = models.BooleanField()
  
    def __str__(self):
        return self.name

WEEKDAYS = [
  ("Monday","Monday"),
  ("Tuesday","Tuesday"),
  ("Wednesday","Wednesday"),
  ("Thursday","Thursday"),
  ("Friday","Friday"),
  ("Saturday","Saturday"),
  ("Sunday","Sunday"),
]

class OpeningHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="opening_hours")
    weekday = models.CharField(max_length=200,choices=WEEKDAYS,unique=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __str__(self):
        return f'{self.store.name}'