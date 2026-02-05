from django.contrib import admin

from .models import (
    Acesso,
    Chamado,
    Email,
    Emprestimo,
    Equipamento,
    IP,
    Insumo,
    Ramal,
    Requisicao,
    Software,
    Usuario,
)

admin.site.register(Usuario)
admin.site.register(Acesso)
admin.site.register(Equipamento)
admin.site.register(IP)
admin.site.register(Email)
admin.site.register(Ramal)
admin.site.register(Software)
admin.site.register(Insumo)
admin.site.register(Requisicao)
admin.site.register(Emprestimo)
admin.site.register(Chamado)

# Register your models here.
