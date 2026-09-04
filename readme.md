# GHOST SCANNER – ULTIMATE EDITION

**All‑in‑One Security Assessment & Penetration Testing Framework**  
Version 2.0 – FAST DEMON  
Release Date: 2026‑09‑03

## OVERVIEW

Ghost Scanner is a modular, high‑performance security tool designed for ethical hacking, vulnerability assessment, and stress testing. It combines:

- **Advanced Web Vulnerability Scanning** – SQLi, XSS, LFI, RFI, Command Injection, SSTI, NoSQL, LDAP, XXE, SSRF, Path Traversal, Deserialization, RCE
- **Intelligent Payload Generation** – over 150,000 payloads with WAF bypass techniques (optimised for speed)
- **Sensitive Data Extraction** – emails, phone numbers, NIK, NPWP, API keys, JWT tokens, source code snippets
- **Port Scanning** – fast TCP port discovery on common service ports
- **Proxy Rotation** – use SOCKS/HTTP proxies from file or built‑in list, with optional validation
- **Cloudflare & Bot Bypass** – cloudscraper + user‑agent rotation + multi‑attempt fallback
- **Double Validation** – reduce false positives by re‑testing findings with alternative payloads
- **DOS/DDOS Engine** – HTTP flood, SYN flood, SSL renegotiation, UDP flood (multi‑threaded)
- **HTML & JSON Reporting** – structured output for professional audit trails

Ghost Scanner is built for speed, accuracy, and reliability. It is intended for **authorised testing only**.

## INSTALLATION

### Prerequisites
- Python 3.8 or higher
- pip (package installer)
- Git (optional, for cloning)

### Platform‑Specific Setup

#### Termux (Android)
```bash
pkg update && pkg upgrade
pkg install python python-pip git
pip install --upgrade pip
```

#### Kali Linux
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

#### Arch Linux
```bash
sudo pacman -Syu
sudo pacman -S python python-pip git
```

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
   If `requirements.txt` is not available, install manually:
   ```bash
   pip install cloudscraper fake-useragent requests rich cryptography
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

### Global Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL (must include protocol, e.g. `https://example.com`) |
| `-o, --output` | Output JSON file name (default: `results.json`) |
| `-v, --verbose` | Enable verbose logging to console |
| `--proxy-list FILE` | Load proxies from a file (one per line) |
| `--validate-proxy` | Test each proxy before use (slower but more reliable) |
| `--no-proxy` | Disable proxy usage (use your own IP) |
| `--quick` | Quick scan (fewer payloads) |
| `-h, --help` | Show the help menu |

### Scan Mode (Default)
When no attack flag is given, the script performs a full vulnerability scan.

**Example:**
```bash
python ghostscanner.py -u https://target.com -v --proxy-list proxies.txt --validate-proxy
```

**What it does:**
- Accesses the target with cloudscraper + proxy rotation
- Extracts parameters, forms, and API endpoints
- Runs SQLi and XSS scans with optimised payloads (30 per category)
- Discovers open ports
- Extracts sensitive data (emails, keys, source code)
- Saves results as JSON and auto‑generates an HTML report

### Attack Mode
Attack flags are mutually exclusive; choose one method at a time.

| Flag | Method |
|------|--------|
| `--dos` | HTTP flood (Layer 7) using GET/POST/HEAD requests |
| `--ddos` | Multi‑method attack: HTTP + SYN + SSL Renegotiation simultaneously |
| `--syn` | SYN flood (Layer 4) – spoofed TCP SYN packets |
| `--ssl-reneg` | SSL renegotiation attack – exhaust server resources |
| `--udp` | UDP flood (placeholder; sends large UDP packets) |

Additional attack options:
- `--threads N` – Number of concurrent threads (default: 200, max recommended 1000)
- `--duration N` – Attack duration in seconds (default: 30)

**Examples:**
```bash
# HTTP flood for 60 seconds with 500 threads
python ghostscanner.py -u https://target.com --dos --threads 500 --duration 60

# Full DDOS (HTTP+SYN+SSL) with proxy rotation
python ghostscanner.py -u https://target.com --ddos --threads 300 --duration 30 --proxy-list proxies.txt

# SYN flood only
python ghostscanner.py -u https://target.com --syn --threads 200 --duration 20
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
If no proxy file is provided and `--no-proxy` is not set, a default set of free public proxies is loaded automatically.


## OUTPUT AND REPORTS

After a scan, two files are generated:

1. **JSON file** (`scan_<timestamp>.json`) – contains all raw data, vulnerabilities, sensitive findings, and statistics. Suitable for automated parsing.

2. **HTML report** (`scan_<timestamp>.html`) – human‑readable summary with vulnerability categories, payload examples, and extracted sensitive information.

The JSON structure includes:
- `target`, `domain`, `timestamp`
- `vulnerabilities` – grouped by type, with parameters, payloads, confidence scores, and evidence
- `sensitive_data` – emails, phones, API keys, JWT tokens, source code snippets
- `ports` – open ports discovered
- `summary` – total findings and risk distribution
- `anti_block_stats` – request/retry/proxy usage metrics


## TUTORIAL – STEP BY STEP

### Scenario 1: Scanning a Government Website
```bash
python ghostscanner.py -u https://www.madiunkota.go.id -v --proxy-list myproxies.txt
```
- Bypasses Cloudflare if present
- Extracts parameters and forms
- Runs SQLi and XSS scans (optimised)
- Scans open ports and shows them
- Extracts emails, phone numbers, API keys
- Saves JSON + HTML reports

### Scenario 2: Testing a Vulnerable Lab
```bash
python ghostscanner.py -u http://vulnerable-lab.local --no-proxy --verbose
```
- Disables proxies for internal testing
- Verbose mode shows each request in real time

### Scenario 3: Conducting a DDOS Test on Your Own Server
```bash
python ghostscanner.py -u https://your-server.com --ddos --threads 250 --duration 15
```
- Simulates a distributed attack
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

**ALL COPYRIGHT RESERVED**  
© 2026 GhostTeam – Ghost Scanner
