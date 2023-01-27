from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from core.api.viewsets.profile_viewset import *
from pagamentos.api.viewsets.adicional_viewset import *
from pagamentos.api.viewsets.cupom_viewset import *
from pagamentos.api.viewsets.pagamento_viewset import *
from pedidos.api.viewsets.cardapio_viewset import *
from pedidos.api.viewsets.categoria_cadarpio_viewset import *
from pedidos.api.viewsets.cliente_viewset import *
from pedidos.api.viewsets.complemento_viewset import *
from pedidos.api.viewsets.grupo_complemento_viewset import *
from pedidos.api.viewsets.item_pedido_complemento_viewset import *
from pedidos.api.viewsets.item_pedido_viewset import *
from pedidos.api.viewsets.item_viewset import *
from pedidos.api.viewsets.pedido_viewset import *
from pedidos.api.viewsets.restaurante_viewset import *
from pedidos.api.viewsets.tempo_estimado_viewset import *

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile'),

router.register(r'pagamento', PagamentoViewSet, basename='pagamento'),
router.register(r'cupom', CupomViewSet, basename='cupom'),
router.register(r'adicional', AdicionalViewSet, basename='adicional'),


router.register(r'cardapio', CardapioViewSet, basename='cardapio'),
router.register(r'categoria_cardapio', CategoriaCardapioViewSet, basename='categoria_cardapio'),
router.register(r'cliente', ClienteViewSet, basename='cliente'),
router.register(r'complemento', ComplementosViewSet, basename='complemento'),
router.register(r'grupo_complemento', GrupoComplementosViewSet, basename='grupo_complemento'),
router.register(r'item', ItemCardapioViewSet, basename='item'),
router.register(r'item_complemento', ItensPedidoComplementosViewSet, basename='item_complemento'),
router.register(r'item_pedido', ItensPedidoViewSet, basename='item_pedido'),
router.register(r'pedido', PedidosViewSet, basename='pedido'),
router.register(r'restaurante', RestauranteViewSet, basename='restaurante'),
router.register(r'tempo', TempoEstimadoViewSet, basename='tempo'),


urlpatterns = [
    path('pagamentos/', include('pagamentos.urls')),
    path('', include('pedidos.urls')),
    path('profile/', include('core.urls')),
    path('admin/', admin.site.urls),
 
    path('api/', include(router.urls)),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)