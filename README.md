# 🕵️ OSINT Reconnaissance — Tesla Case Study
### CEH Journey — Week 2 | Assessment 2

![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)

---

## ⚙️ Installation & Setup

### Step 1 — Install required tools
```bash
sudo apt update
sudo apt install whois dnsutils whatweb theharvester amass -y
```

### Step 2 — No pip install needed
Basic modules use only built-in Python libraries + free APIs.

---

## 🚀 How To Run — Complete Usage Guide

### Basic scan (fast — under 60 seconds)
```bash
python3 osint_collector.py --target tesla.com
```
**Modules that run automatically:**
- ✅ Module 1 — DNS Enumeration
- ✅ Module 2 — WHOIS Lookup
- ✅ Module 3 — IP Geolocation
- ✅ Module 4 — Technology Detection
- ✅ Module 6 — Shodan Query Reference
- ❌ Module 5 — Subdomain Enum (requires --all)

---

### Full scan including subdomains (slow — 5 to 15 mins)
```bash
python3 osint_collector.py --target tesla.com --all
```
**What --all adds:**
- ✅ Module 5 — Subdomain Enumeration via Amass + theHarvester + wordlist

> ⚠️ Module 5 is separate because subdomain enumeration
> takes 5-15 minutes. Basic modules finish in under 60 seconds.
> Use --all only when you want comprehensive results.

---

### Save output to a file
```bash
python3 osint_collector.py --target tesla.com --output tesla_report.txt
```

---

### Full scan + save (most complete — recommended)
```bash
python3 osint_collector.py --target tesla.com --all --output tesla_full.txt
```

---

### Run on any target
```bash
python3 osint_collector.py --target google.com
python3 osint_collector.py --target xiaomi.com --all --output xiaomi.txt
```

---

## 📋 Module Reference

| Module | Flag | Time | What It Does |
|--------|------|------|-------------|
| 1 - DNS | always runs | ~5s | A, MX, NS, TXT, CNAME records |
| 2 - WHOIS | always runs | ~5s | Registrar, age, owner |
| 3 - Geolocation | always runs | ~5s | Country, city, ISP, coordinates |
| 4 - Tech Detection | always runs | ~10s | Server, frameworks, WAF |
| 5 - Subdomain Enum | `--all` only | 5-15 min | Amass + theHarvester + wordlist |
| 6 - Shodan Queries | always runs | instant | Manual Shodan reference queries |

---

## 🔧 Troubleshooting

```bash
# whois not found
sudo apt install whois -y

# amass not found
sudo apt install amass -y

# whatweb not found
sudo apt install whatweb -y

# theHarvester not found
sudo apt install theharvester -y

# Geolocation not working — test connection
curl -s https://ipapi.co/json/
```

---
### CEH Journey — Week 2 | Assessment 2

![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
![Tools](https://img.shields.io/badge/Tools-Shodan_|_Amass_|_theHarvester_|_WHOIS-blue?style=flat-square)
![Level](https://img.shields.io/badge/Level-Beginner-orange?style=flat-square)
![Type](https://img.shields.io/badge/Type-OSINT_|_Reconnaissance-red?style=flat-square)

> ⚠️ All information gathered in this project is publicly available. No private systems were accessed. This is purely educational OSINT research.

---

## 📌 Objective

Demonstrate how Open Source Intelligence (OSINT) techniques can be used to build a comprehensive profile of a target organization using only publicly available information — without ever touching their systems.

**Target:** Tesla, Inc. (tesla.com)

---

## 🧠 What is OSINT?

Open Source Intelligence is the collection and analysis of information gathered from **publicly available sources** to produce actionable intelligence.

Sources include: websites, DNS records, WHOIS databases, search engines, social media, Shodan, certificate transparency logs, and more.

```
OSINT is used by:
├── Penetration testers    → Pre-engagement reconnaissance
├── SOC analysts           → Threat intelligence
├── Law enforcement        → Investigations
├── Journalists            → Research
└── Attackers              → Target profiling (why defenders must understand it)
```

---

## 🛠️ Tools Used

| Tool | Purpose | Command |
|------|---------|---------|
| **WHOIS** | Domain registration info | `whois tesla.com` |
| **Nmap** | IP + service detection | `nmap -sV tesla.com` |
| **theHarvester** | Emails, subdomains, IPs | `theHarvester -d tesla.com -b all` |
| **Amass** | Subdomain enumeration | `amass enum -d tesla.com` |
| **Shodan** | Internet-exposed assets | `shodan search hostname:tesla.com` |
| **WhatWeb** | Technology fingerprinting | `whatweb tesla.com` |

---

## 📊 Findings — Tesla Intelligence Report

### Company Overview
| Field | Information |
|-------|------------|
| **Company Name** | Tesla, Inc. |
| **Key Products** | Electric Vehicles, Solar Panels, Energy Storage, AI |
| **Scope** | Automobile, Artificial Intelligence, Robotics, Energy |
| **Website** | www.tesla.com |

### Website Intelligence
| Field | Finding |
|-------|---------|
| **FQDN** | www.tesla.com |
| **IP Address** | 23.39.40.66 |
| **Hosting Country** | Netherlands |
| **Hosting Company** | Akamai Technologies |
| **Domain Age** | ~33 years |
| **Technologies** | WordPress, PHP, MySQL, React Framework |
| **Load Balancer** | Akamai Load Balancer |
| **WAF** | Akamai WAF |
| **CDN** | Akamai CDN |
| **Shared Hosting** | No (dedicated infrastructure) |

### Geolocation
| Field | Value |
|-------|-------|
| **Server Location** | Netherlands (Akamai Edge Node) |
| **CDN Edge Nodes** | Global (Akamai network) |

### Subdomain Enumeration
Tools used: **Amass** + **theHarvester**

| Subdomain | Purpose |
|-----------|---------|
| shop.tesla.com | E-commerce store |
| service.tesla.com | Service portal |
| api.tesla.com | API endpoint |
| auth.tesla.com | Authentication |
| cdn.tesla.com | Content delivery |
| model3.tesla.com | Product page |
| owners.tesla.com | Owner portal |

**Total subdomains discovered:** 356 live domains, 901 subdomains

### Key Intelligence Summary (Mind Map)
```
                        TESLA
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   Key Services      Technologies        Website
   ─────────────     ────────────        ───────
   • Insurance       • WordPress         • www.tesla.com
   • Charging        • PHP               • IP: 23.39.40.66
   • Maintenance     • MySQL             • Hosted: Netherlands
   • Solar/Roof      • React             • Age: 33 years
                     • Akamai            
        │                 │                 │
   Scope            Load Balancer         CDN
   ─────            ─────────────         ───
   • Automobile      Akamai               Akamai
   • AI                                   
   • Robotics             │
                    Shared Hosting
                    ──────────────
                         NO
```

---

## ⚙️ Methodology

### Phase 1 — Passive Reconnaissance
```bash
# WHOIS lookup
whois tesla.com

# DNS enumeration
nslookup tesla.com
dig tesla.com ANY

# Check domain age and registrar
# → Used: who.is website
```

### Phase 2 — Active Reconnaissance
```bash
# Nmap service scan
nmap -sV --script=http-headers tesla.com

# Technology fingerprinting
whatweb -v tesla.com

# theHarvester - emails and subdomains
theHarvester -d tesla.com -b bing,google,linkedin
```

### Phase 3 — Subdomain Enumeration
```bash
# Amass - comprehensive subdomain enum
amass enum -d tesla.com -o tesla_subdomains.txt

# Check live subdomains
cat tesla_subdomains.txt | httprobe
```

### Phase 4 — Shodan Intelligence
```
Search queries used:
→ hostname:tesla.com
→ org:"Tesla Motors"
→ ssl.cert.subject.cn:tesla.com
```

---

## 🚨 Security Implications

What this OSINT reveals to an attacker:

```
Finding                    → Security Risk
──────────────────────────────────────────────────
356 live subdomains        → Large attack surface
WordPress installation     → Common CMS vulnerabilities
API endpoints exposed      → Potential API abuse
CDN provider identified    → CDN misconfiguration attacks
Hosting provider known     → Targeted infrastructure attacks
```

**Defender's takeaway:** If a beginner can find this in 3 hours using free tools, imagine what a motivated threat actor can discover. Regular OSINT assessments of your own organization are essential.

---

## 🐍 Automation Script

Included: `osint_collector.py` — automates the entire OSINT workflow for any domain.

```bash
python3 osint_collector.py --target example.com --output report.txt
```

See [`osint_collector.py`](./osint_collector.py) for full source.

---

## 💡 What I Learned

- Public information alone can build a surprisingly detailed picture of any organization
- Subdomains are often the weakest link — many are forgotten and unmaintained
- Understanding CDN and WAF infrastructure helps attackers plan bypass strategies — and helps defenders understand what they're protecting
- OSINT is not just a hacker skill — it's a critical skill for any security professional

---

## 🔗 Connect

**Muhammad Owais Raza**
- GitHub: [Mianowaisraza](https://github.com/Mianowaisraza)
- LinkedIn: [muhammad-owais-raza](https://www.linkedin.com/in/muhammad-owais-raza-8693753a7)

---

*Part of my CEH learning journey — documented weekly on LinkedIn and GitHub*
