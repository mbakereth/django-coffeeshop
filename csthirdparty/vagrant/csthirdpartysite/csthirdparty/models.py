from django.db import models


class Cookies(models.Model):
    cookies = models.CharField(max_length=256)
    add_date = models.DateField()

    def __str__(self):
        return self.key


class PostTest(models.Model):
    value = models.CharField(max_length=256)
    add_date = models.DateField()

    def __str__(self):
        return self.value
