from django.urls import path

from core.views import about, contact, home

app_name = 'core'
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
