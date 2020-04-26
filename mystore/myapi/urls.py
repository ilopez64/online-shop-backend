# myapi/urls.py

from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'discount', views.DiscountViewSet)
router.register(r'item', views.ItemViewSet)
router.register(r'purchase', views.PurchaseViewSet)
router.register(r'purchaseditem', views.PurchasedItemViewSet)
router.register(r'login',views.LoginViewSet,basename='login')
router.register(r'purchasehistory',views.PurchaseHistoryViewSet,basename='purchasehistory')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here

]
