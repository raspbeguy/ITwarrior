from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    """This is a user wrapping class for later use."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()


class Project(models.Model):
    name        = models.CharField('projet', max_length=50)
    shortname   = models.CharField('identifiant', max_length=50)
    description = models.TextField('description')
    parent      = models.ForeignKey('self', verbose_name="parent", blank=True, null=True, on_delete=models.CASCADE)

    def fully_qualified_name(self):
        return self.shortname if self.parent is None else self.parent.fully_qualified_name()+'.'+self.shortname

    def __str__(self):
        return self.fully_qualified_name()


class Tag(models.Model):
    name        = models.CharField('tag', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('deleted', 'Deleted'),
            ('waiting', 'Waiting'),
            ('recurring', 'Recurring'),
            ]
    description = models.TextField('description', blank=False)
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    status      = models.CharField('status', choices=STATUS_CHOICES, default='pending', max_length=9)
    autor       = models.ForeignKey(Profile, verbose_name="auteur", null=True, on_delete=models.SET_NULL, blank=True)
    depends     = models.ManyToManyField("self", verbose_name="dépendances", symmetrical=False, blank=True, related_name="task_depends")
    entry       = models.DateTimeField('date de créaton', blank=False)
    due         = models.DateTimeField('date d\'échéance', blank=True)
    start       = models.DateTimeField('date de début', blank=True)
    end         = models.DateTimeField('date de fin', blank=True)
    until       = models.DateTimeField('date de fin de récurrence', blank=True)
    scheduled   = models.DateTimeField('date prévue', blank=True)
    wait        = models.DateTimeField('date d\'attente', blank=True)
    modified    = models.DateTimeField('date de modification', blank=False)
    recur       = models.CharField('périodicité', blank=True, max_length=50)
    mask        = models.CharField('masque', blank=True, max_length=256)
    imask       = models.IntegerField('indice de masque', blank=True)
    parent      = models.ForeignKey('self', verbose_name="parent", on_delete=models.CASCADE, blank=True, related_name="task_parent")
    project     = models.ForeignKey(Project, verbose_name="projet", on_delete=models.CASCADE, blank=True)
    priority    = models.CharField('priorité', blank=True, max_length=50)
    tags        = models.ManyToManyField(Tag, verbose_name="tags", blank=True)

class Annotation(models.Model):
    content     = models.TextField('contenu')
    author      = models.ForeignKey(Profile, verbose_name="auteur", null=True, on_delete=models.SET_NULL)
    date        = models.DateTimeField('date')
    task        = models.ForeignKey(Task, verbose_name="tâche", on_delete=models.CASCADE)


class UdaDef(models.Model):
    name        = models.CharField('attribut', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return self.name


class UdaVal(models.Model):
    value       = models.TextField('valeur')
    definition  = models.ForeignKey(UdaDef, verbose_name="définition", on_delete=models.PROTECT)
    task        = models.ForeignKey(Task, verbose_name="tâche", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.task+":"+self.definition
