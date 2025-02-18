from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render

from services.models import Service


def list(request):
    services = Service.objects.all()
    paginator = Paginator(services, settings.PAGINATION)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'services/list.html', {'page': page})
