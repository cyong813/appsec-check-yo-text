from django.db import models


class Text(models.Model):
    body = models.CharField(max_length=2500)

    def __str__(self): 
        return self.body