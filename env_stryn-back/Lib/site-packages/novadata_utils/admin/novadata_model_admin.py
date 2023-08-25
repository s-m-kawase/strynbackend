from functools import partial

from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django_object_actions import DjangoObjectActions
from import_export.admin import ImportExportMixin

from novadata_utils.functions import get_prop, transform_field


class NovadataModelAdmin(
    AdminAdvancedFiltersMixin,
    ImportExportMixin,
    DjangoObjectActions,
    admin.ModelAdmin,
):
    """
    Classe para realizar funcionalidades default em todas as classes do admin.

    A mesma adiciona todos os campos possíveis nas seguintes propriedades:
    - list_display
    - list_filter
    - autocomplete_fields
    - filter_horizontal
    """

    list_display: list = []

    search_fields: list = []

    list_filter: list = []

    autocomplete_fields: list = []

    list_select_related: list = []

    auto_search_fields: bool = True

    filter_horizontal: list = []

    exclude: list = []

    def get_list_display(self, request):
        """Retorna a lista de campos que estarão na listagem."""
        super().get_list_display(request)

        if not self.list_display:
            model = self.model
            list_display = get_prop(model, "list_display")

            return list_display
        else:
            return self.list_display

    def get_search_fields(self, request):
        """Retorna a lista de campos que estarão no campo de busca."""
        super().get_search_fields(request)

        if self.auto_search_fields and not self.search_fields:
            model = self.model
            search_fields = get_prop(model, "search_fields")

            return search_fields
        else:
            return self.search_fields

    def get_list_filter(self, request):
        """Retorna a lista de campos que estarão no filtro."""
        super().get_list_filter(request)

        if not self.list_filter:
            model = self.model
            foreign_keys = get_prop(model, "foreign_keys")
            choices_fields = get_prop(model, "choices_fields")

            list_filter_fields = get_prop(model, "list_filter")

            transform_foreign_keys = partial(
                transform_field,
                foreign_keys,
                "foreign_keys",
            )
            transform_choices_fields = partial(
                transform_field,
                choices_fields,
                "choices_fields",
            )

            list_filter = list(map(transform_foreign_keys, list_filter_fields))
            list_filter = list(map(transform_choices_fields, list_filter))

            return list_filter
        else:
            return self.list_filter

    def get_autocomplete_fields(self, request):
        """Retorna a lista de campos que estarão no autocomplete."""
        super().get_autocomplete_fields(request)

        if not self.autocomplete_fields:
            model = self.model
            autocomplete_fields = get_prop(model, "autocomplete_fields")

            return autocomplete_fields
        else:
            return self.autocomplete_fields

    def get_list_select_related(self, request):
        """Retorna a lista de campos que estarão no select_related."""
        super().get_list_select_related(request)

        if not self.list_select_related:
            model = self.model
            list_select_related = get_prop(model, "list_select_related")

            return list_select_related
        else:
            return self.list_select_related

    def get_filter_horizontal(self):
        """Retorna a lista de campos que estarão no filtro horizontal."""
        if not self.filter_horizontal:
            model = self.model
            filter_horizontal = get_prop(model, "filter_horizontal")

            return filter_horizontal
        else:
            return self.filter_horizontal

    def get_exclude(self, request, obj=None):
        """Retorna a lista de campos que estarão no exclude."""
        exclude_fields = [super().get_exclude(request, obj)]
        exclude_fields += self.exclude
        exclude_fields += [
            "usuario_criacao",
            "usuario_atualizacao",
            "created_by",
            "updated_by",
        ]

        return exclude_fields

    def __init__(self, *args, **kwargs):
        """Método para executarmos ações ao iniciar a classe."""
        super().__init__(*args, **kwargs)
        self.filter_horizontal = self.get_filter_horizontal()
