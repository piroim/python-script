from module.imports import * 
from extract.ext_form_test import form_ext2 #잠시 테스트용, 테스트 후 삭제
#requests 요청 간소화
class HTTPClient:
    def __init__(self, base_url="", verify=False):
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update(get_headers())
        self.base_url = base_url.rstrip('/')

    #GET 요청
    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)
    
    #POST 요청
    def post(self, path, data=None, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{path}", data=data, json=json, **kwargs)

def main():
    #HTTPClient 사용
    # client = HTTPClient(base_url="https://lxmma.com/order/")
    # res = client.get("/login.do")
    
    res = requests.get("https://lxmma.com/order/login.do")
    if res.status_code == 200:
        form_ext2(res.text)
    else:
        print(f"Failed to fetch form data: {res.status_code}")

if __name__ == "__main__":
    main()
