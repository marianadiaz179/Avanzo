from django.db import models

class Cliente(models.Model):
    name =  models.CharField(max_length=50)
    cedula = models.FloatField(null=True, blank=True, default=None)
    empresa = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)