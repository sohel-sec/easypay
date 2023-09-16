# payment/urls.py
from django.urls import path
from payment.views import  (
    initiate_payment,
    payment_success,
    payment_failure,
    payment_cancel,
    sslc_status,
    sslc_complete

)

urlpatterns = [
    path('initiate/', initiate_payment, name='payment_initiate'),
    path('sslc_status/', sslc_status, name='sslc_status'),
    path('sslc_complete/<str:val_id>/<str:tran_id>/', sslc_complete, name='sslc_complete'),
    path('success/', payment_success, name='payment_success'),
    path('failure/', payment_failure, name='payment_failure'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    # Add more URL patterns as needed
]
