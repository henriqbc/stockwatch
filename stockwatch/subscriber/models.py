from django.db import models

MAX_STR_FIELD_SIZE = 20

class UserModel(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = MAX_STR_FIELD_SIZE)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

