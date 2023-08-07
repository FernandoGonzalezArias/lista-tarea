from django.db import models

class Tarea(models.Model):
    titulo = models.CharField(max_length=64, blank = False, null = False, default = "---")
    estado = models.BooleanField(default=0)
