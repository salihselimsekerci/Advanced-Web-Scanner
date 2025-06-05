import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import sys
import argparse

# Zafiyet test payloadları
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "'><img src=x onerror=alert(1)>"
]
SQLI_PAYLOADS = [
    "' OR '1'='1", 
    "' UNION SELECT NULL--",
    "' OR 1=1--"
]
HEADERS_TO_CHECK = ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"]

# Formları çek

def get_forms(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")
        return soup.find_all("form")
    except:
        return []

# Form detaylarını al (action, method, inputlar)

def form_details(form):
    details = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details

# Form gönderimi (XSS testi için)

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        if input["type"] == "text" or input["type"] == "search":
            data[input["name"]] = payload
    if form_details['method'] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

# XSS zafiyet taraması yap

def scan_xss(url):
    forms = get_forms(url)
    for form in forms:
        details = form_details(form)
        for payload in XSS_PAYLOADS:
            response = submit_form(details, url, payload)
            if payload in response.text:
                print(f"[!] XSS bulundu: {url} -> {payload}")

# SQL Injection zafiyet taraması yap

def scan_sqli(url):
    for payload in SQLI_PAYLOADS:
        target = f"{url}?id={payload}"
        try:
            res = requests.get(target)
            errors = ["you have an error in your sql syntax", "mysql_fetch", "sql syntax"]
            if any(error in res.text.lower() for error in errors):
                print(f"[!] SQL Injection bulundu: {target}")
        except:
            continue

# HTTP response header kontrolleri

def check_headers(url):
    try:
        res = requests.get(url)
        print("[+] Header Kontrolü:")
        for header in HEADERS_TO_CHECK:
            if header in res.headers:
                print(f"  [+] {header}: {res.headers[header]}")
            else:
                print(f"  [!] Eksik header: {header}")
    except:
        print("[-] Header kontrolü başarısız.")

# Ana fonksiyon - komut satırından URL alır ve tüm testleri başlatır

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Hedef URL")
    args = parser.parse_args()
    url = args.url
    if not url.startswith("http"):
        url = "http://" + url

    print("[+] Header güvenlik denetimi başlıyor...")
    check_headers(url)

    print("\n[+] XSS taraması başlıyor...")
    scan_xss(url)

    print("\n[+] SQL Injection taraması başlıyor...")
    scan_sqli(url)

if __name__ == "__main__":
    main()
