from django.contrib.auth.models import User
from django.db import models


def service_upload_to(instance, filename):
    return f'services/{instance.user.username}/{filename}'


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=service_upload_to, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
