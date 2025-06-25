
# How to Use LYNX - Web Security Suite 2025

This README explains how to **use LYNX**, a powerful web vulnerability exploitation tool.

---

## 🔧 Requirements

| Requirement        | Details                                |
|--------------------|----------------------------------------|
| Python             | Version 3.x or higher                  |
| Dependencies       | Install using: `pip install -r requirements.txt` |

---

## 📁 Project Structure

The project contains main scripts and a **bash launcher** in the root directory to manage modules.

### Available Modules

| Module Name     | Description                            |
|------------------|----------------------------------------|
| XSS Scanner      | Tests for reflected and stored XSS     |
| Path Scanner     | Brute-forces directories/endpoints     |
| Smap             | Collects basic info about the target   |

---

## 🧭 Using the Interactive Menu

In the root directory, there's a bash file `lynx.sh` for running modules easily.

### Example:

```bash
./lynx
```

Then show available options:

```bash
--help
```

or

```bash
-h
```

---

## 🖥️ Using Command Line Directly

You can run the modules directly:

```bash
python3 dev.py (--ModuleName) (Tool options)
```

**Example:**

```bash
python3 dev.py --path -u www.example.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug
```

---

## ⚔️ Practical Usage

### XSS Scanner

| Option           | Description                                           |
|------------------|-------------------------------------------------------|
| `-T, --type`     | Type of attack: `-Tr` for reflected, `-Ta` for stored |
| `-l, --limit`    | Limit of payloads used (e.g. `-l1000`)                |
| `-t, --thread`   | Number of threads (e.g. `-t30`)                       |
| `-d, --debug`    | Enables verbose mode (optional)                       |

#### Reflected XSS

| Option         | Description |
|----------------|-------------|
| `-u, --url`     | Target URL with parameter (e.g. `-u www.example.com/login?uid=10`) |

#### Stored XSS

| Option         | Description |
|----------------|-------------|
| `-p, --post`    | Target POST URL (e.g. `-p www.example.com`) |
| `-v, --view`    | URL to view the injected payload (e.g. `-v www.example2.com`) |

**Example:**

```bash
-Tr -u www.example.com -l200 -t20 --debug
```

---

### Path Scanner

| Option           | Description                                                   |
|------------------|---------------------------------------------------------------|
| `-u, --url`      | Target URL (e.g. `-u www.example.com`)                         |
| `-w, --wordlist` | Path wordlist file (default = `path.txt`)                      |
| `-l`             | Number of payloads (max/default = `5000`)                      |
| `-t`             | Number of threads (default = `10`)                             |
| `-s, --status`   | Status codes considered successful (e.g. `-s 200 301 302`)     |
| `-d, --delay`    | Delay between requests (e.g. `-d 0.3 0.5`)                      |
| `-m, --mode`     | Output mode (`normal` or `debug`, default = `normal`)          |

**Example:**

```bash
-u www.example.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug
```

---

### Smap (Information Scanner)

| Option           | Description                       |
|------------------|-----------------------------------|
| `-u, --url`      | Target URL (e.g. `-u www.example.com`) |

**Example:**

```bash
--url www.example.com
```

*That’s it. Easy as hell.*

---

