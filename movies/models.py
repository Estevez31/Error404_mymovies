from django.db import models

class  Genre(models.Model):
    name = models.CharField(max_length=100)
    def _str_(self):
        return self.name
