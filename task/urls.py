from django.urls import path

from . import views

urlpatterns = [
        path('<str:uuid>/', views.detail, name='detail'),
]
