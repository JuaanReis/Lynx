
#  LYNX - v1.0.2 Changelog

##  Update Highlights

###  New Features

| Feature                     | Description                                  |
|-----------------------------|----------------------------------------------|
| **Tor Proxy Support**       | Added proxy integration using Tor            |
| **Header Spoofing**         | Custom headers to disguise requests          |
| **New Payloads**            | Expanded attack vectors                      |
| **Dev Mode**                | Easier debugging and module development      |
| **Sensitive Host Blocking**| Prevents scanning on blacklisted targets     |

---

### Removed

| Removed Component           | Reason |
|-----------------------------|--------|
| Proxy from Path Scanner     | Reworked for better compatibility |
| System Info from Menu       | Cleaned up interface |
| AI Folder                   | Restructured for future integration |

---

### Fixes & Improvements

| Fix/Improvement                     | Description |
|-------------------------------------|-------------|
| XSS Tool Modularization             | Separated into modules for better maintenance |
| PATH Scanner Response Check         | Fixed logic for detecting real paths |
| SMAP Port Scan Fix                  | Corrected issue in port checking      |
| Log Files with `.log` Extension     | Standardized log file outputs         |

---

## Coming Soon

###  New Modules

- Remote Code Execution (RCE)
- SQL Injection (SQLi)
- Command Injection

### UX & UI Improvements

- Better user experience across modules
- More intuitive CLI feedback

### System Enhancements

- Rewritten modules in **C** for performance
- DEV mode for adding new modules easily
- More stable and reliable core
- JSON Report generation
- AI integration

---

## Module Overviews

### SMAP (Site Mapper)

| Feature                     | Description |
|-----------------------------|-------------|
| General Info                | Site title, domain, and SSL check |
| Headers & Cookies           | CORS, custom headers, cookie data |
| Backend Technologies        | Attempts tech fingerprinting |
| Port Scanning               | Basic open port detection |
| Forms                       | Detects method, fields, values |
| Links                       | Internal and external link extraction |
| Parameter Check             | Detects URL parameters |

---

### XSS

#### Reflected XSS

| Feature                     | Description |
|-----------------------------|-------------|
| Local Result                | Executed only in the response |
| Parameter Based             | Looks for vulnerable parameters |
| GET Method                  | Supports GET requests |
| Dangerous Context Detection | Checks if payload is in a critical context |

#### Stored XSS

| Feature                     | Description |
|-----------------------------|-------------|
| Server-Side Persistence     | Payload stored on the server |
| POST Method                 | Injects via form submissions |

---

### PATH Scanner

| Feature                     | Description |
|-----------------------------|-------------|
| Path Injection              | Injects paths into target URLs |
| False Positive Avoidance    | Analyzes HTML to filter invalid results |

---

