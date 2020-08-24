from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=20)

    def __str(self):
        return self.name

    class Meta:
        # the plural name
        verbose_name_plural = 'cities'

