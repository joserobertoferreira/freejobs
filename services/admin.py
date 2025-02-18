from django.contrib import admin

from services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'user')
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
