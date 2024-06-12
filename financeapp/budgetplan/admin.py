from django.contrib import admin

from budgetplan import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Activity)