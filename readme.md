# GHOST SCANNER – OMNI TOOLS+

**All‑in‑One Security Assessment & Penetration Testing Framework**  
Version 4.5 – OMNI TOOLS+  
Release Date: 2026‑09‑10

## OVERVIEW

Ghost Scanner is a modular, high‑performance security assessment framework designed for ethical hacking, vulnerability assessment, and stress testing. It combines internal engines with 15 industry‑standard external tools, generating comprehensive reports (JSON, HTML, PDF) with AI‑powered analysis and separate PDF outputs for each sensitive data category.

### Key Capabilities

- **Advanced Web Vulnerability Scanning** – SQLi, XSS (Dalfox context‑aware), LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE, Business Logic Errors, Mass Assignment, Rate Limit
- **15 External Tools Integration** – Nuclei, Subfinder, httpx, Naabu, Katana, ffuf, sqlmap, Dalfox, Amass, dnsx, gau, waybackurls, Arjun, SecretFinder, Interactsh
- **Deface Detection** – full PoC with 22+ indicators, title extraction, curl command, screenshot simulation
- **WordPress Activity Log RCE (CVE‑2026‑54806)** – detection & blind command execution (auto‑skip if not WordPress)
- **Admin Deep Extraction** – after successful admin login bypass, crawls 22+ admin pages, extracts tables, downloads exports (.sql, .csv, .zip, .json), detects database config leaks
- **E‑commerce Detection** – identifies domain/hosting/VPS provider, extracts products, prices, buyers, employees
- **Sensitive Data Extraction (Indonesia)** – NIK (with province/kabupaten/kecamatan parsing), NPWP, NIP, bank accounts, bank names, WhatsApp, PIN, KTP links, KK links, Surat Izin links, PDF links, API keys, JWT, cloud keys, source code
- **Separate PDF per Sensitive Category** – each data type (NIK, KTP, KK, HP, Email, Bank, Rekening, PIN, API, Source Code, Admin Users/Buyers/Employees/Orders/Products) gets its own PDF
- **AI Analysis (Claude Opus 5 via CodeCraft)** – 8‑section report: executive summary, critical findings, high findings, sensitive data analysis (UU PDP/GDPR), prioritized remediation, further testing suggestions, constructive critique, best practices
- **PoC Verification 5x** – each finding is re‑verified 5 times (min. 4/5 must match) to eliminate false positives
- **IP Safety / Anti‑Ban** – adaptive delay with jitter, proxy rotation (ProxyScrape API), user‑agent rotation, cloudscraper + fallback, exponential backoff
- **Domain Classification** – Government, Education, Police, Military, Medical, Business, Other
- **DOS/DDOS Engine** – HTTP flood, SYN flood, SSL renegotiation, UDP flood (multi‑threaded)
- **Cross‑Platform** – Windows, Linux (Kali/Ubuntu/Arch/BlackArch), Termux (Android), macOS

Ghost Scanner is intended for **authorized testing only**.

---

## TABLE OF CONTENTS

1. [Kali Linux / Debian / Ubuntu Installation](#1-kali-linux--debian--ubuntu-installation)
2. [Arch Linux / BlackArch Installation](#2-arch-linux--blackarch-installation)
3. [Termux (Android) Installation](#3-termux-android-installation)
4. [Windows Installation](#4-windows-installation)
5. [macOS Installation](#5-macos-installation)
6. [Usage Examples](#usage-examples)
7. [External Tools](#external-tools-integrated)
8. [Output & Reports](#output--reports)
9. [Troubleshooting](#troubleshooting)
10. [Disclaimer](#disclaimer)

---

## 1. KALI LINUX / DEBIAN / UBUNTU INSTALLATION

### Step 1 – Update System & Install Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git golang-go -y
```

### Step 2 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
cd ghost-scanner
```

### Step 3 – Install Python Dependencies

```bash
pip install -r requirements.txt
pip install sqlmap arjun
```

### Step 4 – Install Go Tools

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

### Step 5 – Add GOPATH to PATH

```bash
# Sesi ini saja
export PATH=$PATH:$(go env GOPATH)/bin

# Permanen (tambahkan ke ~/.bashrc atau ~/.zshrc)
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install -r ~/SecretFinder/requirements.txt
```

### Step 7 – Verify Installation

```bash
nuclei -version
subfinder -version
httpx -version
dalfox version
sqlmap --version
python3 ghostscanner.py --help
```

### Step 8 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

---

## 2. ARCH LINUX / BLACKARCH INSTALLATION

### Step 1 – Update System & Install Prerequisites

```bash
sudo pacman -Syu
sudo pacman -S python python-pip git go base-devel
```

### Step 2 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
cd ghost-scanner
```

### Step 3 – Install Python Dependencies

```bash
pip install -r requirements.txt
pip install sqlmap arjun
```

**Jika ada error "externally-managed-environment"** (Arch Linux terbaru):
```bash
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun
```

Atau pakai virtualenv:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install sqlmap arjun
```

### Step 4 – Install Go Tools

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

### Step 5 – Add GOPATH to PATH

```bash
export PATH=$PATH:$(go env GOPATH)/bin

# Permanen (tambahkan ke ~/.bashrc atau ~/.zshrc)
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install -r ~/SecretFinder/requirements.txt
```

### Step 7 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

---

## 3. TERMUX (ANDROID) INSTALLATION

### Step 1 – Update & Install Prerequisites

```bash
pkg update && pkg upgrade -y
pkg install python python-pip git golang -y
pip install --upgrade pip
```

### Step 2 – Setup Storage (Opsional)

```bash
termux-setup-storage
```

### Step 3 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
cd ghost-scanner
```

### Step 4 – Install Python Dependencies

```bash
pip install -r requirements.txt
pip install sqlmap arjun
```

**Jika ada error "externally-managed-environment"**:
```bash
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun
```

### Step 5 – Install Go Tools (Termux)

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

**Catatan Termux:** Beberapa tool mungkin gagal compile karena keterbatasan environment. Jika demikian, gunakan flag:
```bash
GODEBUG=madvdontneed=1 go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### Step 6 – Add GOPATH to PATH

```bash
export PATH=$PATH:$HOME/go/bin

# Permanen (tambahkan ke ~/.bashrc)
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 7 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install -r ~/SecretFinder/requirements.txt
```

### Step 8 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com -v --ai --pdf --tools
```

**Catatan:** Di Termux, mungkin perlu mengurangi thread untuk menghindari memory error:
```bash
python3 ghostscanner.py -u https://target.com --quick --threads 50
```

---

## 4. WINDOWS INSTALLATION

### Step 1 – Install Python

1. Buka [python.org/downloads](https://www.python.org/downloads/)
2. Download installer Python 3.11+ (Windows installer 64-bit)
3. **PENTING:** Centang **"Add Python to PATH"** saat instalasi
4. Klik **Install Now**

Verifikasi (buka PowerShell baru):
```powershell
python --version
pip --version
```

### Step 2 – Install Go

1. Buka [go.dev/dl](https://go.dev/dl/)
2. Download **`go1.xx.x.windows-amd64.msi`** (versi terbaru)
3. **Double-click** file `.msi`
4. Ikuti wizard: Next → Next → Install (default path: `C:\Program Files\Go`)
5. **Tutup PowerShell, buka lagi** (biar PATH kebaca)

Verifikasi:
```powershell
go version
```

### Step 3 – Install Git

1. Buka [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download dan install Git for Windows
3. Default settings OK

Verifikasi:
```powershell
git --version
```

### Step 4 – Clone Repository

Buka **PowerShell**, jalankan:
```powershell
cd "C:\Users\asus\Downloads"
git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
cd ghost-scanner
```

### Step 5 – Install Python Dependencies

```powershell
pip install -r requirements.txt
pip install sqlmap arjun
```

**Jika ada error "externally-managed-environment"**:
```powershell
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun
```

### Step 6 – Install Go Tools

**Jalankan satu per satu** di PowerShell:
```powershell
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

### Step 7 – Add GOPATH\bin to PATH (PowerShell)

```powershell
# Cek dulu di mana Go install binary
go env GOPATH
# Biasanya: C:\Users\asus\go

# Tambah ke PATH (sesi ini saja)
$env:Path += ";" + (go env GOPATH) + "\bin"

# Permanen (tutup dan buka ulang PowerShell setelah ini)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + (go env GOPATH) + "\bin", [EnvironmentVariableTarget]::User)
```

### Step 8 – Install SecretFinder

```powershell
git clone https://github.com/m4ll0k/SecretFinder.git $env:USERPROFILE\SecretFinder
```

### Step 9 – Verify Installation

Buka **PowerShell baru**, jalankan:
```powershell
nuclei -version
subfinder -version
httpx -version
dalfox version
sqlmap --version
```

### Step 10 – Run Ghost Scanner

```powershell
cd "C:\Users\asus\Downloads\ghost-scanner"
python ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

**Catatan:** Di Windows, gunakan `python` (bukan `python3`).

---

## 5. MACOS INSTALLATION

### Step 1 – Install Homebrew (Jika Belum Ada)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2 – Install Prerequisites

```bash
brew install python3 git go
```

### Step 3 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
cd ghost-scanner
```

### Step 4 – Install Python Dependencies

```bash
pip3 install -r requirements.txt
pip3 install sqlmap arjun
```

**Jika ada error "externally-managed-environment"**:
```bash
pip3 install --break-system-packages -r requirements.txt
pip3 install --break-system-packages sqlmap arjun
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

# Permanen (tambahkan ke ~/.zshrc)
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc
source ~/.zshrc
```

### Step 7 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip3 install -r ~/SecretFinder/requirements.txt
```

### Step 8 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

---

## USAGE EXAMPLES

### Full Scan (All Features)

**Linux / Termux / macOS:**
```bash
python3 ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

**Windows:**
```powershell
python ghostscanner.py -u https://target.com -v --ai --pdf --tools --force-admin
```

### Quick Scan (No External Tools, No AI)

```bash
python3 ghostscanner.py -u https://target.com --quick
```

### Scan with Proxy Rotation

```bash
python3 ghostscanner.py -u https://target.com -v --proxy-list proxies.txt --validate-proxy --ai --pdf
```

### Stealth Mode (Slow Delay, No Proxy)

```bash
python3 ghostscanner.py -u https://target.com --no-proxy --delay 2.0
```

### Force Admin Login + Deep Extraction

```bash
python3 ghostscanner.py -u https://target.com --force-admin --ai --pdf
```

### Check WP Activity Log CVE Only

```bash
python3 ghostscanner.py -u https://target.com --wp-check
```

### Exploit WP Activity Log (Blind RCE)

```bash
python3 ghostscanner.py -u https://target.com --wp-command "id"
```

### HTTP Flood (DOS)

```bash
python3 ghostscanner.py -u https://target.com --dos --threads 500 --duration 60
```

### Full DDOS (All Methods)

```bash
python3 ghostscanner.py -u https://target.com --ddos --threads 300 --duration 30
```

### SYN Flood Only

```bash
python3 ghostscanner.py -u https://target.com --syn --threads 200 --duration 20
```

### SSL Renegotiation Only

```bash
python3 ghostscanner.py -u https://target.com --ssl-reneg --threads 150 --duration 30
```

### UDP Flood Only

```bash
python3 ghostscanner.py -u https://target.com --udp --threads 100 --duration 30
```

## EXTERNAL TOOLS INTEGRATED

| # | Tool | Function |
|---|------|----------|
| 1 | **Nuclei** | Template‑based vulnerability scanning (CVE, misconfigurations) |
| 2 | **Subfinder** | Passive subdomain enumeration |
| 3 | **httpx** | Live host probing (status, title, tech detection) |
| 4 | **Naabu** | Fast port scanning |
| 5 | **Katana** | Web crawling & hidden endpoint discovery |
| 6 | **ffuf** | Web fuzzing (directory/file/parameter discovery) |
| 7 | **sqlmap** | Automated SQL injection testing |
| 8 | **Dalfox** | XSS scanning & parameter analysis |
| 9 | **Amass** | Attack‑surface mapping & asset discovery |
| 10 | **dnsx** | DNS resolution, wildcard detection, probing |
| 11 | **gau** | Historical URL fetcher |
| 12 | **waybackurls** | Wayback Machine URL fetcher |
| 13 | **Arjun** | Hidden HTTP parameter discovery |
| 14 | **SecretFinder** | API key / secret detection in JavaScript |
| 15 | **Interactsh** | Out‑of‑band interaction detection |

### Perintah Update Semua Go Tools

**Linux / Termux / macOS:**
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

**Windows PowerShell:** (sama, tapi jalankan satu per satu)

## PROXY CONFIGURATION

### File Format `proxies.txt`

```
http://username:password@192.168.1.100:8080
socks5://proxy.example.com:1080
http://203.0.113.50:3128
```

- Baris dengan `#` di depan diabaikan
- Jika tidak ada protocol, dianggap `http://`
- Gunakan `--validate-proxy` untuk filter proxy mati
- Jika tidak ada file, otomatis fetch dari **ProxyScrape API**

### Contoh Penggunaan

```bash
python3 ghostscanner.py -u https://target.com --proxy-list proxies.txt --validate-proxy
```

## OUTPUT & REPORTS

Setelah scan, struktur folder:

```
results/
├── scan_<timestamp>.json            # Semua data scan
└── report_<timestamp>.pdf           # Report utama (jika --pdf)

sensitive_data/
├── nik_<ts>.txt                     # Raw sensitive data
├── npwp_<ts>.txt
├── nip_<ts>.txt
├── no_rekening_<ts>.txt
├── bank_<ts>.txt
├── emails_<ts>.txt
├── phones_<ts>.txt
├── whatsapp_<ts>.txt
├── pin_<ts>.txt
├── api_keys_<ts>.txt
├── jwt_tokens_<ts>.txt
├── source_code_<ts>.txt
├── admin_deep_<ts>.json             # Admin panel deep extraction
├── exports/                         # File download dari admin
│   ├── users.sql
│   ├── backup.zip
│   └── ...
└── pdfs/                            # PDF terpisah per kategori sensitif
    ├── nik_<ts>.pdf
    ├── ktp_links_<ts>.pdf
    ├── kk_links_<ts>.pdf
    ├── no_rekening_<ts>.pdf
    ├── bank_<ts>.pdf
    ├── phones_<ts>.pdf
    ├── whatsapp_<ts>.pdf
    ├── emails_<ts>.pdf
    ├── pin_<ts>.pdf
    ├── api_keys_<ts>.pdf
    ├── jwt_tokens_<ts>.pdf
    ├── source_code_<ts>.pdf
    ├── admin_users_<ts>.pdf
    ├── admin_buyers_<ts>.pdf
    ├── admin_employees_<ts>.pdf
    ├── admin_orders_<ts>.pdf
    └── admin_products_<ts>.pdf
```

## TROUBLESHOOTING

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: No module named 'cloudscraper'` | `pip install cloudscraper` |
| `go: command not found` | Restart terminal setelah install Go, atau tambahkan `C:\Program Files\Go\bin` (Windows) / `/usr/local/go/bin` (Linux) ke PATH |
| `nuclei: command not found` | Linux/Termux: `export PATH=$PATH:$(go env GOPATH)/bin` / Windows: `$env:Path += ";" + (go env GOPATH) + "\bin"` |
| `pip: command not found` | Pakai `python3 -m pip install ...` (Linux/Termux/macOS) atau `python -m pip install ...` (Windows) |
| Proxy validation fails | Coba tanpa `--validate-proxy` |
| Scan terlalu lambat | Gunakan `--quick` |
| AI timeout | Otomatis retry 3x dengan timeout 180s |
| `Permission denied` (Linux) | `chmod +x ghostscanner.py` |
| Termux: `pkg` not found | Pastikan pakai Termux (bukan shell biasa) |
| `externally-managed-environment` error | Tambah `--break-system-packages` atau pakai venv |
| Windows: `python3` not found | Gunakan `python` (bukan `python3`) |
| Windows: `cd` error | Gunakan tanda kutip: `cd "C:\Users\asus\Downloads\ghost-scanner"` |
| SecretFinder tidak jalan | Cek path: `ls ~/SecretFinder/SecretFinder.py` (Linux) / `Test-Path $env:USERPROFILE\SecretFinder\SecretFinder.py` (Windows) |

### Performance Tips

- `--quick` mengurangi payload jadi 10 per kategori
- `--tools` hanya jalankan jika external tools terinstall
- `--no-proxy` untuk testing lokal/internal
- `--delay 0.3` untuk scan lebih cepat (lebih mudah terdeteksi)
- `--delay 2.0` untuk stealth (lebih lambat tapi aman)

## DISCLAIMER

Ghost Scanner dirancang untuk **ethical security research, penetration testing, dan authorized security assessment**.

- **Anda harus memiliki izin eksplisit** untuk menguji sistem yang bukan milik Anda
- Penggunaan tanpa izin adalah ilegal dan dapat mengakibatkan hukuman pidana berat
- Author (**ARGA NOT DEV**) **tidak bertanggung jawab** atas penyalahgunaan, kerusakan, atau konsekuensi hukum
- Dengan menggunakan tool ini, Anda menerima tanggung jawab penuh atas tindakan Anda


## VERSION HISTORY

- **4.5 (OMNI TOOLS+)** – 2026‑09‑10
  - Integrasi 15 external tools (Nuclei, Subfinder, httpx, Naabu, Katana, ffuf, sqlmap, Dalfox, Amass, dnsx, gau, waybackurls, Arjun, SecretFinder, Interactsh)
  - PDF terpisah per kategori sensitif (NIK, KTP, KK, HP, Email, Bank, Rekening, PIN, API, Source Code, Admin Users/Buyers/Employees/Orders)
  - PIN extraction
  - KK links extraction
  - Auto-skip WP check jika bukan WordPress

- **4.4 (GHOST MULTI‑TOOLS+)** – 2026‑09‑10
  - Sneijderlino methods (robots.txt, sitemap, dir enum, sensitive files, security headers, WAF detection, CORS, open redirect, SSL info, cookie flags, rate limit, CSRF)
  - Banner Ghost Multi-Tools
  - PoC verification 5x

- **4.3 (ADMIN DATABASE EXTRACTOR)** – 2026‑09‑10
  - Deep admin data extraction (crawl 22+ halaman, download export, DB config leaks)
  - E-commerce detection
  - AI real solutions prompt (8 section)

- **4.2 (SENSITIVE HUNTER)** – 2026‑09‑10
  - Domain classification
  - Indonesian sensitive data extraction
  - ProxyScrape API integration

- **4.1 (OMNI XSS + WP LOG EXPLOIT)** – 2026‑09‑09
  - Dalfox XSS engine (context-aware, DOM, CSP bypass, mXSS, Blind XSS)
  - CVE‑2026‑54806 detection & exploitation
  - Deface full PoC

- **3.5 (ULTRA SAVAGE)** – 2026‑09‑08
  - 1M+ SQLi & XSS payloads
  - AI analysis + PDF
  - SQL data extraction
  - PoC generation

- **2.0 (FAST DEMON)** – 2026‑09‑03
  - Speed optimization
  - Custom help menu
  - Proxy validation

- **1.0 (DEMON)** – 2026‑08‑31
  - Initial release


## CONTACT

Maintained by **ARGA NOT DEV**  
GitHub: [https://github.com/cozyleon00b-dev](https://github.com/cozyleon00b-dev)


## ACKNOWLEDGEMENTS

Special thanks to open‑source community dan project berikut:

- ProjectDiscovery (Nuclei, Subfinder, httpx, Naabu, Katana, dnsx, Interactsh)
- OWASP Amass
- ffuf, sqlmap, Dalfox, gau, waybackurls, Arjun, SecretFinder
- Cloudscraper, Rich, fpdf2

**THANKS TO**
1. God
2. Parents
3. GhostTeam
4. Bestfriends
5. Friends

**JOIN CYBERSECURITY GROUP TELEGRAM**  
[https://t.me/roompubiccybersecurity](https://t.me/roompubiccybersecurity)


**ALL COPYRIGHT RESERVED**  
© 2026 GhostTeam – Ghost Scanner