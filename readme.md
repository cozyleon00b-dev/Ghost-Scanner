# GHOST SCANNER – OMNI TOOLS X SAVAGE

**All-in-One Security Assessment & Penetration Testing Framework**  
Version 6.0 [BETA] – OMNI TOOLS X SAVAGE  
Release Date: 2026-09-14  
Developer: GhostTeam

---

## OVERVIEW

Ghost Scanner is a modular, high-performance security assessment framework designed for ethical hacking, vulnerability assessment, and authorized stress testing. **No AI** — semua logic native Python, deterministic, dan hasil 100% reproducible. Combines internal engines, 19 external tools, **domain classification (20+ kategori)**, **region detection (IP geo + TLD + NIK + phone)**, **.env full download**, **50+ sensitive patterns**, real DDoS/DoS engine, dan comprehensive reporting (JSON, HTML, PDF).

### Key Capabilities

- **Unified Scan Mode** – satu command `--scan` jalanin SQLi, XSS, WP, Deface, DDoS check, JWT, HTTP Smuggling, GraphQL, OAuth, admin bypass, sensitive data extraction, .env download
- **Domain Classification (20+ kategori)** – Government (Pusat/Daerah), Education (Sekolah/Universitas), Military, Police, Banking/Finance, E-Commerce, News/Media, Medical, Religious, NGO, Adult, Gambling, Social, Jobs, Travel, Food, Gaming, Hosting/Cloud, Technology, Business, Other
- **Region Detection** – IP geolocation (via ip-api.com) + domain TLD + NIK province code + phone carrier prefix + HTML lang → kesimpulan country, city, ISP, ASN, timezone
- **.env Full Download** – otomatis detect + download semua .env variant (.env, .env.local, .env.production, .env.development, .env.backup, .env.old, .env.example, /env), parse KEY=VALUE, extract DB_PASSWORD / SECRET_KEY / API_KEY / JWT_SECRET / STRIPE_SECRET / dll
- **Config Full Download** – wp-config.php, config.php, database.yml, settings.py, docker-compose.yml, .git/config, credentials.json, dll — download full content
- **50+ Sensitive Patterns** – KTP, KK, SIM, BPJS, passport, SSN, credit card, IBAN, SWIFT, crypto wallet (BTC/ETH/XMR/SOL), cloud keys (AWS/GCP/Azure), Stripe, GitHub, Slack, JWT, DB URL, private key, session ID, CSRF token, dll
- **19 External Tools Integration** – Nuclei, Subfinder, httpx, Naabu, Katana, ffuf, sqlmap, Dalfox, Amass, dnsx, gau, waybackurls, Arjun, SecretFinder, Interactsh, Nmap, Metasploit, Wireshark (tshark), BurpSuite
- **Real DDoS/DoS Engine** – socket-based HTTP flood, SYN flood, **Slowloris**, SSL renegotiation, UDP flood, multi-method (all) — real-time stats, no simulation
- **Advanced Web Vulnerability Scanning** – SQLi (1M+ payloads), XSS (context-aware), LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE
- **Deface Detection** – 13+ indicators, title extraction, curl command, verified 2x
- **WordPress Activity Log RCE (CVE-2026-54806)** – detection (auto-skip if not WordPress)
- **Admin Deep Extraction** – form login bypass + SPA/API JSON bypass, authenticated crawl 8+ admin panels, extract PII
- **Employee Data Correlation** – correlate phone/email/NIK/rekening/NPWP/NIP/PIN/sources into per-person records → output PDF
- **NIK Region Decode** – decode 16-digit NIK: province code, regency code, district code, birth date, sex (from digit 7-12)
- **Sensitive Data Per-Category PDF** – 40+ category-specific PDF reports (nik.pdf, ktp_links.pdf, kk_links.pdf, no_rekening.pdf, bank.pdf, phones.pdf, whatsapp.pdf, emails.pdf, pin.pdf, api_keys.pdf, jwt_tokens.pdf, source_code.pdf, admin_users.pdf, employees.pdf, dll)
- **Full PoC** – setiap finding ada: URL + curl + response snippet + status code + time diff + verified flag
- **Proxy Manager v2** – multi-source (ProxyScrape + GitHub lists) + health-check + latency sort + fail counter + auto-retry fallback without proxy
- **WAF Detection** – Cloudflare, Akamai, Sucuri, Imperva, Fastly, Varnish, AWS CloudFront
- **Anti-Ban v3** – adaptive delay berdasarkan response time + jitter + real browser headers + TLS fingerprint (curl-cffi impersonate chrome120)
- **Fast Mode** – `--fast` skip delays, reduce pages, 3-5x lebih cepat
- **Deep Mode** – `--deep` more pages (120), more payloads, lebih thorough
- **Concurrent** – ThreadPoolExecutor untuk harvest, port probe, .env checks, injection scans
- **NO AI** – semua logic deterministic, no external LLM calls, no API key needed, hasil konsisten
- **Cross-Platform** – Windows, Linux (Kali/Ubuntu/Arch/BlackArch), Termux, macOS
- **NO WSL REQUIRED** – works natively on Windows

Ghost Scanner is intended for **authorized testing only**.

---

## TABLE OF CONTENTS

1. [Kali Linux / Debian / Ubuntu Installation](#1-kali-linux--debian--ubuntu-installation)
2. [Arch Linux / BlackArch Installation](#2-arch-linux--blackarch-installation)
3. [Termux (Android) Installation](#3-termux-android-installation)
4. [Windows Installation](#4-windows-installation)
5. [macOS Installation](#5-macos-installation)
6. [Interactive Menu](#interactive-menu)
7. [Usage Examples](#usage-examples)
8. [Domain Classification](#domain-classification)
9. [Region Detection](#region-detection)
10. [.env & Config Download](#env--config-download)
11. [External Tools](#external-tools-integrated)
12. [Output & Reports](#output--reports)
13. [Troubleshooting](#troubleshooting)
14. [Disclaimer](#disclaimer)
15. [Version History](#version-history)

---

## 1. KALI LINUX / DEBIAN / UBUNTU INSTALLATION

### Step 1 – Update System & Install Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git golang-go poppler-utils -y
```

### Step 2 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 3 – **IMPORTANT:** Fix PyFPDF vs fpdf2 conflict

```bash
pip uninstall -y pypdf fpdf fpdf2
pip install --upgrade --force-reinstall fpdf2
pip install -r requirements.txt
```

### Step 4 – Install Python Tools

```bash
pip install sqlmap arjun user-scanner curl-cffi
```

### Step 5 – Install Go Tools

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/ffuf/ffuf/v2@latest
go install github.com/hahwul/dalfox/v2@latest
go install -v github.com/owasp-amass/amass/v5/cmd/amass@main
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
```

### Step 6 – Add GOPATH to PATH

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 7 – Install System Tools

```bash
# Nmap, Wireshark/tshark
sudo apt install nmap wireshark tshark masscan -y

# Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall

# BurpSuite (manual)
# Download dari https://portswigger.net/burp/communitydownload
```

### Step 8 – Verify Installation

```bash
nuclei -version
subfinder -version
nmap --version
sqlmap --version
user-scanner -h
python3 -c "from fpdf import FPDF; print('fpdf2 OK')"
python3 ghostscanner.py -h
```

### Step 9 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --tools --fast
```

---

## 2. ARCH LINUX / BLACKARCH INSTALLATION

### Step 1 – Update & Install Prerequisites

```bash
sudo pacman -Syu
sudo pacman -S python python-pip git go base-devel poppler
```

### Step 2 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 3 – Fix fpdf conflict + install deps

```bash
pip uninstall -y pypdf fpdf fpdf2
pip install --upgrade --force-reinstall --break-system-packages fpdf2
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun user-scanner curl-cffi
```

Atau pakai virtualenv (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install sqlmap arjun user-scanner curl-cffi
```

### Step 4 – Install Go Tools (sama seperti Kali)

### Step 5 – Add GOPATH to PATH

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 – Install System Tools

```bash
sudo pacman -S nmap wireshark-qt masscan
```

### Step 7 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --tools --fast
```

---

## 3. TERMUX (ANDROID) INSTALLATION

### Step 1 – Update & Install Prerequisites

```bash
pkg update && pkg upgrade -y
pkg install python python-pip git golang nmap -y
pip install --upgrade pip
```

### Step 2 – Setup Storage

```bash
termux-setup-storage
```

### Step 3 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 4 – Fix fpdf + install deps

```bash
pip uninstall -y pypdf fpdf fpdf2
pip install --upgrade --force-reinstall --break-system-packages fpdf2
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun user-scanner curl-cffi
```

### Step 5 – Install Go Tools (sama seperti Kali, tapi satu-satu biar gak OOM)

### Step 6 – Add GOPATH to PATH

```bash
export PATH=$PATH:$HOME/go/bin
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 7 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --fast --threads 20
```

**Catatan Termux:** Kurangi thread `--threads 20` biar gak memory error.

---

## 4. WINDOWS INSTALLATION

### Step 1 – Install Python

1. Buka [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11+ Windows installer 64-bit
3. **PENTING:** Centang **"Add Python to PATH"**
4. Klik **Install Now**

Verifikasi:
```cmd
py --version
pip --version
```

### Step 2 – Install Go

1. Buka [go.dev/dl](https://go.dev/dl/)
2. Download `go1.xx.x.windows-amd64.msi`
3. Install (default: `C:\Program Files\Go`)
4. **Tutup CMD, buka lagi**

Verifikasi:
```cmd
go version
```

### Step 3 – Install Git

Download dari [git-scm.com](https://git-scm.com/download/win), install.

### Step 4 – Clone Repository

```cmd
cd %USERPROFILE%\Downloads
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 5 – **IMPORTANT:** Fix PyFPDF conflict

```cmd
pip uninstall -y pypdf fpdf fpdf2
pip install --upgrade --force-reinstall fpdf2
```

Test:
```cmd
py -c "from fpdf import FPDF; print('fpdf2 OK')"
```

Harus muncul `fpdf2 OK`. Kalau error, lihat [Troubleshooting](#troubleshooting).

### Step 6 – Install Requirements

```cmd
pip install -r requirements.txt
pip install sqlmap arjun user-scanner curl-cffi
```

### Step 7 – Install Go Tools

Jalankan satu-per-satu:
```cmd
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/ffuf/ffuf/v2@latest
go install github.com/hahwul/dalfox/v2@latest
go install -v github.com/owasp-amass/amass/v5/cmd/amass@main
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
```

### Step 8 – Add GOPATH to PATH

```cmd
for /f "delims=" %i in ('go env GOPATH') do set GOPATH=%i
setx PATH "%PATH%;%GOPATH%\bin"
```

Tutup CMD, buka lagi.

### Step 9 – Install System Tools

**Nmap** → [nmap.org/download](https://nmap.org/download.html) → centang "Add to PATH"  
**Wireshark** → [wireshark.org/download](https://www.wireshark.org/download.html) → centang "Install TShark" + "Add to PATH"  
**Metasploit** → [metasploit.com/download](https://www.metasploit.com/download) → install MSI  
**BurpSuite** → [portswigger.net/burp](https://portswigger.net/burp/communitydownload) → enable REST API port 1337

### Step 10 – Run Ghost Scanner

```cmd
cd %USERPROFILE%\Downloads\Ghost-Scanner
py ghostscanner.py -h
```

Kalau muncul banner skull + help → **BERHASIL** ✅

Scan target:
```cmd
py ghostscanner.py -u https://target.com --scan --pdf --tools --fast
```

**Catatan:** Di Windows gunakan `py` atau `python` (bukan `python3`). **NO WSL REQUIRED.**

---

## 5. MACOS INSTALLATION

### Step 1 – Install Homebrew (kalau belum ada)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2 – Install Prerequisites

```bash
brew install python3 git go nmap poppler masscan
```

### Step 3 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 4 – Fix fpdf + install deps

```bash
pip3 uninstall -y pypdf fpdf fpdf2
pip3 install --upgrade --force-reinstall fpdf2
pip3 install -r requirements.txt
pip3 install sqlmap arjun user-scanner curl-cffi
```

### Step 5 – Install Go Tools (sama seperti Kali)

### Step 6 – Add GOPATH to PATH

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc
source ~/.zshrc
```

### Step 7 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --tools --fast
```

---

## INTERACTIVE MENU

Jalankan tanpa argumen:

```bash
python ghostscanner.py
```

Menu yang muncul:

```
[1] SCAN (Unified)     - Full automated scan
[2] TOOLS (External)   - 19 external tools
[3] ATTACK (Real)      - Real DDoS/DoS (http/syn/slow/ssl/udp)
[4] HELP               - Show help
[0] EXIT
```

---

## USAGE EXAMPLES

### Full Scan (Recommended)

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --tools --fast
```

### Deep Scan (More Thorough)

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --deep --force-admin --tools
```

### Stealth Mode (Slow, No Proxy)

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --no-proxy --delay 2.0
```

### With Proxy Rotation

```bash
python3 ghostscanner.py -u https://target.com --scan --pdf --proxy-list proxies.txt --validate-proxy
```

### High Threads Scan

```bash
python3 ghostscanner.py -u https://target.com --scan --fast --threads 100
```

### Attack — Slowloris DoS

```bash
python3 ghostscanner.py -u https://your-server.com --slow --threads 200 --duration 30
```

### Attack — HTTP Flood

```bash
python3 ghostscanner.py -u https://your-server.com --dos --threads 500 --duration 60
```

### Attack — Multi-Method (HTTP + SYN + Slowloris + UDP + SSL)

```bash
python3 ghostscanner.py -u https://your-server.com --ddos --threads 500 --duration 60
```

### Attack — SYN Flood

```bash
python3 ghostscanner.py -u https://your-server.com --syn --threads 200 --duration 20
```

### Attack — SSL Renegotiation

```bash
python3 ghostscanner.py -u https://your-server.com --ssl-reneg --threads 150 --duration 30
```

### Attack — UDP Flood

```bash
python3 ghostscanner.py -u https://your-server.com --udp --threads 100 --duration 30
```

---

## DOMAIN CLASSIFICATION

Ghost Scanner v6.0 otomatis klasifikasi target ke salah satu dari **20+ kategori**:

| Kategori | Contoh TLD / Keyword |
|----------|---------------------|
| **Government / Pemerintah Pusat** | .go.id (non-pemda), .gov, .gob, .gc |
| **Government / Pemerintah Daerah** | pemda, pemkot, pemkab |
| **Education / Universitas** | .ac.id, .edu, university, college |
| **Education / Sekolah** | .sch.id, school |
| **Military** | .mil, .mil.id, tni |
| **Police** | polri, police |
| **Banking / Finance** | bank, bca, mandiri, bni, bri, btn, cimb, credit, finance, invest, trading, forex, crypto, bitcoin |
| **E-Commerce** | shop, store, tokopedia, shopee, lazada, bukalapak, blibli, market |
| **News / Media** | news, media, press, detik, kompas, tempo, tribun, blog |
| **Medical / Healthcare** | hospital, clinic, health, med, rs, klinik |
| **Religious** | islam, kristen, katolik, masjid, gereja, vihara, pura |
| **NGO** | ngo, yayasan, foundation |
| **Adult** | sex, porn, xxx, adult, escort |
| **Gambling** | casino, bet, poker, slot, gamble, togel |
| **Social** | chat, dating, social, friend, match |
| **Jobs** | job, career, hire, recruit, lowongan |
| **Travel** | travel, hotel, flight, ticket, tour |
| **Food** | food, restaurant, recipe, cook, delivery |
| **Gaming** | game, gaming, esport, steam, play |
| **Hosting / Cloud** | cloud, host, vps, server, domain, dns |
| **Technology** | api, dev, code, git, tech, software, app |
| **Business / Commercial** | default untuk domain komersial |
| **International** | .int |
| **Other** | sisa |

Output muncul di report sebagai `domain_category` + `domain_subcategory`.

---

## REGION DETECTION

Ghost Scanner v6.0 detect region via **5 sumber**:

1. **IP Geolocation** (via ip-api.com) – country, countryCode, regionName, city, isp, asn, timezone
2. **Domain TLD** – .go.id/.ac.id/.co.id → Indonesia, .gov → US, .uk → UK, .sg → SG, .jp → JP, dll
3. **NIK Prefix** – 2 digit pertama NIK decode province (11=Aceh, 31=DKI Jakarta, 32=Jawa Barat, ..., 91=Papua)
4. **Phone Prefix** – 4 digit prefix HP decode carrier (0811-0813=Telkomsel, 0814-0816=Indosat, 0817-0819=XL, 0831-0838=Axis, 0895-0899=Tri, 0881-0889=Smartfren)
5. **HTML Lang** – `<html lang="id">` → Indonesian

Output:
```json
{
  "country": "Indonesia",
  "country_code": "ID",
  "city": "Jakarta",
  "region_name": "DKI Jakarta",
  "isp": "PT Telkom Indonesia",
  "asn": "AS7713 PT Telekomunikasi Indonesia",
  "timezone": "Asia/Jakarta",
  "from_tld": "Indonesia",
  "from_ip": "Indonesia",
  "from_nik": ["Jawa Barat", "DKI Jakarta"],
  "from_phone": ["Telkomsel", "Indosat"],
  "from_language": "id"
}
```

---

## .ENV & CONFIG DOWNLOAD

Ghost Scanner v6.0 otomatis detect + download file sensitif. **Full content**, bukan cuma check existence.

### File yang Discan

**ENV files:**
- `/.env`, `/.env.local`, `/.env.production`, `/.env.development`
- `/.env.backup`, `/.env.old`, `/.env.example`, `/env`

**Config files:**
- `/wp-config.php`, `/config.php`, `/config.php.bak`, `/config.php~`
- `/configuration.php`, `/settings.py`, `/local_settings.py`
- `/config.json`, `/config.yaml`, `/config.yml`, `/config.xml`
- `/database.yml`, `/database.json`
- `/credentials.json`, `/secrets.json`
- `/.htaccess`, `/.htpasswd`, `/web.config`
- `/Dockerfile`, `/docker-compose.yml`
- `/.git/config`, `/.git/HEAD`
- `/.npmrc`, `/.pypirc`, `/.netrc`
- `/.ssh/id_rsa`, `/.ssh/authorized_keys`
- `/backup.sql`, `/backup.zip`, `/db.sql`, `/dump.sql`
- `/phpinfo.php`, `/info.php`
- Dan 40+ file lainnya

### Yang di-Extract dari .env

- DB_PASSWORD, DB_USERNAME, DB_HOST, DB_DATABASE
- APP_KEY, SECRET_KEY, JWT_SECRET, SESSION_SECRET
- API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- STRIPE_SECRET, SENDGRID_API_KEY, MAIL_PASSWORD
- REDIS_PASSWORD, MONGODB_URI, DATABASE_URL
- GOOGLE_CLIENT_SECRET, FACEBOOK_SECRET, TWITTER_SECRET

### Output

Files disimpan di:
```
downloads/
├── env_files/
│   └── env_<timestamp>_.env
└── config_files/
    └── config_<timestamp>_wp-config.php
```

Finding muncul sebagai `CRITICAL` di report dengan:
- URL
- File size
- Total keys (untuk .env)
- Extracted secrets
- curl command
- Full content snippet

---

## EXTERNAL TOOLS INTEGRATED

| # | Tool | Fungsi |
|---|------|--------|
| 1 | Nuclei | Template-based vuln scanning |
| 2 | Subfinder | Passive subdomain enumeration |
| 3 | httpx | Live host probing |
| 4 | Naabu | Fast port scanning |
| 5 | Katana | Web crawling |
| 6 | ffuf | Web fuzzing |
| 7 | sqlmap | Automated SQL injection |
| 8 | Dalfox | XSS scanning |
| 9 | Amass | Attack surface mapping |
| 10 | dnsx | DNS resolution |
| 11 | gau | Historical URL fetcher |
| 12 | waybackurls | Wayback Machine URLs |
| 13 | Arjun | Hidden HTTP parameter discovery |
| 14 | SecretFinder | API key detection in JS |
| 15 | Interactsh | OOB interaction |
| 16 | Nmap | Port scan + service detection |
| 17 | Metasploit | Exploit suggestions |
| 18 | Wireshark (tshark) | Packet capture |
| 19 | BurpSuite | REST API integration |

**Auto-skip** kalau tool gak ada — gak akan error.

---

## OUTPUT & REPORTS

Setelah scan, struktur folder:

```
results/
├── scan_v60_<timestamp>.json      # Full data (JSON)
└── report_v60_<timestamp>.pdf     # PDF report

sensitive_data/
├── nik_<ts>.txt
├── no_hp_<ts>.txt
├── email_<ts>.txt
├── ktp_links_<ts>.txt
├── kk_links_<ts>.txt
├── no_rekening_<ts>.txt
├── bank_<ts>.txt
├── pin_<ts>.txt
├── api_keys_<ts>.txt
├── jwt_tokens_<ts>.txt
├── source_code_<ts>.txt
├── employees_<ts>.pdf            # Employee correlation PDF
├── photos/                       # KTP/KK/photo dari target
│   └── photo_*.jpg
└── pdfs/                         # Per-category PDF
    ├── nik_<ts>.pdf
    ├── ktp_links_<ts>.pdf
    ├── kk_links_<ts>.pdf
    ├── no_rekening_<ts>.pdf
    ├── bank_<ts>.pdf
    ├── phones_<ts>.pdf
    ├── emails_<ts>.pdf
    ├── pin_<ts>.pdf
    ├── api_keys_<ts>.pdf
    ├── jwt_tokens_<ts>.pdf
    ├── source_code_<ts>.pdf
    └── ... (40+ kategori)

downloads/
├── env_files/
│   └── env_<ts>_.env             # Full .env content
└── config_files/
    └── config_<ts>_wp-config.php  # Full config content
```

---

## TROUBLESHOOTING

### 🔴 `ImportError: cannot import name 'FPDF' from 'fpdf' (unknown location)`

**Penyebab:** PyFPDF & fpdf2 bentrok (share module namespace `fpdf`).

**Fix:**
```bash
pip uninstall -y pypdf fpdf fpdf2
pip install --upgrade --force-reinstall --no-cache-dir fpdf2
python -c "from fpdf import FPDF; print('fpdf2 OK')"
```

Kalau masih error:
```bash
# Cek apakah ada file fpdf.py nyangkut di folder project
Get-ChildItem -Path . -Recurse -Filter "fpdf*" -ErrorAction SilentlyContinue
# Hapus kalau ada
Remove-Item -Recurse -Force .\fpdf, .\fpdf.py, .\__pycache__ -ErrorAction SilentlyContinue
```

Solusi paling aman — pakai venv:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install curl-cffi user-scanner
python ghostscanner.py -h
```

### 🔴 `NameError: name 'show_help' is not defined`

**Penyebab:** File `ghostscanner.py` corrupt / kepotong.

**Fix:** Download ulang dari GitHub, atau pastikan file length > 2000 baris.

### 🟡 `mediapipe requires protobuf<5,>=4.25.3, but you have protobuf 5.29.6`

**Gak masalah.** Mediapipe beda project. Abaikan. Kalau butuh:
```bash
pip install "protobuf<5,>=4.25.3"
```

### 🔴 `nuclei: command not found`

```bash
# Linux/Termux:
export PATH=$PATH:$(go env GOPATH)/bin

# Windows:
setx PATH "%PATH%;%GOPATH%\bin"
```

### 🟡 `user-scanner: command not found`

```bash
pip install user-scanner
```

### 🟡 `strix` not found

Strix gak dipakai di v6.0 (no AI). Auto-skip.

### 🔴 Scan lambat

Gunakan `--fast`:
```bash
python3 ghostscanner.py -u https://target.com --scan --fast
```

### 🔴 Proxy validation fails

```bash
python3 ghostscanner.py -u https://target.com --scan --no-proxy
```

### 🔴 `Permission denied` (Linux)

```bash
chmod +x ghostscanner.py
```

### 🔴 `externally-managed-environment` (Arch)

```bash
pip install --break-system-packages -r requirements.txt
```

---

## DISCLAIMER

Ghost Scanner dirancang untuk **ethical security research, penetration testing, dan authorized security assessment**.

- Anda harus punya **izin eksplisit** untuk menguji sistem yang bukan milik Anda
- Penggunaan tanpa izin = **ilegal**, dapat hukuman pidana berat
- **DDoS/DoS** ke server orang lain = **tindak pidana**. Gunakan **hanya pada server milik sendiri**
- Author (**GhostTeam**) **tidak bertanggung jawab** atas penyalahgunaan, kerusakan, atau konsekuensi hukum
- Dengan menggunakan tool ini, Anda menerima tanggung jawab penuh atas tindakan Anda

---

## VERSION HISTORY

### v6.0 [BETA] – 2026-09-14
- **AI completely removed** (no AI_KEYS, no models, no API calls)
- **Full logic**, all functions self-contained
- Domain classification 20+ kategori
- Region detection (IP geo + TLD + NIK + phone + lang)
- .env full download + secret extraction
- Config file full download (50+ files)
- 50+ sensitive data patterns
- Employee correlation (NIK/email/phone/rekening)
- NIK region decode
- Fast mode (`--fast`) & Deep mode (`--deep`)
- Full PoC every finding
- Fix `show_help` bug
- Fix PyFPDF vs fpdf2 conflict

### v5.6 [ALPHA] – 2026-09-13
- Domain category (partial)
- Region detection (basic)
- .env download
- 50+ sensitive patterns
- AI multi-model fallback

### v5.5 – 2026-09-11
- Deep harvest
- Admin PoC (form + API)
- Real port probe
- Employee correlation
- Masscan support
- Slowloris DoS

### v5.1 [BETA] – 2026-09-11
- 19 external tools
- user-scanner OSINT
- 1M+ payloads

### v5.0 (OMNI TOOLS X SAVAGE) – 2026-09-10
- Unified scan mode
- Real DDoS engine
- Interactive menu

### v4.x dan sebelumnya
- Lihat changelog di GitHub

---

## CONTACT

Maintained by **GhostTeam**  
GitHub: [https://github.com/cozyleon00b-dev](https://github.com/cozyleon00b-dev)

---

## ACKNOWLEDGEMENTS

- ProjectDiscovery (Nuclei, Subfinder, httpx, Naabu, Katana, dnsx, Interactsh)
- OWASP Amass
- ffuf, sqlmap, Dalfox, gau, waybackurls, Arjun, SecretFinder
- Nmap, Metasploit, Wireshark, BurpSuite
- [kaifcodec/user-scanner](https://github.com/kaifcodec/user-scanner)
- Cloudscraper, Rich, fpdf2, curl-cffi

**THANKS TO**
1. God
2. Parents
3. GhostTeam
4. Bestfriends
5. Friends

**JOIN CYBERSECURITY GROUP TELEGRAM**  
[https://t.me/roompubiccybersecurity](https://t.me/roompubiccybersecurity)

---

**ALL COPYRIGHT RESERVED**  
© 2026 GhostTeam – Ghost Scanner v6.0 [BETA]