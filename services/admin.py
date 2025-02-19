from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse

from services.models import Service, ServiceOrder, ServiceOrderReview


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'user',
        'average_rating',
        'total_reviews',
    )
    list_filter = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change) -> None:
        if not request.user.is_superuser:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj):  # noqa: PLR6301
        if not request.user.is_superuser and not obj:
            return ['user']
        return []

    def get_readonly_fields(self, request, obj):  # noqa: PLR6301
        if obj and not request.user.is_superuser:
            return ['user']
        return []


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'service',
        'name',
        'email',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'service',
        'status',
    )
    actions = (
        'cancel_service_order',
        'conclude_service_order',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(service__user=request.user)

    @admin.action(description='Cancelar ordem')
    def cancel_service_order(self, request, queryset):
        queryset.filter(status=ServiceOrder.Status.OPEN).update(
            status=ServiceOrder.Status.CANCELED
        )
        self.message_user(request, 'Ordem de serviço cancelada com sucesso.')

    @admin.action(description='Concluir ordem')
    def conclude_service_order(self, request, queryset):
        queryset.filter(status=ServiceOrder.Status.OPEN).update(
            status=ServiceOrder.Status.DONE
        )

        for service_order in queryset:
            relative_review_url = reverse(
                'services:create_review', kwargs={'code': service_order.code}
            )
            review_url = request.build_absolute_uri(relative_review_url)

            message = f'Olá {service_order.name},\n\n'
            message += f'A ordem de serviço {service_order.code} foi concluída.\n\n'
            message += f'Serviço: {service_order.service.name}\n'
            message += f'Valor: $ {service_order.service.price:.2f}\n\n'
            message += f'Avalie o serviço em: {review_url}\n\n'
            message += 'Atenciosamente,\n'
            message += 'Equipe de serviços'

            send_mail(
                'Ordem de serviço concluída',
                message,
                settings.CONTACT_EMAIL,
                [service_order.email],
            )

        self.message_user(request, 'Ordem de serviço concluída com sucesso.')


@admin.register(ServiceOrderReview)
class ServiceOrderReviewAdmin(admin.ModelAdmin):
    list_display = (
        'order__service__name',
        'order__name',
        'order__email',
        'rating',
    )
    list_filter = ('rating',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(order__service__user=request.user)
