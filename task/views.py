from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Project


def task(request, uuid):
    task = Task.objects.get(uuid=uuid)
    return render(request,"task/detail.html", {'task': task})

def project(request, fullname):
    project = Project.objects.get(fullname=fullname)
    return render(request,"project/detail.html", {'project': project})
