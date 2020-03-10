from django.db import models
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    ns_choices = [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D"), ("e", "E")]
    nutriscore = models.CharField(max_length=1, choices=ns_choices, db_index=True)
    categories = ArrayField(models.CharField(max_length=100))
    name = models.CharField(max_length=200, unique=True)
    image = models.URLField()
    link = models.URLField(unique=True)

    def __str__(self):
        return self.name
