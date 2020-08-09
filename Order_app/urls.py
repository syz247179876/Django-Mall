from rest_framework.routers import DefaultRouter

from Order_app.views.order import personal_order, personal_generate_order
from Order_app.views.order_api import OrderBasicOperation, OrderCommitOperation, OrderBuyNow, OrderListOperation
from User_app.views.personal import personal_change
from django.urls import path, include

app_name = 'Order_app'

urlpatterns = [
    path('personal_order/', personal_order, name='personal_order'),
    path('personal_change/', personal_change, name='personal_change'),
    path('personal_generate_order/', personal_generate_order, name='personal_generate_order'),
    # path('order-refund-chsc-api/', OrderBasicRefund.as_view(), name='order-refund-chsc-api'),
    path('order-buy-now-chsc-api/', OrderBuyNow.as_view(), name='order-buy-now-chsc-api'),
    path('order-get-chsc-api/<str:status>', OrderListOperation.as_view(), name='order-get-chsc-api')
]

router = DefaultRouter()
router.register(r'order-commit-chsc-api', OrderCommitOperation, basename='order-commit')
router.register(r'order-chsc-api', OrderBasicOperation, basename='order')
urlpatterns += router.urls
