import base64
import json
from datetime import datetime
from urllib.parse import quote_plus

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class AliPay(object):

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):

        self.appid = appid
        self.app_notify_url = app_notify_url
        self.return_url = return_url
        self.app_private_key_path = app_private_key_path
        self.alipay_public_key_path = alipay_public_key_path

        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            self.gateway = 'https://openapi.alipaydev.com/gateway.do'
        else:
            self.gateway = ''

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):

        # 支付 业务参数
        biz_content = {
            'subject': subject,
            'out_trade_no': out_trade_no,
            'total_amount': total_amount,
            'product_code': "FAST_INSTANT_TRADE_PAY",
        }
        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def direct_query(self, out_trade_no, trade_no):
        biz_content = {
            'out_trade_no', out_trade_no,
            'trade_no', trade_no
        }
        data = self.build_body("alipay.trade.query", biz_content)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }
        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url
        return data

    def sign_data(self, data):
        data.pop('sign', None)
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))
        return sorted([k, v] for k, v in data.items())

    def sign(self, unsigned_string):
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, base64.decodestring((signature.encode("utf8")))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)



















