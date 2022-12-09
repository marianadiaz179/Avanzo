from django.db import models

class Credito(models.Model):
    infoAnalisis =  models.CharField(max_length=50)
    solicitud = models.FloatField(null=True, blank=True, default=None)
    cliente = models.IntegerField(null=False, default=None)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)