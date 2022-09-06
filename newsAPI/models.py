from django.db import models
from django.contrib.postgres.fields import ArrayField

class News(models.Model):
    class Meta:
        db_table = 'news'
    id = models.CharField(max_length=512, primary_key=True)
    uri = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=256), blank=True)
    pdate = models.DateField()