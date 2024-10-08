from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publish_year = models.IntegerField()
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return self.title

