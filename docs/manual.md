# 📖 How to Use LYNX - Web Security Suite 2025

This guide explains how to **use the LYNX CLI** to scan, fuzz, and gather information from web targets — all from the terminal.

---

## ⚙️ Requirements

| Requirement       | Description                                     |
|-------------------|-------------------------------------------------|
| Python            | Version 3.x is required                         |
| Dependencies      | Run `pip install -r requirements.txt` to install them |

---

## 📁 Project Structure

The tool is modular and organized with a main script `dev.py` and a helper bash menu `lynx.sh`.

| Module        | Description                                           |
|---------------|-------------------------------------------------------|
| XSS Scanner   | Tests for reflected and stored XSS vulnerabilities    |
| Path Scanner  | Bruteforce common directories/files on the target     |
| Smap          | Collects technical and metadata info from a URL       |

---

## 🚀 Interactive Menu (Easy Mode)

From the root folder, run the script:

```bash
./lynx

Then use:

--help  or  -h

To see available modules and flags.


---

🔧 Direct CLI Usage (Power Mode)

python3 dev.py [--module] [flags]

Example:

python3 dev.py --path -u www.example.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug


---

💥 Modules & Flags

🧪 XSS Scanner

Flag	Description	Example

-T, --type	Type of attack (r for reflected, a stored)	-Tr
-l, --limit	Limit of payloads to test	-l1000
-t, --thread	Number of threads	-t30
-d, --debug	Show debug info (optional)	--debug


Reflected XSS Specific

Flag	Description	Example

-u, --url	Target URL with a query param	-u https://site.com/search?q=test


Stored XSS Specific

Flag	Description	Example

-p, --post	URL where payload will be injected	-p https://site.com/form
-v, --view	URL where result will be viewed	-v https://site.com/posts


Example usage:

-Ta -p https://site.com/form -v https://site.com/posts -l200 -t20 --debug


---

📂 Path Scanner

Flag	Description	Example

-u, --url	Target base URL	-u https://target.com
-w, --wordlist	Wordlist file (default: path.txt)	-w path.txt
-l	Number of payloads (max 5000, default 5000)	-l5000
-t	Number of threads (default 10)	-t60
-s, --status	Status codes to treat as "valid"	-s 200 301 403
-d, --delay	Delay between requests (range)	-d 0.2 0.4
-m, --mode	Output mode: normal or debug	-m debug


Example usage:

--path -u https://target.com -w path.txt -l5000 -t50 -s 200 301 -d 0.2 0.4 -m debug


---

🌐 Smap - Info Scanner

Flag	Description	Example

-u, --url	Target website URL	-u https://example.com


No other flags needed — it's that simple.

Example usage:

--smap -u https://example.com


---

🔐 Legal Note

This tool is for educational and authorized testing only.
Do not use it on any system you don’t own or don’t have explicit permission to test.
The author is not responsible for any misuse.