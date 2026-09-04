# Security Policy

## Supported Versions

Ghost Scanner is actively maintained and security updates are provided for the latest stable release. Older versions may receive critical patches on a best-effort basis.

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :warning: Limited  |
| < 1.0   | :x:                |

**Notes:**
- `2.0.x` – Fully supported with regular security updates.
- `1.0.x` – Only critical security patches will be considered.
- `< 1.0` – Not supported. Please upgrade to the latest version.

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability in Ghost Scanner, please report it responsibly.

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Send an email to: `cozystoreid992@gmail.com`
   - Use the subject prefix: `[GHOST-SCANNER SECURITY]`
   - Include a clear description of the vulnerability.
   - Provide steps to reproduce (proof of concept, if possible).
   - Mention the version affected.
3. Alternatively, you can contact via Telegram: [@cozystoreoffc](@Cozy_Store_official) (encrypted chat preferred).

### What to Expect

- **Initial Response** – Within 48 hours, we will acknowledge receipt of your report.
- **Status Updates** – We will provide updates every 5-7 days until the issue is resolved.
- **Acceptance** – If the vulnerability is confirmed, we will:
  - Patch it in the next release.
  - Credit you in the release notes (unless you prefer to remain anonymous).
- **Decline** – If the issue is out of scope or a false positive, we will explain why.

### Responsible Disclosure Policy

We kindly ask that you:
- Allow us a reasonable timeframe (typically 30 days) to fix the issue before disclosing it publicly.
- Do not exploit the vulnerability for malicious purposes.
- Do not test on systems you do not own or have explicit permission to test.

### Scope

This policy applies to:
- The official Ghost Scanner source code (`ghostscanner.py` and all modules).
- The build process and release artifacts.

Out of scope:
- Third-party dependencies (please report to their respective maintainers).
- Issues that require physical access to a system or social engineering.

## Security Best Practices for Users

As a user of Ghost Scanner, you are responsible for:

- **Using the tool only on systems you own or have explicit permission to test.**
- **Keeping your installation up to date** to receive the latest security patches.
- **Reviewing proxy lists and configurations** to avoid malicious proxies.
- **Never sharing your proxy credentials** or sensitive data publicly.

## Acknowledgements

We appreciate the security researchers and ethical hackers who help make Ghost Scanner safer for everyone. Your contributions are valued and respected.

**ALL COPYRIGHT RESERVED**  
© 2026 GhostTeam – Ghost Scanner
