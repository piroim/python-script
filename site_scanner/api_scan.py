#!/usr/bin/env python3
import argparse, json, sys, time, traceback
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from param_search import run_for_url #모듈적용

def get_driver(driver_path=None, no_headless=False):
    options = Options()
    if not no_headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    if driver_path:
        try:
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception:
            traceback.print_exc()

    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception:
        print("[WARN] Selenium Manager 방식 실패, webdriver-manager로 시도")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception:
        traceback.print_exc()

    print("\n[ERROR] Could not start Chrome WebDriver.")
    sys.exit(1)


def scan_resources(url, driver_path=None, no_headless=False, wait_time=5):
    driver = get_driver(driver_path=driver_path, no_headless=no_headless)

    try:
        # CDP 네트워크 추적 활성화
        driver.execute_cdp_cmd("Network.enable", {})
        driver.get(url)

        # JS파일 정적/동적 호출 대기시간 설정
        time.sleep(wait_time)

        # Performance 로그에서 요청 수집
        raw_logs = driver.get_log("performance")
        resources = []
        for entry in raw_logs:
            try:
                message = json.loads(entry["message"])["message"]
                # Network.requestWillBeSent 이벤트만
                if message.get("method") == "Network.requestWillBeSent":
                    req = message.get("params", {}).get("request")
                    if req and "url" in req:
                        resources.append(req["url"])
            except Exception:
                continue

    except Exception as e:
        print("[ERROR] driver.get() or CDP failed:", str(e))
        driver.quit()
        return

    driver.quit()

    # 블랙리스트 설정, data:image, fonts 제외
    exclude_keywords = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".woff")
    filtered = [r for r in set(resources)
                if all(ext not in r.lower() for ext in exclude_keywords)
                and not r.lower().startswith("data:image")
                and "fonts" not in r.lower()]

    # 항목별 그룹화
    base_netloc = urlparse(url).netloc
    # print(base_url)
    # print(base_netloc)
    js_list = sorted([r for r in filtered if ".js" in r.lower()])
    css_list = sorted([r for r in filtered
                       if r.lower().endswith(".css") or "/css/" in r.lower() or r.lower().endswith("css")])
    # api_list = sorted([r for r in filtered
    #                    if ("/api/" in r.lower() or "?" in r) and r not in js_list + css_list])
    api_list = sorted([r for r in filtered if r not in js_list + css_list])
    others_url = sorted([r for r in filtered if r not in js_list + css_list
                        and urlparse(r).netloc != ""
                        and urlparse(r).netloc != base_netloc
                    ])

    # 출력
    print("\n Found resources (excluding images, data:image, fonts, total {}):".format(len(filtered)))

    print(f"\n\033[93m--- JavaScript Files (.js included) [{len(js_list)}] ---\033[0m")
    for r in js_list:
        print(r)

    # print(f"\n\033[94m--- CSS Files (.css, /css/ or ending with css) [{len(css_list)}] ---\033[0m")
    # for r in css_list:
    #     print(r)

    print(f"\n\033[95m--- API Requests [{len(api_list)}] ---\033[0m")
    for r in api_list:
        run_for_url(r)

    print(f"\n\033[92m--- Other URLs [{len(others_url)}] ---\033[0m")
    for r in others_url:
        run_for_url(r)


def main():
    parser = argparse.ArgumentParser(description="CDP Resource Scanner - JS/CSS/API/Other, excluding images, data:image, fonts")
    parser.add_argument("-u", "--url", required=True, help="Scan target URL")
    parser.add_argument("-d", "--driver-path", default=None, help="Optional chromedriver.exe full path")
    parser.add_argument("--no-headless", action="store_true", help="Run browser with GUI (not headless)")
    parser.add_argument("--wait", type=int, default=5, help="Wait seconds after page load for dynamic requests")
    args = parser.parse_args()

    scan_resources(args.url, driver_path=args.driver_path, no_headless=args.no_headless, wait_time=args.wait)


if __name__ == "__main__":
    main()
