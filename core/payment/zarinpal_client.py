class ZarinPalSandBox:
    payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def payment_request(self,):
        pass

    def payment_verify(self,):
        pass

    def generate_payment_url(self,):
        pass
