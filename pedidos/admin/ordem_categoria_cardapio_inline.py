from django.contrib import admin

from ..models.ordem_categoria_cardapio import OrdemCategoriaCardapio 



class OrdemCategoriaCardapioInline(admin.TabularInline):
    model = OrdemCategoriaCardapio
    extra = 0

    
    
    