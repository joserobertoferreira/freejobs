from django.urls import path

from services.views import create_order, create_review, detail, list

app_name = 'services'
urlpatterns = [
    path('', list, name='list'),
    path('<int:pk>/', detail, name='detail'),
    path('<int:pk>/order/', create_order, name='create_order'),
    path('review/<uuid:code>/', create_review, name='create_review'),
]
