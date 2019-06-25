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
    description = models.TextField('Description')
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status      = models.CharField('Status', choices=STATUS_CHOICES, default='pending')
    autor       = models.CharField('Auteur')
    depends     = models.ManyToManyField("self",symmetrical=False)
    entry       = models.DateTimeField('Date de créaton')
    due         = models.DateTimeField('Date d\'échéance')
    start       = models.DateTimeField('Date de début')
    end         = models.DateTimeField('date de fin')
    until       = models.DateTimeField('Date de fin de récurrence')
    scheduled   = models.DateTimeField('Date prévue')
    wait        = models.DateTimeField('Date d\'attente')
    modified    = models.DateTimeField('Date de modification')
    recur       = models.CharField('Périodicité')
    mask        = models.CharField('Masque')
    imask       = models.CharField('Indice de masque')
    parent      = models.ForeignKey('self',symmetrical=False, on_delete=models.CASCADE)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE)
    priority    = models.CharField('Priorité')
    tags        = models.ManyToManyField(Tag)

class Tag(models.Model):
    name        = models.CharField('Tag')
    description = models.TextField('Description')

class Uda(models.Model):
    name        = models.CharField('Attribut')
    description = models.TextField('Description')
    value       = models.TextField('Valeur')
