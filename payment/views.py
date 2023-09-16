# payment/views.py
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from sslcommerz_python.payment import SSLCSession
from django.conf import settings
import json
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt


def initiate_payment(request):
    
    if request.method == 'POST':
        print("Payment calling")
        
        # Retrieve payment data from the form or your database
        total_amount = 100  # Replace with your actual amount
        currency = 'BDT'    # Replace with your currency
        transaction_id = '12345'  # Replace with a unique transaction ID
        sslc = SSLCSession(
            sslc_is_sandbox=True,  # Set this to False in production
            sslc_store_id=settings.SSL_COMMERZ_STORE_ID,
            sslc_store_pass=settings.SSL_COMMERZ_STORE_PASSWORD,
        )
        sslc_status_url = request.build_absolute_uri( reverse('sslc_status') )
        print("status url", sslc_status_url)
        sslc.set_urls(success_url=sslc_status_url, fail_url=sslc_status_url, cancel_url=sslc_status_url, ipn_url=sslc_status_url)
        sslc.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')
        sslc.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')
        sslc.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')
        # If you want to post some additional values
        sslc.set_additional_values(value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d='uuid')

        response_data = sslc.init_payment()
        print("response_data: ", response_data)
        
        if response_data.get('GatewayPageURL'):
            print("redirecting to gateway")
            print("response_data: ", response_data['GatewayPageURL'])
            # return HttpResponseRedirect(response_data['GatewayPageURL'])
            
            return HttpResponseRedirect(response_data['GatewayPageURL'])
            print("redirected to gateway")
        else:
            return HttpResponse("Payment initiation failed")
    
    return render(request, 'payment/initiate_payment.html')

def payment_success(request):
    # Handle successful payment here
    return render(request, 'payment/success.html')

def payment_failure(request):
    # Handle failed payment here
    return render(request, 'payment/failure.html')

def payment_cancel(request):
    # Handle canceled payment here
    return render(request, 'payment/cancel.html')

@csrf_exempt
def sslc_status(request):
    if request.method == 'POST':
        data = request.POST
        print("data: ", data)
        status = data['status']
        if status == 'VALID':
            val_id = data['val_id']
            tran_id = data['tran_id']
            return HttpResponseRedirect(reverse('sslc_complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))

    return render(request, 'pament/status.html', {})


def sslc_complete(request, val_id, tran_id):
    return HttpResponse("OK")