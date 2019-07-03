from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    """This is a user wrapping class for later use."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()


class Project(models.Model):
    name        = models.CharField('projet', max_length=50)
    shortname   = models.CharField('sous-dentifiant', max_length=50)
    fullname    = models.CharField('identifiant', max_length=50, primary_key=True)
    description = models.TextField('description', blank=True, default="")
    parent      = models.ForeignKey('self', verbose_name="parent", related_name="children", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname

    def to_dict(self):
        result = {}
        taskset = self.task_set.all()
        children = self.children.all()
        if taskset:
            result['tasks'] = list(taskset)
        if children:
            for child in children:
                childresult = child.to_dict()
                if childresult:
                    result['children'] = childresult
        if result:
            result['name'] = self.shortname
        return result

    def to_list(self, prefix=None):
        result = []
        taskset = self.task_set.all()
        children = self.children.all()
        if prefix:
            newprefix = prefix + "." + self.shortname
        else:
            newprefix = self.shortname
        if taskset:
            result = [(newprefix, list(taskset))]
        if children:
            for child in children:
                result += child.to_list(prefix=newprefix)
        return result

    @classmethod
    def get_or_new(cls, fullname):
        if fullname:
            try:
                return cls.objects.get(fullname=fullname)
            except cls.DoesNotExist:
                splitted = fullname.rsplit('.', 1)
                try:
                    shortname = splitted[1]
                    parent = cls.get_or_new(splitted[0])
                except IndexError:
                    shortname = splitted[0]
                    parent = None
                p = cls(name=shortname, shortname=shortname, fullname=fullname, parent=parent)
                p.save()
                return p
        else:
            return None


class Tag(models.Model):
    name        = models.CharField('tag', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return str(self.name)


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
    entry       = models.DateTimeField('date de création', blank=False, default=timezone.now)
    due         = models.DateTimeField('date d\'échéance', blank=True, null=True)
    start       = models.DateTimeField('date de début', blank=True, null=True)
    end         = models.DateTimeField('date de fin', blank=True, null=True)
    until       = models.DateTimeField('date de fin de récurrence', blank=True, null=True)
    scheduled   = models.DateTimeField('date prévue', blank=True, null=True)
    wait        = models.DateTimeField('date d\'attente', blank=True, null=True)
    modified    = models.DateTimeField('date de modification', blank=False, null=True)
    recur       = models.CharField('périodicité', blank=True, max_length=50)
    mask        = models.CharField('masque', blank=True, max_length=256)
    imask       = models.IntegerField('indice de masque', blank=True, null=True)
    parent      = models.ForeignKey('self', verbose_name="parent", on_delete=models.CASCADE, blank=True, related_name="task_parent", null=True)
    project     = models.ForeignKey(Project, verbose_name="projet", on_delete=models.CASCADE, blank=True, null=True)
    priority    = models.CharField('priorité', blank=True, max_length=50)
    tags        = models.ManyToManyField(Tag, verbose_name="tags", blank=True)

    def __str__(self):
        return str(self.uuid)

class Annotation(models.Model):
    content     = models.TextField('contenu')
    author      = models.ForeignKey(Profile, verbose_name="auteur", null=True, on_delete=models.SET_NULL)
    date        = models.DateTimeField('date', blank=False, default=timezone.now)
    task        = models.ForeignKey(Task, verbose_name="tâche", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)


class UdaDef(models.Model):
    name        = models.CharField('attribut', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return str(self.name)


class UdaVal(models.Model):
    value       = models.TextField('valeur')
    definition  = models.ForeignKey(UdaDef, verbose_name="définition", on_delete=models.PROTECT)
    task        = models.ForeignKey(Task, verbose_name="tâche", on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.task)+":"+str(self.definition)
