#!/usr/bin/env python3
"""
============================================================
  OSINT Collector
  CEH Journey — Week 2 | Assessment 2
  Author : Muhammad Owais Raza
  GitHub : https://github.com/Mianowaisraza

  Description:
  Automates OSINT reconnaissance on a target domain.
  Performs WHOIS lookup, DNS enumeration, subdomain
  discovery, IP geolocation, and technology detection
  using only built-in Python libraries + free APIs.

  Usage:
    python3 osint_collector.py --target tesla.com
    python3 osint_collector.py --target tesla.com --output report.txt
    python3 osint_collector.py --target tesla.com --all
============================================================
"""

import argparse
import socket
import subprocess
import json
import os
import sys
from datetime import datetime

# ── COLORS ──────────────────────────────────────────────
R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
B  = "\033[94m"
C  = "\033[96m"
W  = "\033[97m"
M  = "\033[95m"
RS = "\033[0m"

# ── OUTPUT STORAGE ───────────────────────────────────────
report_lines = []

# ── HELPERS ─────────────────────────────────────────────
def banner():
    os.system("clear")
    print(f"""{C}
╔══════════════════════════════════════════════════════════╗
║              OSINT COLLECTOR v1.0                       ║
║         CEH Journey — Week 2 | Assessment 2             ║
║         Author: Muhammad Owais Raza                     ║
║         GitHub: github.com/Mianowaisraza               ║
╚══════════════════════════════════════════════════════════╝{RS}
    """)

def divider(title):
    line = f"\n{'─'*55}"
    print(f"{M}{line}{RS}")
    print(f"{W}  {title}{RS}")
    print(f"{M}{'─'*55}{RS}")
    report_lines.append(f"\n{'─'*55}")
    report_lines.append(f"  {title}")
    report_lines.append(f"{'─'*55}")

def log(symbol, color, msg):
    print(f"  {color}[{symbol}]{RS} {msg}")
    report_lines.append(f"  [{symbol}] {msg}")

def found(msg):
    log("+", G, msg)

def notfound(msg):
    log("-", R, msg)

def info(msg):
    log("i", B, msg)

def warn(msg):
    log("!", Y, msg)

def run_cmd(cmd):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True,
            text=True, timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error: {e}"

def tool_exists(tool):
    """Check if a tool is installed."""
    result = subprocess.run(
        f"which {tool}", shell=True,
        capture_output=True, text=True
    )
    return result.returncode == 0

# ── MODULE 1: DNS ENUMERATION ────────────────────────────
def dns_enum(target):
    divider("MODULE 1 — DNS Enumeration")
    info(f"Target domain: {target}")

    # A Record (IP)
    try:
        ip = socket.gethostbyname(target)
        found(f"A Record (IP)     : {ip}")
    except socket.gaierror:
        notfound("Could not resolve A record")
        ip = None

    # All DNS records via dig
    record_types = ["A", "MX", "NS", "TXT", "CNAME"]
    for rtype in record_types:
        output = run_cmd(f"dig +short {rtype} {target}")
        if output and "Error" not in output:
            found(f"{rtype} Record          : {output[:80]}")
        else:
            warn(f"{rtype} Record          : Not found or dig not available")

    return ip

# ── MODULE 2: WHOIS LOOKUP ───────────────────────────────
def whois_lookup(target):
    divider("MODULE 2 — WHOIS Lookup")

    if tool_exists("whois"):
        output = run_cmd(f"whois {target}")
        if output:
            # Extract key fields
            key_fields = [
                "Registrar:",
                "Creation Date:",
                "Registry Expiry Date:",
                "Registrant Organization:",
                "Registrant Country:",
                "Name Server:",
            ]
            info("Extracting key WHOIS fields:")
            for line in output.splitlines():
                for field in key_fields:
                    if field.lower() in line.lower():
                        found(line.strip()[:80])
                        break
        else:
            warn("WHOIS returned no data")
    else:
        warn("whois not installed — run: sudo apt install whois")
        info("Manual alternative: https://who.is")

# ── MODULE 3: IP GEOLOCATION ─────────────────────────────
def ip_geolocation(ip):
    divider("MODULE 3 — IP Geolocation")

    if not ip:
        warn("No IP to geolocate — skipping")
        return

    info(f"Geolocating IP: {ip}")

    # Use curl to hit free IP API
    output = run_cmd(f"curl -s https://ipapi.co/{ip}/json/")

    if output and "Error" not in output:
        try:
            data = json.loads(output)
            fields = {
                "IP"         : data.get("ip", "N/A"),
                "City"       : data.get("city", "N/A"),
                "Region"     : data.get("region", "N/A"),
                "Country"    : data.get("country_name", "N/A"),
                "Latitude"   : data.get("latitude", "N/A"),
                "Longitude"  : data.get("longitude", "N/A"),
                "ISP/Org"    : data.get("org", "N/A"),
                "Timezone"   : data.get("timezone", "N/A"),
            }
            for key, val in fields.items():
                found(f"{key:<15}: {val}")
        except json.JSONDecodeError:
            warn("Could not parse geolocation response")
            info(f"Raw response: {output[:200]}")
    else:
        warn("Geolocation API unavailable — try: https://ipinfo.io")

# ── MODULE 4: TECHNOLOGY DETECTION ───────────────────────
def tech_detection(target):
    divider("MODULE 4 — Technology Detection")

    if tool_exists("whatweb"):
        info(f"Running WhatWeb on {target}...")
        output = run_cmd(f"whatweb -v {target} 2>/dev/null")
        if output:
            for line in output.splitlines()[:20]:
                if line.strip():
                    found(line.strip()[:80])
        else:
            warn("WhatWeb returned no results")
    else:
        warn("whatweb not installed — run: sudo apt install whatweb")
        info("Manual alternative: https://builtwith.com")

    # Try curl headers as fallback
    info("Checking HTTP headers for technology hints...")
    headers = run_cmd(f"curl -sI {target}")
    if headers:
        tech_headers = ["Server:", "X-Powered-By:", "X-Generator:",
                       "Via:", "X-Cache:", "CF-Ray:", "X-Akamai"]
        for line in headers.splitlines():
            for h in tech_headers:
                if h.lower() in line.lower():
                    found(f"Header → {line.strip()[:80]}")

# ── MODULE 5: SUBDOMAIN ENUMERATION ──────────────────────
def subdomain_enum(target):
    divider("MODULE 5 — Subdomain Enumeration")

    subdomains_found = []

    # Method 1: Amass
    if tool_exists("amass"):
        info("Running Amass (this may take a few minutes)...")
        output = run_cmd(f"amass enum -passive -d {target} -timeout 2")
        if output:
            subs = output.splitlines()
            subdomains_found.extend(subs)
            found(f"Amass found {len(subs)} subdomains")
            for sub in subs[:10]:
                info(f"  → {sub}")
            if len(subs) > 10:
                warn(f"  ... and {len(subs)-10} more (saved to report)")
    else:
        warn("Amass not installed — run: sudo apt install amass")

    # Method 2: theHarvester
    if tool_exists("theHarvester"):
        info("Running theHarvester...")
        output = run_cmd(
            f"theHarvester -d {target} -b bing,google -l 50 2>/dev/null"
        )
        if output:
            for line in output.splitlines():
                if target in line and line not in subdomains_found:
                    subdomains_found.append(line.strip())
                    info(f"  → {line.strip()[:60]}")
    else:
        warn("theHarvester not installed")
        info("Install: sudo apt install theharvester")

    # Method 3: Common subdomains wordlist check
    info("Checking common subdomains...")
    common_subs = [
        "www", "mail", "ftp", "api", "dev", "staging",
        "admin", "portal", "shop", "blog", "cdn", "auth",
        "vpn", "remote", "secure", "test", "app", "mobile"
    ]

    for sub in common_subs:
        full = f"{sub}.{target}"
        try:
            ip = socket.gethostbyname(full)
            found(f"LIVE → {full} ({ip})")
            subdomains_found.append(full)
        except socket.gaierror:
            pass

    info(f"Total unique subdomains found: {len(set(subdomains_found))}")
    return list(set(subdomains_found))

# ── MODULE 6: SHODAN SEARCH ───────────────────────────────
def shodan_search(target, ip):
    divider("MODULE 6 — Shodan Intelligence")

    info("Shodan queries to run manually:")
    queries = [
        f'hostname:{target}',
        f'org:"{target.split(".")[0].title()}"',
        f'ssl.cert.subject.cn:{target}',
        f'http.title:"{target.split(".")[0].title()}"',
    ]

    for q in queries:
        found(f'shodan search "{q}"')

    if ip:
        found(f"shodan host {ip}")

    info("Run these at: https://shodan.io")
    info("Or install CLI: pip install shodan && shodan init YOUR_API_KEY")

# ── SAVE REPORT ───────────────────────────────────────────
def save_report(target, output_file):
    divider("SAVING REPORT")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_file or f"osint_{target}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"OSINT REPORT — {target}\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Author: Muhammad Owais Raza\n")
        f.write(f"GitHub: github.com/Mianowaisraza\n")
        f.write("=" * 55 + "\n\n")
        for line in report_lines:
            f.write(line + "\n")

    found(f"Report saved → {filename}")

# ── MAIN ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="OSINT Collector — by Muhammad Owais Raza",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target domain (e.g. tesla.com)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file name (default: osint_[target]_[timestamp].txt)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all modules including slow ones"
    )

    args = parser.parse_args()
    target = args.target.lower().replace("https://", "").replace("http://", "").strip("/")

    banner()
    print(f"{W}  Target   : {C}{target}{RS}")
    print(f"{W}  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RS}")
    print(f"{W}  Output   : {args.output or 'auto-generated'}{RS}\n")

    report_lines.append(f"Target: {target}")
    report_lines.append(f"Started: {datetime.now()}")

    # Run all modules
    ip = dns_enum(target)
    whois_lookup(target)
    ip_geolocation(ip)
    tech_detection(target)

    if args.all:
        subdomain_enum(target)

    shodan_search(target, ip)
    save_report(target, args.output)

    # Final summary
    print(f"\n{C}{'═'*55}{RS}")
    print(f"{G}  ✓ OSINT COLLECTION COMPLETE{RS}")
    print(f"{W}  Target  : {target}{RS}")
    print(f"{W}  IP      : {ip or 'Could not resolve'}{RS}")
    print(f"{B}  GitHub  : github.com/Mianowaisraza{RS}")
    print(f"{C}{'═'*55}{RS}\n")

if __name__ == "__main__":
    main()
