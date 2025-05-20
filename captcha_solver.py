import requests
import time

class CaptchaSolver2Captcha:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://2captcha.com"

    def solve_recaptcha(self, site_key, page_url):
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        resp = requests.post(f"{self.base_url}/in.php", data=payload).json()
        if resp["status"] != 1:
            raise Exception(f"CAPTCHA submission failed: {resp}")
        captcha_id = resp["request"]

        for _ in range(20):
            time.sleep(5)
            res = requests.get(f"{self.base_url}/res.php?key={self.api_key}&action=get&id={captcha_id}&json=1").json()
            if res["status"] == 1:
                return res["request"]
        raise Exception("CAPTCHA solve timeout")
