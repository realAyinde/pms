from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.urls import reverse

class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(archived=timezone.now())


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).filter(archived__isnull=True)
    
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


# Create your models here.
class BaseModel(models.Model):
    archived = models.DateTimeField(blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = BaseModelManager()

    def archive(self, using=None, keep_parents=False):
        self.archived = timezone.now()
        super(BaseModel, self).save(using=using)

    def delete(self, using=None, keep_parents=False):
        self.archive(using, keep_parents)

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        try:
            if self.title:
                return self.title
        except AttributeError:
            pass
        try:
            if self.name:
                return self.name
        except AttributeError:
            pass
        return ""

    class Meta:
        abstract = True
        ordering = ['-last_modified']
