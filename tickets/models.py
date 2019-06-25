from django.db import models
import uuid

class Project(models.Model):
    name        = models.CharField('Projet')
    shortname   = models.CharField('Identifiant')
    description = models.TextField('Description')

class Annotation(models.Model):
    content     = models.TextField('Contenu')
    author      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date        = models.DateTimeField('Date')
    task        = models.ForeignKey(Task, on_delete=models.CASCADE)

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
    status      = models.CharField('Status', choices=STATUS_CHOICES, default='pending')
    autor       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)
    depends     = models.ManyToManyField("self",symmetrical=False)
    entry       = models.DateTimeField('Date de créaton', blank=False)
    due         = models.DateTimeField('Date d\'échéance', blank=True)
    start       = models.DateTimeField('Date de début', blank=True)
    end         = models.DateTimeField('date de fin', blank=True)
    until       = models.DateTimeField('Date de fin de récurrence', blank=True)
    scheduled   = models.DateTimeField('Date prévue', blank=True)
    wait        = models.DateTimeField('Date d\'attente', blank=True)
    modified    = models.DateTimeField('Date de modification', blank=False)
    recur       = models.CharField('Périodicité', blank=True)
    mask        = models.CharField('Masque', blank=True)
    imask       = models.IntegerField('Indice de masque', blank=True)
    parent      = models.ForeignKey('self', symmetrical=False, on_delete=models.CASCADE, blank=True)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    priority    = models.CharField('Priorité', blank=True)
    tags        = models.ManyToManyField(Tag, blank=True)

class Tag(models.Model):
    name        = models.CharField('Tag')
    description = models.TextField('Description')

class Uda(models.Model):
    name        = models.CharField('Attribut')
    description = models.TextField('Description')
    value       = models.TextField('Valeur')
