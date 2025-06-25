## How to Use LYNX - Web Security Suite 2025

This README explains how to use LYNX, a powerful web vulnerability exploitation tool.


---

## 🔧 Requirements

Requirement	Details

Python	Version 3.x or higher
Dependencies	Install using the command below if needed:


pip install -r requirements.txt


---

## 📁 Project Structure

The project contains main scripts and a bash launcher located in the root directory, which helps manage the tool’s modules.

Current Modules

Module Name	Description

XSS Scanner	Tests for reflected and stored XSS
Path Scanner	Brute-forces directories and endpoints
Smap	Collects basic information about a target



---

🧭 Using the Interactive Menu

In the root directory, there's a bash file called lynx.sh that makes it easier to run any module.

Run:

./lynx

Then see available options:

--help

or

-h


---

## 🖥️ Using Direct Command Line

You can also run the modules directly via:

python3 dev.py (--ModuleName) (Chosen tool command)

Example:

python3 dev.py --path -u www.example.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug


---

## ⚔️ Practical Usage

XSS Scanner

Option	Description

-T, --type	Type of XSS: -Tr for reflected, -Ta for stored
-l, --limit	Limit of payloads used (e.g. -l1000)
-t, --thread	Number of threads (e.g. -t30)
-d, --debug	Enables verbose mode (not required)


Reflected XSS

Option	Description

-u, --url	Target URL with parameter (e.g. -u www.example.com/login?uid=10)


Stored XSS

Option	Description

-p, --post	Target POST URL (e.g. -p www.example.com)
-v, --view	URL to view the injected payload (e.g. -v www.example2.com)


Example:

-Tr -u www.example.com -l200 -t20 --debug


---

Path Scanner

Option	Description

-u, --url	Target URL (e.g. -u www.example.com)
-w, --wordlist	Path wordlist file (default = path.txt)
-l	Number of payloads (max/default = 5000)
-t	Number of threads (default = 10)
-s, --status	Status codes that count as success (e.g. -s 200 301 302)
-d, --delay	Delay range between requests (e.g. -d 0.3 0.5)
-m, --mode	Output mode (normal or debug, default = normal)


Example:

-u www.example.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug


---

Smap

Option	Description

-u, --url	Target URL (e.g. -u www.example.com)


Example:

--url www.example.com

Simple as that.


---

