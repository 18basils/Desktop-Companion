# Security Policy

## Supported Versions

We actively maintain and provide security updates for the current major release of **Desktop Companion & Companion Hub**:

| Version | Supported          | Status                                   |
| :------ | :----------------- | :--------------------------------------- |
| 2.0.x   | :white_check_mark: | Currently Supported (Universal Release)  |
| < 2.0   | :x:                | Deprecated                               |

---

## Reporting a Vulnerability

The Desktop Companion team takes the security and privacy of our users seriously. If you discover a security vulnerability, we appreciate your help in disclosing it to us responsibly.

### How to Report
1. **GitHub Private Vulnerability Reporting**:
   - Navigate to the [Security Advisories](https://github.com/18basils/Desktop-Companion/security/advisories) tab on GitHub and click **"Report a vulnerability"**.
2. **Direct Contact**:
   - If private vulnerability reporting is not available, please open an issue with the label `security` without exposing sensitive exploit payloads publicly, or contact the project maintainer via their GitHub profile [@18basils](https://github.com/18basils).

### What to Include in Your Report
To help us triage and resolve the issue quickly, please provide:
* A clear description of the vulnerability and its potential impact.
* Step-by-step instructions or a minimal Proof of Concept (PoC) to reproduce the issue.
* Affected platform(s) (Windows, Android, macOS, iOS, or Web Portal).
* Proposed remediations or patches if available.

### Response & Resolution Timeline
* **Initial Acknowledgement**: Within **48 hours** of receiving the report.
* **Assessment & Triage**: Within **5 business days**, confirming severity and scope.
* **Patch Release**: High or critical vulnerabilities are prioritized for immediate patch release, followed by an advisory update.

---

## Built-In Security Architecture

Desktop Companion is built with defense-in-depth principles across all supported targets:

### 1. Windows Desktop Application
* **Non-Elevated User Space**: The application and installer run exclusively within user space (`%LocalAppData%\Programs\Desktop Companion`). It requires **zero administrative or UAC privileges**.
* **Hardened Local IPC**: The local single-instance communication socket (`companion_ipc`) enforces command whitelisting (`SUMMON`), rate limiting (1.5s debounce), and bounded message buffers to prevent local Denial of Service (DoS) attacks.
* **Safe Avatar & Image Processing**: Avatar uploads undergo MIME and header validation via `QImageReader`, with strict file extension whitelisting (`.gif`, `.png`) and a 15 MB file size boundary.
* **Zip-Slip Traversal Defense**: All archive extraction routines enforce canonical path validation before writing files to disk to prevent directory traversal exploits.
* **Resource Exhaustion Prevention**: Painting and rendering loops explicitly manage and terminate GDI painters to prevent handle leaks.

### 2. Android & Apple Targets
* **Sandboxed Native Runtimes**: Standard mobile platform sandboxing with explicit permission boundaries.
* **Local-First Architecture**: Hydration tracking, alarms, and avatar preferences are stored locally on-device without remote telemetry transmission.

### 3. Web Portal (`https://mycompanionhub.web.app`)
* **Strict Transport Security (HSTS)**: `max-age=31536000; includeSubDomains; preload`.
* **Content Security Policy (CSP)**: Whitelists only trusted origins (`'self'`, Google Tag Manager, Google Analytics, QR Server).
* **Anti-Clickjacking**: `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'`.
* **MIME Sniffing Defense**: `X-Content-Type-Options: nosniff`.
* **Crawler & Download Shielding**: High-bandwidth binary downloads are shielded with `X-Robots-Tag: noindex, nofollow`, `Content-Disposition: attachment`, and CDN edge caching.
