from django.db import models
import uuid as pyuuid

class Task(models.Model):
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('deleted', 'Deleted'),
            ]
    description = models.TextField('Description')
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status      = models.CharField('Status', choices=STATUS_CHOICES, default='pending')
    autor       = models.CharField('Auteur')
    depends     = models.ManyToManyField("self",symmetrical=False)
    entry       = models.DateTimeField('Créaton')
    due         = models.DateTimeField('Échéance')
    end         = models.DateTimeField('Fin')

