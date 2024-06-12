from django.db import models # type: ignore

# Create your models here.

class Category(models.Model):
    cat_id=models.AutoField(primary_key=True)
    cat_name=models.CharField(max_length=50)
    budget=models.DecimalField(max_digits = 9, decimal_places = 2)
    def __str__(self) :
        return self.cat_name


class Activity(models.Model):
    ac_id=models.AutoField(primary_key=True)
    ac_name=models.CharField(max_length=50)
    ac_desc=models.CharField(max_length=200)
    expense=models.DecimalField(max_digits = 9, decimal_places = 2)
    a_cat = models.ForeignKey(Category, on_delete=models.CASCADE, default = 1)
    a_date=models.DateField()
    def __str__(self) :
        return self.ac_name


