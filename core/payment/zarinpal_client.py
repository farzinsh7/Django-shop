from django.conf import settings
import requests
import json


class ZarinPalSandBox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, merchant_id=settings.MERCHANT_ID, currency=settings.CURRENCY):
        self.merchant_id = merchant_id
        self.currency = currency

    def payment_request(self, amount, description="پرداخت کاربر سندباکس"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "currency": self.currency,
            "callback_url": self._callback_url,
            "description": description,
            "metadata": {
                "mobile": "09359420403",
                "email": "farzinweb@gmail.com"
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "authority": authority,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(
            self._payment_verify_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def generate_payment_url(self, authority):
        return f"{self._payment_page_url}{authority}"


if __name__ == "__main__":
    zarinpal = ZarinPalSandBox(
        merchant_id="4ced0a1e-4ad8-4309-9668-3ea3ae8e8897")
    response = zarinpal.payment_request(750000)
    print(response)
    input("Proceed to generating Payment URL?")

    print(zarinpal.generate_payment_url(response['data']['authority']))

    input("Check the Payment?")

    response = zarinpal.payment_verify(750000, response['data']['authority'])
    print(response)
