from django.contrib import admin
from administrar.models import Tarea

class  TareaAdmin (admin.ModelAdmin):
    list_display = ("titulo", "estado", "descripcion")
    
    def descripcion(self, obj):
        if obj.estado:
            return "Completado"
        else:
            return "Pendiente"

admin.site.register(Tarea, TareaAdmin)