from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError

from .models import Task, Project


def task(request, uuid):
    try:
        task = get_object_or_404(Task, uuid=uuid)
    except ValidationError:
        raise Http404("Mettez-y un peu du votre, bon sang !")
    return render(request,"task/detail.html", {'task': task})

def project(request, fullname):
    project = get_object_or_404(Project, fullname=fullname)
    return render(request,"project/detail.html", {'project': project})

def projectlist(request):
    plist = Project.objects.all()
    return rendre(request,"project/list.html", {'plist': plist})
