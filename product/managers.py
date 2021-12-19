from django.db import models
from django.utils import timezone
today_date = timezone.now().date()

class SubCategoryQuerySet(models.QuerySet):
    pass


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return SubCategoryQuerySet(self.model, using=self._db).select_related("category")
        
class ProductQuerySet(models.QuerySet):
    def this_month(self):
        return self.filter(created_at__year=today_date.year, created_at__month=today_date.month)

class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            ProductQuerySet(self.model, using=self._db)
            .select_related("sub_category__category")
        )

    def this_month(self):
        return self.get_queryset().this_month()
