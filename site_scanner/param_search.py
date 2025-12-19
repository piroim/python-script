# param_search.py
import argparse, requests, re, time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs, urljoin 
from bs4 import BeautifulSoup

class webscan:
    def __init__(self, url):
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/91.0.4472.124 Safari/537.36')
        }
        self.url = url

    def extract_urls(self):
        res = requests.get(url=self.url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        extracted_urls = []

        # <form> 처리 (method 지정 없으면 GET)
        for form in soup.find_all("form"):
            method = (form.get("method") or "GET").upper()
            action = form.get("action") or self.url
            action_url = action if action.startswith("http") else urljoin(self.url, action)

            fields = []
            for inp in form.find_all("input"):
                name = inp.get("name") or inp.get("id")
                if name:
                    fields.append(name)

            extracted_urls.append({"method": method, "url": action_url, "fields": fields})

        # <form> 밖의 <input> → GET으로
        for inp in soup.find_all("input"):
            if inp.find_parent("form") is None:
                name = inp.get("name") or inp.get("id")
                if name:
                    extracted_urls.append({"method": "GET", "url": self.url, "fields": [name]})

        return extracted_urls

    def status_urls(self, extracted_urls):
        '''
            GET/POST 요청을 수행한 상태코드를 가져오는 함수    
        '''
        # print("  ///========================================================================///")
        # print(" ///                             GET/POST 요청결과                          ///")
        # print("///========================================================================///\033[0m")

        for target in extracted_urls:
            method = target["method"]
            url = target["url"]
            fields = target["fields"]
            try:
                if method == "POST":
                    data = {k: "" for k in fields}
                    res = requests.post(url, headers=self.headers, data=data, timeout=10)
                else:
                    params = {k: "" for k in fields}
                    res = requests.get(url, headers=self.headers, params=params, timeout=10)

                status = res.status_code
                # 상태코드 색상
                if status // 100 == 2:
                    color = "\033[92m"
                elif status // 100 == 3:
                    color = "\033[94m"
                elif status // 100 == 4:
                    color = "\033[93m"
                elif status // 100 == 5:
                    color = "\033[91m"
                else:
                    color = "\033[0m"

                # 메서드 색: GET=초록, POST=파랑
                method_color = "\033[94m" if method == "POST" else "\033[92m"

                param_str = f" {fields}" if fields else ""
                print(f"{method_color}[STATUS: {status}][{method}]\033[0m : {res.url}  param:{param_str}")
            except requests.RequestException as e:
                print(f"\033[90m[STATUS: ERR][{method}]\033[0m : [{url}] — error={e}")

        # print("========================================================================")

# 모듈 호출용 래퍼 (api_scan.py에서 사용)
def run_for_url(url: str):
    '''
        주어진 URL 하나에 대해 추출→요청→출력까지 실행
    '''
    # print(f"[DEBUG] run_for_url() called with: {url}")
    scan = webscan(url)
    # print(f"[DEBUG] scan type: {type(scan)}")
    extracted = scan.extract_urls()
    if not extracted:
        extracted = [{"method": "GET", "url": url, "fields": []}]
    scan.status_urls(extracted)
