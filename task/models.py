from django.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    name        = models.CharField('Projet', max_length=50)
    shortname   = models.CharField('Identifiant', max_length=50)
    description = models.TextField('Description')

class Tag(models.Model):
    name        = models.CharField('Tag', max_length=50)
    description = models.TextField('Description')

class Uda(models.Model):
    name        = models.CharField('Attribut', max_length=50)
    description = models.TextField('Description')
    value       = models.TextField('Valeur')

class Task(models.Model):
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('deleted', 'Deleted'),
            ('waiting', 'Waiting'),
            ('recurring', 'Recurring'),
            ]
    description = models.TextField('Description', blank=False)
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    status      = models.CharField('Status', choices=STATUS_CHOICES, default='pending', max_length=9)
    autor       = models.ForeignKey(User, verbose_name="Auteur", null=True, on_delete=models.SET_NULL, blank=True)
    depends     = models.ManyToManyField("self", verbose_name="Dépendances", symmetrical=False, blank=True, related_name="task_depends")
    entry       = models.DateTimeField('Date de créaton', blank=False)
    due         = models.DateTimeField('Date d\'échéance', blank=True)
    start       = models.DateTimeField('Date de début', blank=True)
    end         = models.DateTimeField('date de fin', blank=True)
    until       = models.DateTimeField('Date de fin de récurrence', blank=True)
    scheduled   = models.DateTimeField('Date prévue', blank=True)
    wait        = models.DateTimeField('Date d\'attente', blank=True)
    modified    = models.DateTimeField('Date de modification', blank=False)
    recur       = models.CharField('Périodicité', blank=True, max_length=50)
    mask        = models.CharField('Masque', blank=True, max_length=256)
    imask       = models.IntegerField('Indice de masque', blank=True)
    parent      = models.ForeignKey('self', verbose_name="Parent", on_delete=models.CASCADE, blank=True, related_name="task_parent")
    project     = models.ForeignKey(Project, verbose_name="Projet", on_delete=models.CASCADE, blank=True)
    priority    = models.CharField('Priorité', blank=True, max_length=50)
    tags        = models.ManyToManyField(Tag, verbose_name="Tags", blank=True)

class Annotation(models.Model):
    content     = models.TextField('Contenu')
    author      = models.ForeignKey(User, verbose_name="Auteur", null=True, on_delete=models.SET_NULL)
    date        = models.DateTimeField('Date')
    task        = models.ForeignKey(Task, verbose_name="Tâche", on_delete=models.CASCADE)
