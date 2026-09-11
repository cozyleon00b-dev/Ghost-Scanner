# GHOST SCANNER – OMNI TOOLS X SAVAGE

**All‑in‑One Security Assessment & Penetration Testing Framework**  
Version 5.0 – OMNI TOOLS X SAVAGE  
Release Date: 2026‑09‑11  
Developer: GhostTeam

---

## OVERVIEW

Ghost Scanner is a modular, high‑performance security assessment framework designed for ethical hacking, vulnerability assessment, and authorized stress testing. It combines internal engines with **19 industry‑standard external tools**, unified scanning, real DDoS/DoS engine, AI‑powered analysis, and comprehensive reporting in JSON, HTML, and PDF.

### Key Capabilities

- **Unified Scan Mode** – one command `--scan` runs SQLi, XSS, WP, Deface, DDoS check, JWT, HTTP Smuggling, GraphQL, OAuth, admin bypass, sensitive data extraction, and more in a single pass
- **19 External Tools Integration** – Nuclei, Subfinder, httpx, Naabu, Katana, ffuf, sqlmap, Dalfox, Amass, dnsx, gau, waybackurls, Arjun, SecretFinder, Interactsh, Nmap, Metasploit, Wireshark (tshark), BurpSuite
- **Real DDoS/DoS Engine** – socket‑based HTTP flood, SYN flood, SSL renegotiation, UDP flood with real‑time stats (no simulation)
- **Advanced Web Vulnerability Scanning** – SQLi (1M+ payloads), XSS (Dalfox context‑aware + 1M payloads), LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE
- **Deface Detection** – advanced pattern matching with 20+ indicators, title extraction, curl command, verified 3x
- **WordPress Activity Log RCE (CVE‑2026‑54806)** – detection and blind command execution (auto‑skip if not WordPress)
- **Admin Deep Extraction** – login bypass, crawl 22+ admin pages, extract tables, download exports (.sql, .csv, .zip, .json), detect database config leaks
- **E‑commerce Detection** – identifies domain/hosting/VPS provider, extracts products, prices, buyers, employees
- **Sensitive Data Extraction (Indonesia)** – NIK (with province/kabupaten/kecamatan parsing), NPWP, NIP, bank accounts, bank names, WhatsApp, PIN, KTP links, KK links, Surat Izin links, PDF links, API keys, JWT, cloud keys, source code
- **Separate PDF per Sensitive Category** – each data type gets its own PDF (NIK, KTP, KK, HP, Email, Bank, Rekening, PIN, API, Source Code, Admin Users/Buyers/Employees/Orders/Products)
- **AI Analysis (Claude Opus 5 via CodeCraft)** – 8‑section report: executive summary, critical findings, high findings, sensitive data analysis (UU PDP/GDPR), prioritized remediation, 30‑60‑90 day action plan, further testing suggestions, constructive critique, best practices
- **PoC Verification 3x** – each finding re‑verified 3 times (min. 2/3 match) to eliminate false positives
- **IP Safety / Anti‑Ban v2** – adaptive delay based on response time, proxy rotation (ProxyScrape API), user‑agent rotation, cloudscraper + fallback, exponential backoff
- **Domain Classification** – Government, Education, Police, Military, Medical, Business, Other
- **Interactive Menu** – menu lengkap dengan penjelasan tiap mode saat start tanpa argumen
- **Cross‑Platform** – Windows, Linux (Kali/Ubuntu/Arch/BlackArch), Termux (Android), macOS
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
8. [External Tools](#external-tools-integrated)
9. [Output & Reports](#output--reports)
10. [Troubleshooting](#troubleshooting)
11. [Disclaimer](#disclaimer)

---

## 1. KALI LINUX / DEBIAN / UBUNTU INSTALLATION

### Step 1 – Update System & Install Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git golang-go -y
```

### Step 2 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
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
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install -r ~/SecretFinder/requirements.txt
```

### Step 7 – Install System Tools (Nmap, Metasploit, Wireshark, BurpSuite)

```bash
# Nmap
sudo apt install nmap -y

# Wireshark + tshark
sudo apt install wireshark tshark -y

# Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall

# BurpSuite
# Download dari https://portswigger.net/burp/communitydownload
```

### Step 8 – Verify Installation

```bash
nuclei -version
subfinder -version
httpx -version
dalfox version
nmap --version
sqlmap --version
python3 ghostscanner.py --help
```

### Step 9 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
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
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 3 – Install Python Dependencies

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
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 – Install SecretFinder & System Tools

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install --break-system-packages -r ~/SecretFinder/requirements.txt

# Nmap, Wireshark
sudo pacman -S nmap wireshark-qt
```

### Step 7 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
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

### Step 4 – Install Python Dependencies

```bash
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages sqlmap arjun
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
export PATH=$PATH:$HOME/go/bin
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 7 – Install SecretFinder

```bash
git clone https://github.com/m4ll0k/SecretFinder.git ~/SecretFinder
pip install --break-system-packages -r ~/SecretFinder/requirements.txt
```

### Step 8 – Run Ghost Scanner

```bash
python3 ghostscanner.py -u https://target.com --scan --ai --pdf --tools
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

Verifikasi (buka CMD baru):
```cmd
python --version
pip --version
```

### Step 2 – Install Go

1. Buka [go.dev/dl](https://go.dev/dl/)
2. Download **`go1.xx.x.windows-amd64.msi`** (versi terbaru)
3. **Double-click** file `.msi`
4. Ikuti wizard: Next → Next → Install (default path: `C:\Program Files\Go`)
5. **Tutup CMD, buka lagi** (biar PATH kebaca)

Verifikasi:
```cmd
go version
```

### Step 3 – Install Git

1. Buka [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download dan install Git for Windows

Verifikasi:
```cmd
git --version
```

### Step 4 – Clone Repository

Buka **CMD**, jalankan:
```cmd
cd %USERPROFILE%\Downloads
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 5 – Install Python Dependencies

```cmd
pip install -r requirements.txt
pip install sqlmap arjun
```

### Step 6 – Install Go Tools

**Jalankan satu per satu** di CMD:
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

### Step 7 – Add GOPATH to PATH (CMD)

```cmd
for /f "delims=" %i in ('go env GOPATH') do set GOPATH=%i
setx PATH "%PATH%;%GOPATH%\bin"
```

Tutup CMD, buka lagi.

### Step 8 – Install System Tools

**Nmap**
1. Download dari https://nmap.org/download.html
2. Install `nmap-x.xx-setup.exe`
3. Centang **"Add Nmap to PATH"**

**Wireshark**
1. Download dari https://www.wireshark.org/download.html
2. Install `Wireshark-x.xx-x64.exe`
3. Centang **"Install TShark"** dan **"Add to PATH"**

**Metasploit**
1. Download dari https://www.metasploit.com/download
2. Install `metasploitframework-latest.msi`

**BurpSuite**
1. Download dari https://portswigger.net/burp/communitydownload
2. Install & buka BurpSuite
3. Enable REST API: Settings → Suite → REST API → **Enable** (default port 1337)

### Step 9 – Install SecretFinder

```cmd
cd %USERPROFILE%
git clone https://github.com/m4ll0k/SecretFinder.git
```

### Step 10 – Verify Installation

Buka **CMD baru**:
```cmd
where nuclei && where subfinder && where httpx && where naabu && where katana && where ffuf && where dalfox && where amass && where dnsx && where gau && where waybackurls && where interactsh-client
```

Kalau semua muncul path `C:\Users\<user>\go\bin\xxx.exe`, berarti berhasil.

### Step 11 – Run Ghost Scanner

```cmd
cd %USERPROFILE%\Downloads\Ghost-Scanner
python ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
```

**Catatan:** Di Windows, gunakan `python` (bukan `python3`). **NO WSL REQUIRED.**

---

## 5. MACOS INSTALLATION

### Step 1 – Install Homebrew (Jika Belum Ada)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2 – Install Prerequisites

```bash
brew install python3 git go nmap
```

### Step 3 – Clone Repository

```bash
git clone https://github.com/cozyleon00b-dev/Ghost-Scanner.git
cd Ghost-Scanner
```

### Step 4 – Install Python Dependencies

```bash
pip3 install -r requirements.txt
pip3 install sqlmap arjun
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
python3 ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
```

---

## INTERACTIVE MENU

Jalankan Ghost Scanner tanpa argumen untuk membuka **menu interaktif** dengan penjelasan lengkap:

```bash
python ghostscanner.py
```

Menu yang muncul:

```
[1] SCAN (Unified)
    Full automated scan dalam satu perintah:
      SQLi (1M+ payloads), XSS (Dalfox + 1M), LFI/RFI/SSTI/XXE/SSRF,
      WP Activity Log CVE, Deface, DDoS Check, JWT, HTTP Smuggling,
      GraphQL, OAuth, Admin bypass, Sensitive data, AI + PDF.

[2] TOOLS (External)
    Jalankan 19 external tools (Nuclei, Subfinder, httpx, Naabu, Katana,
    ffuf, sqlmap, Dalfox, Amass, dnsx, gau, waybackurls, Arjun,
    SecretFinder, Interactsh, Nmap, Metasploit, Wireshark, BurpSuite).

[3] ATTACK (Real DDoS/DoS)
    Real attack engine (socket-based):
      --dos HTTP Flood, --ddos Multi-method,
      --syn SYN Flood, --ssl-reneg SSL Reneg, --udp UDP Flood.

[4] HELP
[0] EXIT
```

Setiap mode akan meminta target URL dan konfigurasi tambahan (AI, PDF, tools, force admin).

---

## USAGE EXAMPLES

### Unified Scan (All Features, 19 Tools)

**Linux / Termux / macOS:**
```bash
python3 ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
```

**Windows (CMD):**
```cmd
python ghostscanner.py -u https://target.com --scan --ai --pdf --tools --force-admin
```

### Quick Scan (No External Tools, No AI)

```bash
python3 ghostscanner.py -u https://target.com --quick
```

### Scan with Proxy Rotation

```bash
python3 ghostscanner.py -u https://target.com --scan --proxy-list proxies.txt --validate-proxy --ai --pdf
```

### Stealth Mode (Slow Delay, No Proxy)

```bash
python3 ghostscanner.py -u https://target.com --scan --no-proxy --delay 2.0
```

### Force Admin Login + Deep Extraction

```bash
python3 ghostscanner.py -u https://target.com --scan --force-admin --ai --pdf
```

### Check WP Activity Log CVE Only

```bash
python3 ghostscanner.py -u https://target.com --wp-check
```

### Real DDoS Attack (HTTP Flood)

```bash
python3 ghostscanner.py -u https://your-server.com --dos --threads 500 --duration 60
```

### Full DDoS (All Methods)

```bash
python3 ghostscanner.py -u https://your-server.com --ddos --threads 300 --duration 30
```

### SYN Flood

```bash
python3 ghostscanner.py -u https://your-server.com --syn --threads 200 --duration 20
```

### SSL Renegotiation

```bash
python3 ghostscanner.py -u https://your-server.com --ssl-reneg --threads 150 --duration 30
```

### UDP Flood

```bash
python3 ghostscanner.py -u https://your-server.com --udp --threads 100 --duration 30
```

---

## EXTERNAL TOOLS INTEGRATED

| # | Tool | Function |
|---|------|----------|
| 1 | Nuclei | Template‑based vulnerability scanning |
| 2 | Subfinder | Passive subdomain enumeration |
| 3 | httpx | Live host probing |
| 4 | Naabu | Fast port scanning |
| 5 | Katana | Web crawling & endpoint discovery |
| 6 | ffuf | Web fuzzing |
| 7 | sqlmap | Automated SQL injection |
| 8 | Dalfox | XSS scanning |
| 9 | Amass | Attack‑surface mapping |
| 10 | dnsx | DNS resolution & probing |
| 11 | gau | Historical URL fetcher |
| 12 | waybackurls | Wayback Machine URLs |
| 13 | Arjun | Hidden HTTP parameter discovery |
| 14 | SecretFinder | API key detection in JS |
| 15 | Interactsh | Out‑of‑band interaction |
| 16 | Nmap | Port scan + service detection |
| 17 | Metasploit | Exploit module suggestions |
| 18 | Wireshark (tshark) | Packet capture & verification |
| 19 | BurpSuite | REST API integration for scanning |

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

**Windows CMD:** (sama, tapi jalankan satu per satu)

---

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
python3 ghostscanner.py -u https://target.com --scan --proxy-list proxies.txt --validate-proxy
```

---

## OUTPUT & REPORTS

Setelah scan, struktur folder:

```
results/
├── scan_<timestamp>.json            # Semua data scan
└── report_<timestamp>.pdf           # Report utama (jika --pdf)

sensitive_data/
├── nik_<ts>.txt
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
├── admin_deep_<ts>.json
├── exports/
└── pdfs/
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

---

## TROUBLESHOOTING

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: No module named 'cloudscraper'` | `pip install cloudscraper` |
| `go: command not found` | Restart terminal, atau tambah Go ke PATH |
| `nuclei: command not found` | Linux/Termux: `export PATH=$PATH:$(go env GOPATH)/bin` / Windows: tambah `%GOPATH%\bin` ke PATH |
| `pip: command not found` | Pakai `python -m pip install ...` |
| Proxy validation fails | Coba tanpa `--validate-proxy` |
| Scan terlalu lambat | Gunakan `--quick` |
| AI timeout | Otomatis retry 3x dengan timeout 180s |
| `Permission denied` (Linux) | `chmod +x ghostscanner.py` |
| Termux: `pkg` not found | Pastikan pakai Termux |
| `externally-managed-environment` error | Tambah `--break-system-packages` atau pakai venv |
| Windows: `python3` not found | Gunakan `python` |
| Windows: Device Guard blokir tool | Unblock file atau install WSL |
| Windows: `UnicodeDecodeError` | Sudah di‑fix di v4.6+ (`errors='ignore'`) |
| `The system cannot find the path specified` | Pakai tanda kutip: `cd "C:\path\to\folder"` |

### Performance Tips

- `--quick` mengurangi payload jadi 10 per kategori
- `--tools` hanya jalankan jika external tools terinstall
- `--no-proxy` untuk testing lokal/internal
- `--delay 0.3` untuk scan lebih cepat
- `--delay 2.0` untuk stealth

---

## DISCLAIMER

Ghost Scanner dirancang untuk **ethical security research, penetration testing, dan authorized security assessment**.

- Anda harus memiliki **izin eksplisit** untuk menguji sistem yang bukan milik Anda
- Penggunaan tanpa izin adalah **ilegal** dan dapat mengakibatkan hukuman pidana berat
- **DDoS/DoS** ke server orang lain adalah **tindak pidana**. Gunakan **hanya pada server milik Anda sendiri**
- Author (**ARGA NOT DEV**) **tidak bertanggung jawab** atas penyalahgunaan, kerusakan, atau konsekuensi hukum
- Dengan menggunakan tool ini, Anda menerima tanggung jawab penuh atas tindakan Anda

---

## VERSION HISTORY

- **5.0 (OMNI TOOLS X SAVAGE)** – 2026‑09‑11
  - Unified scan mode (`--scan` gas semua sekaligus)
  - Real DDoS/DoS engine (socket‑based, real‑time stats)
  - Interactive menu dengan penjelasan lengkap
  - Rebranding skull banner (ARGA NOT DEV)
  - Fix interactive prompt (loop kalau kosong)
  - No error, no bug

- **4.7 (OMNI TOOLS+ X FINAL)** – 2026‑09‑11
  - DDoS vulnerability check
  - Advanced deface detection
  - JWT attack, HTTP smuggling, Subdomain takeover
  - GraphQL introspection, OAuth bypass

- **4.6 (OMNI TOOLS+ X)** – 2026‑09‑11
  - 4 new tools: Nmap, Metasploit, Wireshark, BurpSuite
  - Fix UnicodeDecodeError
  - Anti‑ban double‑layer delay
  - PoC verification 3x

- **4.5 (OMNI TOOLS+)** – 2026‑09‑10
  - 15 external tools integration
  - Separate PDF per sensitive data category
  - PIN extraction, KK links
  - Auto‑skip WP check

- **4.4 (GHOST MULTI‑TOOLS+)** – 2026‑09‑10
  - Sneijderlino methods (robots.txt, sitemap, dir enum, dll)
  - PoC verification 5x

- **4.3 (ADMIN DATABASE EXTRACTOR)** – 2026‑09‑10
  - Deep admin data extraction
  - E‑commerce detection
  - AI real solutions

- **4.2 (SENSITIVE HUNTER)** – 2026‑09‑10
  - Domain classification
  - Indonesian sensitive data extraction
  - ProxyScrape API

- **4.1 (OMNI XSS + WP LOG EXPLOIT)** – 2026‑09‑09
  - Dalfox XSS engine
  - CVE‑2026‑54806 detection

- **3.5 (ULTRA SAVAGE)** – 2026‑09‑08
  - 1M+ SQLi & XSS payloads
  - AI analysis + PDF

- **2.0 (FAST DEMON)** – 2026‑09‑03
  - Speed optimization
  - Custom help menu
  - Proxy validation

- **1.0 (DEMON)** – 2026‑08‑31
  - Initial release

---

## CONTACT

Maintained by **ARGA NOT DEV**  
GitHub: [https://github.com/cozyleon00b-dev](https://github.com/cozyleon00b-dev)

---

## ACKNOWLEDGEMENTS

Special thanks to open‑source community dan project berikut:

- ProjectDiscovery (Nuclei, Subfinder, httpx, Naabu, Katana, dnsx, Interactsh)
- OWASP Amass
- ffuf, sqlmap, Dalfox, gau, waybackurls, Arjun, SecretFinder
- Nmap, Metasploit, Wireshark, BurpSuite
- Cloudscraper, Rich, fpdf2

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
© 2026 GhostTeam – Ghost Scanner