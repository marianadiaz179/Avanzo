from django.db import models

class Solicitud(models.Model):
    idSolicitud = models.FloatField(null=True, blank=True, default=None)
    documento =  models.CharField(max_length=50)
    cliente = models.IntegerField(null=False, default=None)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)