from django.db import models

# Create your models here.
class users(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    regno = models.CharField(max_length=100)
    fpbiotemplate1 = models.CharField(max_length=10000)
    fpbiotemplate2 = models.CharField(max_length=10000)
    fno1 = models.CharField(max_length=2)
    fno2 = models.CharField(max_length=2)
    date = models.DateTimeField(auto_now_add=True)
