from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from services.forms import ServiceOrderForm, ServiceOrderReviewForm
from services.models import Service, ServiceOrder, ServiceOrderReview
from services.utils import calculate_approval_rates


def list(request):
    query = request.GET.get('q', '')
    city = request.GET.get('city')

    services = Service.objects.filter(name__icontains=query)

    if city:
        services = services.filter(user__profile__city=city)

    paginator = Paginator(services, settings.PAGINATION)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    cities = (
        Service.objects.filter(user__profile__isnull=False)
        .values('user__profile__city')
        .distinct()
    )
    cities = [city['user__profile__city'] for city in cities]

    return render(request, 'services/list.html', {'page': page, 'cities': cities})


def detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    reviews = ServiceOrderReview.objects.filter(order__service=service)
    done_services = ServiceOrder.objects.filter(
        service=service,
        status__in=[ServiceOrder.Status.DONE, ServiceOrder.Status.FINISHED],
    ).count()

    user_done_services = ServiceOrder.objects.filter(
        service__user=service.user,
        status__in=[ServiceOrder.Status.DONE, ServiceOrder.Status.FINISHED],
    ).count()

    approval_rate = calculate_approval_rates(reviews)

    total_orders = ServiceOrder.objects.filter(service__user=service.user).count()

    conclusion_rate = (user_done_services / total_orders) * 100 if total_orders else 0

    return render(
        request,
        'services/detail.html',
        {
            'service': service,
            'reviews': reviews,
            'done_services': done_services,
            'user_done_services': user_done_services,
            'approval_rate': int(approval_rate),
            'conclusion_rate': int(conclusion_rate),
        },
    )


def create_order(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceOrderForm(request.POST or None, initial={'service': service})

    if form.is_valid():
        form.save()
        return redirect('services:detail', pk=pk)

    return render(
        request, 'services/create_order.html', {'service': service, 'form': form}
    )


def create_review(request, code):
    service_order = get_object_or_404(ServiceOrder, code=code)

    if service_order.status != ServiceOrder.Status.DONE:
        return redirect('services:detail', pk=service_order.service.pk)

    form = ServiceOrderReviewForm(request.POST or None, initial={'order': service_order})

    if form.is_valid():
        form.save()
        return redirect('services:detail', pk=service_order.service.pk)

    return render(
        request,
        'services/create_review.html',
        {'service_order': service_order, 'form': form},
    )
