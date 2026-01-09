from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import subscription_views

router = DefaultRouter()
router.register(r'plans', subscription_views.PlanViewSet, basename='plan')
router.register(r'subscription', subscription_views.SubscriptionViewSet, basename='subscription')
router.register(r'fornecedores', subscription_views.FornecedorViewSet, basename='fornecedor')

urlpatterns = [
    path('', include(router.urls)),
    path('upgrade-pro/', subscription_views.upgrade_pro, name='upgrade-pro'),
    path('cancel-subscription/', subscription_views.cancel_subscription, name='cancel-subscription'),
]
