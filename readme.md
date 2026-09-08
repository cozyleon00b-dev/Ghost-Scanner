# GHOST SCANNER – ULTRA SAVAGE+

**All‑in‑One Security Assessment & Penetration Testing Framework**  
Version 3.6 – ULTRA SAVAGE+  
Release Date: 2026‑09‑08

## OVERVIEW

Ghost Scanner is a modular, high‑performance security tool designed for ethical hacking, vulnerability assessment, and stress testing. It combines:

- **Advanced Web Vulnerability Scanning** – SQLi, XSS, LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE, Business Logic Errors, Mass Assignment, Rate Limit
- **Deface Detection** – automatically checks for indicators of website defacement (e.g., “hacked”, “defaced”, “owned by”) with proof‑of‑concept
- **Massive Payload Generation** – 1,000,000+ dynamic payloads for SQLi and XSS (sourced from W3Schools & OWASP) with intelligent sampling for speed
- **SQL Data Extraction** – automatically extract database name, tables, columns, and sample data when SQL injection is found
- **Proof‑of‑Concept (PoC) Generation** – every finding includes a cURL command and direct URL for replication
- **AI‑Powered Analysis** – optional integration with CodeCraft Claude Opus 5 for intelligent vulnerability analysis and recommendations
- **PDF Report Generation** – professional, printable reports with all findings, PoCs, sensitive data, and AI analysis
- **Sensitive Data Extraction** – emails, phone numbers, NIK, NPWP, KTP, API keys, JWT tokens, AWS/Azure/GCP keys, source code snippets, and employee/staff data
- **Port Scanning** – fast TCP port discovery on common service ports
- **Proxy Rotation** – use SOCKS/HTTP proxies from file or built‑in list, with optional validation
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

3. **(Optional) Prepare a proxy list** – one proxy per line in a text file, e.g. `proxies.txt`:
   ```
   http://user:pass@proxy1:8080
   socks5://proxy2:1080
   http://proxy3:3128
   ```

4. **Make the script executable** (Linux/macOS/Termux):
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
| `-h, --help` | Show the help menu |

### Scan Mode (Default)
When no attack flag is given, the script performs a full vulnerability scan.

**Example:**
```bash
python ghostscanner.py -u https://target.com -v --proxy-list proxies.txt --validate-proxy --pdf --ai
```

**What it does:**
- Accesses the target with cloudscraper + proxy rotation
- Extracts parameters, forms, and API endpoints
- Runs SQLi and XSS scans with 1,000,000+ dynamically generated payloads
- Performs Deface Detection on the homepage
- Checks Business Logic Errors, Mass Assignment, and Rate Limit
- Extracts sensitive data (emails, NIK, KTP, API keys, employee data, etc.)
- Performs port scanning on common ports
- Generates PoC for every finding (cURL + URL)
- Optionally runs AI analysis (Claude Opus 5) and generates a PDF report
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

---

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
If no proxy file is provided and `--no-proxy` is not set, a default set of free public proxies is loaded automatically.

---

## OUTPUT AND REPORTS

After a scan, the following files are generated:

1. **JSON file** (`scan_<timestamp>.json`) – contains all raw data, vulnerabilities, PoCs, sensitive findings, SQL extracted data, and statistics. Suitable for automated parsing.

2. **HTML report** (`scan_<timestamp>.html`) – human‑readable summary with vulnerability categories, payload examples, and extracted sensitive information.

3. **PDF report** (`report_<timestamp>.pdf`) – if `--pdf` is enabled, a professional printable report with all findings, PoCs, and AI analysis (if `--ai` is set).

The JSON structure includes:
- `target`, `domain`, `timestamp`
- `vulnerabilities` – grouped by type, with parameters, payloads, confidence scores, evidence, and PoC (cURL + URL)
- `sql_extracted` – database name, tables, columns, sample data
- `sensitive_data` – emails, phones, NIK, KTP, API keys, JWT tokens, AWS/Azure/GCP keys, source code snippets
- `ports` – open ports discovered
- `summary` – total findings and risk distribution
- `ai_analysis` – AI-generated summary and recommendations (if enabled)

---

## TUTORIAL – STEP BY STEP

### Scenario 1: Scanning a Government Website with AI + PDF
```bash
python ghostscanner.py -u https://www.madiunkota.go.id -v --proxy-list myproxies.txt --ai --pdf
```
- Bypasses Cloudflare if present
- Extracts parameters and forms
- Runs SQLi and XSS scans with 1M+ payloads
- Performs Deface Detection
- Scans open ports and shows them
- Extracts emails, NIK, KTP, API keys, employee data
- Generates PoC for each finding
- Performs AI analysis (Claude Opus 5) and creates a PDF report

### Scenario 2: Testing a Vulnerable Lab
```bash
python ghostscanner.py -u http://vulnerable-lab.local --no-proxy --verbose --quick
```
- Disables proxies for internal testing
- Verbose mode shows each request in real time
- Quick mode reduces payloads for speed

### Scenario 3: Conducting a DDOS Test on Your Own Server
```bash
python ghostscanner.py -u https://your-server.com --ddos --threads 250 --duration 15
```
- Simulates a distributed attack with multiple methods
- Useful for capacity testing and firewall rule validation

---

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

---

## DISCLAIMER

Ghost Scanner is a powerful tool designed for **ethical security research, penetration testing, and educational purposes**.

- **You must have explicit authorisation** to test any system that you do not own.
- Unauthorised use of this tool is illegal and may result in severe criminal penalties.
- The author (ARGA NOT DEV) is **not responsible** for any misuse, damage, or legal consequences arising from the use of this software.
- By using this tool, you agree to accept full responsibility for your actions and to use it only in compliance with all applicable laws.

---

## VERSION HISTORY

- **3.6 (ULTRA SAVAGE+)** – 2026‑09‑08
  - Added **Deface Detection** – automatically checks for deface indicators (hacked, defaced, etc.) with PoC
  - AI model upgraded to **Claude Opus 5** via CodeCraft API
  - Optimised request handling for speed and reliability
  - Cross‑platform support for Arch, BlackArch, Termux, CMD, PowerShell
  - All previous features from v3.5 retained

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

---

## CONTACT

For support, suggestions, or collaboration, please contact the developer via the official channel (if any). This project is maintained by **ARGA NOT DEV**.

---

## ACKNOWLEDGEMENTS

Special thanks to the open‑source community for the libraries and inspiration that made this tool possible.

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