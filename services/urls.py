from django.urls import path

from services.views import list

app_name = 'services'
urlpatterns = [
    path('', list, name='list'),
]
