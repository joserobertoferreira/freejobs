from django.db.models import Count
from django.shortcuts import render

from core.forms import ContactForm
from services.models import Service


def home(request):
    cities = (
        Service.objects.filter(user__profile__isnull=False)
        .values('user__profile__city')
        .distinct()
    )
    cities = [city['user__profile__city'] for city in cities]

    top_services = Service.objects.annotate(total_orders=Count('orders')).order_by(
        '-total_reviews'
    )[:3]

    return render(
        request, 'core/home.html', {'cities': cities, 'top_services': top_services}
    )


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        form.send_email()
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
