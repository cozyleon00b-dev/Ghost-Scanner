# GHOST SCANNER – SENSITIVE HUNTER

**All‑in‑One Security Assessment & Penetration Testing Framework**  
Version 4.2 – SENSITIVE HUNTER  
Release Date: 2026‑09‑10

## OVERVIEW

Ghost Scanner is a modular, high‑performance security tool designed for ethical hacking, vulnerability assessment, and stress testing. It combines:

- **Advanced Web Vulnerability Scanning** – SQLi, XSS (with Dalfox context‑aware engine), LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE, Business Logic Errors, Mass Assignment, Rate Limit
- **Deface Detection** – full PoC with indicator matching, title extraction, and curl command generation
- **WordPress Activity Log RCE (CVE‑2026‑54806)** – detection and blind command execution
- **Massive Payload Generation** – 1,000,000+ dynamic payloads for SQLi and XSS (sourced from W3Schools & OWASP) with intelligent sampling
- **SQL Data Extraction** – automatically extract database name, tables, columns, and sample data when SQL injection is found
- **Proof‑of‑Concept (PoC) Generation** – every finding includes a cURL command and direct URL for replication
- **Sensitive Data Extraction (Indonesia)** – NIK, NPWP, NIP, bank account numbers, bank names, WhatsApp numbers, KTP links, surat izin links, PDF links, and area codes (province, kabupaten, kecamatan)
- **Domain Classification** – automatically categorises target domain: Government, Education, Police, Military, Medical, Business/Commercial, or Other
- **AI‑Powered Analysis** – optional integration with CodeCraft Claude Opus 5 for intelligent vulnerability analysis, PoC evaluation, recommendations, and constructive feedback
- **PDF Report Generation** – professional, printable reports with all findings, PoCs, sensitive data, and AI analysis
- **Port Scanning** – fast TCP port discovery on common service ports
- **Proxy Rotation** – use SOCKS/HTTP proxies from file or built‑in list, with optional validation and ProxyScrape API integration
- **Cloudflare & Bot Bypass** – cloudscraper + user‑agent rotation + multi‑attempt fallback
- **Double Validation** – reduce false positives by re‑testing findings with alternative payloads
- **DOS/DDOS Engine** – HTTP flood, SYN flood, SSL renegotiation, UDP flood (multi‑threaded)
- **HTML, JSON & PDF Reporting** – structured output for professional audit trails

Ghost Scanner is built for speed, accuracy, and reliability. It is intended for **authorised testing only**.

## INSTALLATION

### Prerequisites
- Python 3.8 or higher
- pip (package installer)
- Git (optional, for cloning)

### Platform‑Specific Setup

**Termux (Android)**
```bash
pkg update && pkg upgrade
pkg install python python-pip git
pip install --upgrade pip
```

**Kali Linux / Debian**
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

**Arch Linux / BlackArch**
```bash
sudo pacman -Syu
sudo pacman -S python python-pip git
```

**Windows (CMD / PowerShell)**
- Download and install Python from [python.org](https://www.python.org/).
- Ensure **"Add Python to PATH"** is checked during installation.
- Use `python` command in terminal (not `python3`).

### Install Ghost Scanner

1. **Clone or download** the repository:
   ```bash
   git clone https://github.com/cozyleon00b-dev/ghost-scanner.git
   cd ghost-scanner
   ```
   *(If you only have the single `ghostscanner.py` file, place it in a dedicated folder.)*

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The updated `requirements.txt` includes:
   ```txt
   cloudscraper>=1.2.71
   fake-useragent>=1.5.1
   requests>=2.31.0
   rich>=13.7.1
   cryptography>=42.0.0
   fpdf>=1.7.2
   ```

3. **(Optional) Install pyppeteer for headless XSS verification** (`--headless` flag):
   ```bash
   pip install pyppeteer
   ```

4. **(Optional) Prepare a proxy list** – one proxy per line in a text file, e.g. `proxies.txt`:
   ```
   http://user:pass@proxy1:8080
   socks5://proxy2:1080
   http://proxy3:3128
   ```

5. **Make the script executable** (Linux/macOS/Termux):
   ```bash
   chmod +x ghostscanner.py
   ```

## USAGE

Ghost Scanner runs in two primary modes: **Scan** and **Attack**.

### Command Syntax
```bash
python ghostscanner.py -u <TARGET_URL> [OPTIONS]
```
*On Windows, use `python`; on Linux/macOS/Termux, use `python3`.*

### Global Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL (must include protocol, e.g. `https://example.com`) |
| `-o, --output` | Output JSON file name (default: `results.json`) |
| `-v, --verbose` | Enable verbose logging to console |
| `--proxy-list FILE` | Load proxies from a file (one per line) |
| `--validate-proxy` | Test each proxy before use (slower but more reliable) |
| `--no-proxy` | Disable proxy usage (use your own IP) |
| `--quick` | Quick scan (fewer payloads, faster) |
| `--pdf` | Generate PDF report (default: report.pdf) |
| `--ai` | Enable AI analysis using CodeCraft Claude Opus 5 |
| `--headless` | Enable headless verification for XSS (requires pyppeteer) |

### Scan Mode (Default)
When no attack flag is given, the script performs a full vulnerability scan.

**Example:**
```bash
python ghostscanner.py -u https://target.com -v --proxy-list proxies.txt --validate-proxy --pdf --ai
```

**What it does (all checks are performed automatically):**
- Accesses the target with cloudscraper + proxy rotation
- Extracts parameters, forms, and API endpoints
- Performs domain classification (Government, Education, Police, Military, Medical, Business, Other)
- Extracts sensitive data: NIK, NPWP, NIP, bank account numbers, bank names, WhatsApp numbers, KTP links, surat izin links, PDF links, area codes
- Scans for SQLi and XSS with 1,000,000+ dynamically generated payloads
- Runs Dalfox context‑aware XSS engine (HTML, Attribute, JavaScript, URL, DOM, CSP bypass, mXSS, Blind XSS)
- Checks Business Logic Errors, Mass Assignment, and Rate Limit
- Detects Deface with full PoC
- Checks for WP Activity Log RCE (CVE‑2026‑54806)
- Performs port scanning on common ports
- Generates PoC for every finding (cURL + URL)
- Optionally runs AI analysis and generates a PDF report
- Saves results as JSON and auto‑generates an HTML report

### Attack Mode
Attack flags are mutually exclusive; choose one method at a time.

| Flag | Method |
|------|--------|
| `--dos` | HTTP flood (Layer 7) using GET/POST/HEAD requests |
| `--ddos` | Multi‑method attack: HTTP + SYN + SSL Renegotiation + UDP simultaneously |
| `--syn` | SYN flood (Layer 4) – spoofed TCP SYN packets |
| `--ssl-reneg` | SSL renegotiation attack – exhaust server resources |
| `--udp` | UDP flood – sends large UDP packets to random ports |

Additional attack options:
- `--threads N` – Number of concurrent threads (default: 200, max recommended 1000)
- `--duration N` – Attack duration in seconds (default: 30)

**Examples:**
```bash
# HTTP flood for 60 seconds with 500 threads
python ghostscanner.py -u https://target.com --dos --threads 500 --duration 60

# Full DDOS (HTTP+SYN+SSL+UDP) with proxy rotation
python ghostscanner.py -u https://target.com --ddos --threads 300 --duration 30 --proxy-list proxies.txt

# SYN flood only
python ghostscanner.py -u https://target.com --syn --threads 200 --duration 20
```

### WordPress Activity Log Exploit (CVE‑2026‑54806)

| Option | Description |
|--------|-------------|
| `--wp-check` | Check if target is vulnerable to CVE‑2026‑54806 |
| `--wp-command CMD` | Execute a system command via blind RCE |

**Examples:**
```bash
python ghostscanner.py -u https://target.com --wp-check
python ghostscanner.py -u https://target.com --wp-command "id"
```

## PROXY CONFIGURATION

Ghost Scanner supports HTTP, HTTPS, and SOCKS5 proxies. They are used for both scanning and attacks to hide your IP and distribute requests.

### Proxy File Format
```
http://username:password@192.168.1.100:8080
socks5://proxy.example.com:1080
http://203.0.113.50:3128
```
- Lines starting with `#` are ignored.
- If no protocol is specified, `http://` is assumed.
- Use `--validate-proxy` to remove dead proxies before use (increases startup time).

### Built‑in Proxy List
If no proxy file is provided and `--no-proxy` is not set, a default set of free public proxies is loaded automatically from ProxyScrape API.

## OUTPUT AND REPORTS

After a scan, the following files are generated:

1. **JSON file** (`scan_<timestamp>.json`) – contains all raw data, vulnerabilities, PoCs, sensitive findings, SQL extracted data, and statistics. Suitable for automated parsing.

2. **HTML report** (`scan_<timestamp>.html`) – human‑readable summary with vulnerability categories, payload examples, and extracted sensitive information.

3. **PDF report** (`report_<timestamp>.pdf`) – if `--pdf` is enabled, a professional printable report with all findings, PoCs, and AI analysis (if `--ai` is set).

The JSON structure includes:
- `target`, `domain`, `domain_category` (Government, Education, Police, Military, Medical, Business, Other)
- `vulnerabilities` – grouped by type, with parameters, payloads, confidence scores, evidence, and PoC (cURL + URL)
- `sensitive_data` – NIK, NPWP, NIP, bank accounts, bank names, WhatsApp numbers, KTP links, surat izin links, PDF links, area codes (province, kabupaten, kecamatan), emails, phones, API keys, JWT tokens, source code snippets
- `sql_extracted` – database name, tables, columns, sample data
- `ports` – open ports discovered
- `summary` – total findings and risk distribution
- `ai_analysis` – AI-generated summary and recommendations (if enabled)

## TUTORIAL – STEP BY STEP

### Scenario 1: Full Scan with AI + PDF
```bash
python ghostscanner.py -u https://target.com -v --ai --pdf
```
- Automatically classifies domain type
- Extracts all sensitive Indonesian data (NIK, NPWP, NIP, bank, etc.)
- Runs SQLi, XSS (Dalfox), Business Logic, Mass Assignment, Rate Limit, Deface, WP Log checks
- Generates JSON, HTML, and PDF reports
- AI analysis with actionable recommendations

### Scenario 2: Quick Scan (Fast)
```bash
python ghostscanner.py -u https://target.com --quick
```
- Uses fewer payloads per category
- Skips AI and PDF generation
- Ideal for initial reconnaissance

### Scenario 3: Conducting a DDOS Test on Your Own Server
```bash
python ghostscanner.py -u https://your-server.com --ddos --threads 250 --duration 15
```
- Simulates a distributed attack with multiple methods
- Useful for capacity testing and firewall rule validation

## TROUBLESHOOTING

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'cloudscraper'` | Install missing package: `pip install cloudscraper` |
| SSL certificate errors | Add `--no-proxy` or use `verify=False` (already set) |
| Scan takes too long | Use `--quick` to reduce payload count |
| Proxy validation fails | Ensure proxies are reachable; try without `--validate-proxy` |
| `fake-useragent` errors | Install: `pip install fake-useragent` |
| Permission denied (Linux) | Run `chmod +x ghostscanner.py` |
| Termux: `pkg` not found | Make sure you are using Termux (not a normal shell) |

### Performance Tips
- For faster scans, use `--quick` (reduces payloads to 10 per category).
- Increase `--threads` for port scanning (default 300).
- Use a reliable proxy list to avoid rate‑limiting.

## DISCLAIMER

Ghost Scanner is a powerful tool designed for **ethical security research, penetration testing, and educational purposes**.

- **You must have explicit authorisation** to test any system that you do not own.
- Unauthorised use of this tool is illegal and may result in severe criminal penalties.
- The author (ARGA NOT DEV) is **not responsible** for any misuse, damage, or legal consequences arising from the use of this software.
- By using this tool, you agree to accept full responsibility for your actions and to use it only in compliance with all applicable laws.

## VERSION HISTORY

- **4.2 (SENSITIVE HUNTER)** – 2026‑09‑10
  - Added domain classification (Government, Education, Police, Military, Medical, Business, Other)
  - Added sensitive Indonesian data extraction: NIK, NPWP, NIP, bank account numbers, bank names, WhatsApp numbers, KTP links, surat izin links, PDF links, area codes
  - Integrated ProxyScrape API for dynamic proxy fetching
  - Enhanced sensitive data extraction with deduplication and context detection
  - Updated PDF report to include domain category and all sensitive data
  - All previous features from v4.1 retained and improved

- **4.1 (OMNI XSS + WP LOG EXPLOIT)** – 2026‑09‑09
  - Added Dalfox XSS engine (context‑aware, DOM, CSP bypass, mXSS, Blind XSS)
  - Integrated CVE‑2026‑54806 detection and blind RCE exploitation
  - Added full Deface PoC with curl, indicators, and screenshot simulation
  - Enhanced AI analysis for PoC evaluation and recommendations

- **3.5 (ULTRA SAVAGE)** – 2026‑09‑08
  - Added 1,000,000+ SQLi and XSS payloads
  - Integrated AI analysis with `--ai` flag
  - Added PDF report generation with `--pdf` flag
  - Implemented PoC generation (cURL + URL) for every finding
  - Added SQL data extraction (database, tables, columns, sample data)
  - Enhanced sensitive data extraction: NIK, KTP, NPWP, employee/staff data
  - Added Business Logic Error, Mass Assignment, and Rate Limit checks

- **2.0 (FAST DEMON)** – 2026‑09‑03
  - Optimised payload count for speed (30 per category)
  - Added `--quick` mode (10 payloads)
  - Improved progress bars and non‑blocking behaviour
  - Custom help menu with clear screen and loading animation
  - Enhanced proxy validation and rotation

- **1.0 (DEMON)** – 2026‑08‑31
  - Initial release with 150k+ payloads, WAF bypass, double validation, attack engine, HTML/JSON reporting

## CONTACT

For support, suggestions, or collaboration, please contact the developer via the official channel (if any). This project is maintained by **ARGA NOT DEV**.

## ACKNOWLEDGEMENTS

Special thanks to the open‑source community for the libraries and inspiration that made this tool possible.

**THANKS TO**
1. God
2. Parents
3. GhostTeam
4. Bestfriends
5. Friends

**JOIN CYBERSECURITY TELEGRAM**  
[https://t.me/roompubiccybersecurity](https://t.me/roompubiccybersecurity)
[https://t.me/+NP7XHa6AIZRmNGU1](https://t.me/+NP7XHa6AIZRmNGU1)
**ALL COPYRIGHT RESERVED**  
© 2026 GhostTeam – Ghost Scanner