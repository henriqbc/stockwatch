from django.db import models
from django.contrib.auth.models import User

class EmailInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    email = models.EmailField()

    def __str__(self):
        return self.email
