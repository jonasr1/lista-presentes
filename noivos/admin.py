from django.contrib import admin
from noivos.models import Convidados, Presentes
    
@admin.register(Presentes)
class PresenteAdmin(admin.ModelAdmin):
    list_display = ('nome_presente', 'preco', 'foto', 'importancia')  # Configura as colunas visíveis
    search_fields = ('nome_presente',)                                # Adiciona barra de pesquisa
    list_filter = ('preco',)                                          # Adiciona filtros laterais
    ordering = ('preco',)                                             # Define a ordem padrão de exibição
    
@admin.register(Convidados)
class ConvidadosAdmin(admin.ModelAdmin):
    list_display = ('nome_convidado', 'whatsapp', 'maximo_acompanhantes')
    