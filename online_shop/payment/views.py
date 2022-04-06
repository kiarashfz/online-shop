import logging
from django.urls import reverse, reverse_lazy
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = 50000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(
            bank_models.BankType.IDPAY)  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url('/payment/callback/')
        # bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return redirect('customers:dashboard')

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
#
# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://localhost:8000/payment/verify/'
#
#
# def send_request(request):
#     req_data = {
#         "merchant_id": MERCHANT,
#         "amount": amount,
#         "callback_url": CallbackURL,
#         "description": description,
#         "metadata": {"mobile": mobile, "email": email}
#     }
#     req_header = {"accept": "application/json",
#                   "content-type": "application/json'"}
#     req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
#         req_data), headers=req_header)
#     authority = req.json()['data']['authority']
#     if len(req.json()['errors']) == 0:
#         return redirect(ZP_API_STARTPAY.format(authority=authority))
#     else:
#         e_code = req.json()['errors']['code']
#         e_message = req.json()['errors']['message']
#         return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#
#
# def verify(request):
#     t_status = request.GET.get('Status')
#     t_authority = request.GET['Authority']
#     if request.GET.get('Status') == 'OK':
#         req_header = {"accept": "application/json",
#                       "content-type": "application/json'"}
#         req_data = {
#             "merchant_id": MERCHANT,
#             "amount": amount,
#             "authority": t_authority
#         }
#         req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
#         if len(req.json()['errors']) == 0:
#             t_status = req.json()['data']['code']
#             if t_status == 100:
#                 return HttpResponse('Transaction success.\nRefID: ' + str(
#                     req.json()['data']['ref_id']
#                 ))
#             elif t_status == 101:
#                 return HttpResponse('Transaction submitted : ' + str(
#                     req.json()['data']['message']
#                 ))
#             else:
#                 return HttpResponse('Transaction failed.\nStatus: ' + str(
#                     req.json()['data']['message']
#                 ))
#         else:
#             e_code = req.json()['errors']['code']
#             e_message = req.json()['errors']['message']
#             return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#     else:
#         return HttpResponse('Transaction failed or canceled by user')


# from django.http import HttpResponse
# from django.shortcuts import redirect
# # from suds.client import Client
#
#
# MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required
# ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
# amount = 1000  # Amount will be based on Toman  Required
# description = u'توضیحات تراکنش تستی'  # Required
# email = 'user@userurl.ir'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://127.0.0.1:8000/verify/'
#
#
# def send_request(request):
#     client = Client(ZARINPAL_WEBSERVICE)
#     result = client.service.PaymentRequest(MMERCHANT_ID,
#                                            amount,
#                                            description,
#                                            email,
#                                            mobile,
#                                            CallbackURL)
#     if result.Status == 100:
#         return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
#     else:
#         return HttpResponse('Error')
#
#
# def verify(request):
#     client = Client(ZARINPAL_WEBSERVICE)
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MMERCHANT_ID,
#                                                     request.GET['Authority'],
#                                                     amount)
#         if result.Status == 100:
#             return HttpResponse('Transaction success. RefID: ' + str(result.RefID))
#         elif result.Status == 101:
#             return HttpResponse('Transaction submitted : ' + str(result.Status))
#         else:
#             return HttpResponse('Transaction failed. Status: ' + str(result.Status))
#     else:
#         return HttpResponse('Transaction failed or canceled by user')
