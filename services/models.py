import uuid

from django.contrib.auth.models import User
from django.db import models


def service_upload_to(instance, filename):
    return f'services/{instance.user.username}/{filename}'


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    picture = models.ImageField(upload_to=service_upload_to, blank=True, null=True)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, editable=False
    )
    total_reviews = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class ServiceOrder(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Aberta'
        CANCELED = 'CANCELED', 'Cancelada'
        DONE = 'DONE', 'Concluída'
        FINISHED = 'FINISHED', 'Finalizada'

    code = models.UUIDField(default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    extra_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'Order Service'
        verbose_name_plural = 'Order Services'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.service.user.email_user(
                subject='Nova ordem de serviço',
                message=f'Ordem de serviço: {self.code}\n\nNova ordem de serviço foi criada para o serviço: {self.service.name}',
            )

        return super().save(args, kwargs)


class ServiceOrderReview(models.Model):
    order = models.ForeignKey(
        ServiceOrder, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.order.code} - {self.rating}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __notify_user(self):
        self.order.service.user.email_user(
            subject='Nova avaliação',
            message=f'Nova avaliação para o serviço: {self.order.service.name}\n\nComentário: {self.comment}',
        )

    def __update_service_order(self):
        self.order.status = ServiceOrder.Status.FINISHED
        self.order.save()

    def __update_service_rating(self):
        service = self.order.service
        service.total_reviews += 1
        service.average_rating = (
            service.average_rating + self.rating
        ) / service.total_reviews
        service.save()

    def __update_user_rating(self):
        user_profile = self.order.service.user.profile
        user_profile.total_reviews += 1
        user_profile.average_rating = (
            user_profile.average_rating + self.rating
        ) / user_profile.total_reviews
        user_profile.save()

    def save(self, *args, **kwargs):
        self.__notify_user()
        self.__update_service_order()
        self.__update_service_rating()
        self.__update_user_rating()

        return super().save(args, kwargs)
