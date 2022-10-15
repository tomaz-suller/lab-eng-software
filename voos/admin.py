from django.contrib import admin  # noqa: F401

from .models import Estado, CompanhiaAerea, Voo, InstanciaVoo, Movimentacao

admin.site.register(Estado)
admin.site.register(CompanhiaAerea)
admin.site.register(Voo)
admin.site.register(InstanciaVoo)
admin.site.register(Movimentacao)
