from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=500, blank=False, null=False, unique=True)
    wikidata_item_url = models.CharField(max_length=500, blank=True)
    wikidata_item_label = models.CharField(max_length=500, blank=True)
    wikidata_item_description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)