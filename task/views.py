from django.shortcuts import render
from django.http import HttpResponse

from .models import Task


def detail(request, uuid):
    task = Task.objects.get(uuid=uuid)
    return render(request,"task/detail.html", {'task': task})
