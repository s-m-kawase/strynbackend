from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from core.api.viewsets.profile_viewset import ProfileViewSet
from core.api.viewsets.user_viewset import UserViewSet
from pagamentos.api.viewsets.adicional_viewset import AdicionalViewSet
from pagamentos.api.viewsets.cupom_viewset import CupomViewSet
from pagamentos.api.viewsets.pagamento_viewset import PagamentoViewSet
from pedidos.api.viewsets.cardapio_viewset import CardapioViewSet
from pedidos.api.viewsets.categoria_cadarpio_viewset import CategoriaCardapioViewSet
from pedidos.api.viewsets.cliente_viewset import ClienteViewSet
from pedidos.api.viewsets.complemento_viewset import ComplementosViewSet
from pedidos.api.viewsets.grupo_complemento_viewset import GrupoComplementosViewSet
from pedidos.api.viewsets.item_pedido_complemento_viewset import ItensPedidoComplementosViewSet
from pedidos.api.viewsets.item_pedido_viewset import ItensPedidoViewSet
from pedidos.api.viewsets.item_cardapio_viewset import ItemCardapioViewSet
from pedidos.api.viewsets.pedido_viewset import PedidosViewSet
from pedidos.api.viewsets.restaurante_viewset import RestauranteViewSet
from pedidos.api.viewsets.tempo_estimado_viewset import TempoEstimadoViewSet
from pedidos.api.viewsets.ordem_categoria_cardapio_view import OrdemCategoriaCardapioViewSet
from pedidos.api.viewsets.cardapio_com_ordem_viewset import CardapioComOrdemViewSet
from apistripe.api.viewset.config_stripe_viewset import ConfigStripeViewSet
# from apistripe.api.viewset.price_viewset import PriceViewSet
# from apistripe.api.viewset.produto_viewset import ProdutoViewSet
from pedidos.api.viewsets.webhook_viewset import StripeWebhookViewSet
from pedidos.api.viewsets.webhook_asaas import AsaasWebhookViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario'),
router.register(r'profile', ProfileViewSet, basename='profile'),

router.register(r'pagamento', PagamentoViewSet, basename='pagamento'),
router.register(r'cupom', CupomViewSet, basename='cupom'),
router.register(r'adicional', AdicionalViewSet, basename='adicional'),


router.register(r'cardapio', CardapioViewSet, basename='cardapio'),
router.register(r'categoria_cardapio', CategoriaCardapioViewSet, basename='categoria_cardapio'),
router.register(r'cliente', ClienteViewSet, basename='cliente'),
router.register(r'complemento', ComplementosViewSet, basename='complemento'),
router.register(r'grupo_complemento', GrupoComplementosViewSet, basename='grupo_complemento'),
router.register(r'item_cardapio', ItemCardapioViewSet, basename='item'),
router.register(r'item_complemento', ItensPedidoComplementosViewSet, basename='item_complemento'),
router.register(r'item_pedido', ItensPedidoViewSet, basename='item_pedido'),
router.register(r'pedido', PedidosViewSet, basename='pedido'),
router.register(r'restaurante', RestauranteViewSet, basename='restaurante'),
router.register(r'tempo', TempoEstimadoViewSet, basename='tempo'),
router.register(r'ordem_categoria_cardapio', OrdemCategoriaCardapioViewSet, basename='ordem_categoria_cardapio'),
router.register(r'cardapio_com_ordem', CardapioComOrdemViewSet, basename='cardapio_com_ordem'),

router.register(r'Config_stripe', ConfigStripeViewSet, basename='Config_stripe'),
# router.register(r'produto', ProdutoViewSet, basename='produto'),
# router.register(r'price', PriceViewSet, basename='price'),
router.register(r'webhook', StripeWebhookViewSet, basename='webhook')
router.register(r'webhook_asaas', AsaasWebhookViewSet, basename='webhook_asaas')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_app_novadata.urls')),
    path ("accounts/",  include ( "django.contrib.auth.urls" ),name='login'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/webhook/', StripeWebhookViewSet.as_view({'post': 'webhook'}), name='webhook'),
    path('api/webhook_asaas/', AsaasWebhookViewSet.as_view({'post': 'webhook'}), name='webhook_asaas'),
    # path('webhook2/',stripe_webhook,name='webhook'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
    path('api/', include(router.urls)),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('djoser.urls')),
    path(r'^_nested_admin/', include('nested_admin.urls')),
    # path('create-checkout-session', create_checkout_session , name='create_checkout_session' ),
     path('advanced_filters/', include('advanced_filters.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)