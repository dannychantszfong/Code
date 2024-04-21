from django.db import models

class User(models.Model):
    account_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Hashed password

    def __str__(self):
        return self.account_id
