#!/usr/bin/env python3
"""
NetPatch Firewall Groups to Clash Rule Provider Converter

Converts NetPatch Firewall group data (domains and IPs) into Clash Meta
compatible ruleset format with automatic GitHub Actions updates.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Configuration
SOURCE_REPO = "netpatch/groups_for_netpatch_firewall"
BASE_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/master"

# Output directories
OUTPUT_DIR = Path(__file__).parent.parent / "output"
RULESET_DIR = OUTPUT_DIR / "ruleset"
CLASSIC_DIR = OUTPUT_DIR / "classic"

# Source files to convert
DOMAIN_FILES = ["amt.txt", "bdc.txt"]  # Ad/Malware/Tracking, Bypass Domain Categories
COUNTRY_IPS_DIR = "country_ips"


def fetch_url(url: str) -> str:
    """Fetch content from URL with error handling."""
    print(f"  Fetching: {url}")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "netpatch-to-clash/1.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"  ERROR: Failed to fetch {url}: {e}")
        return ""


def parse_domain_list(content: str) -> List[str]:
    """
    Parse domain list from NetPatch format.

    NetPatch format: `.domain.com` (leading dot means domain and subdomains)
    Clash format: `DOMAIN-SUFFIX,domain.com` (no leading dot needed)
    """
    domains = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Remove leading dot if present
        if line.startswith("."):
            line = line[1:]
        if line and "." in line:
            domains.append(line)
    return domains


def parse_ip_list(content: str) -> List[str]:
    """Parse IP CIDR list from NetPatch format."""
    ips = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Validate CIDR format
        if "/" in line:
            ips.append(line)
    return ips


def generate_clash_ruleset(
    name: str,
    domains: List[str] = None,
    ips: List[str] = None,
    payload_type: str = "rules",
) -> Dict:
    """
    Generate Clash ruleset in YAML format.

    Clash ruleset format:
    payload:
      - DOMAIN-SUFFIX,example.com
      - IP-CIDR,192.168.0.0/16
    """
    rules = []

    if domains:
        for domain in domains:
            rules.append(f"DOMAIN-SUFFIX,{domain}")

    if ips:
        for ip in ips:
            rules.append(f"IP-CIDR,{ip}")

    return {"payload": rules}


def generate_classic_text(
    name: str, domains: List[str] = None, ips: List[str] = None
) -> str:
    """Generate classic text format (one rule per line)."""
    lines = []
    lines.append(f"# {name}")
    lines.append(f"# Generated: {datetime.now().isoformat()}")
    lines.append(f"# Source: {SOURCE_REPO}")
    lines.append("")

    if domains:
        lines.append("# Domains")
        for domain in domains:
            lines.append(f"DOMAIN-SUFFIX,{domain}")
        lines.append("")

    if ips:
        lines.append("# IP CIDRs")
        for ip in ips:
            lines.append(f"IP-CIDR,{ip}")

    return "\n".join(lines)


def convert_domain_file(filename: str) -> Tuple[List[str], str]:
    """Download and convert a domain file."""
    url = f"{BASE_URL}/{filename}"
    content = fetch_url(url)
    if not content:
        return [], ""

    domains = parse_domain_list(content)
    return domains, filename.replace(".txt", "")


def convert_country_ips() -> Dict[str, List[str]]:
    """Download and convert all country IP files."""
    # First, get the list of country files
    api_url = f"https://api.github.com/repos/{SOURCE_REPO}/contents/country_ips"

    try:
        req = urllib.request.Request(
            api_url, headers={"User-Agent": "netpatch-to-clash/1.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            files = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR: Failed to list country IPs: {e}")
        return {}

    country_ips = {}
    for file_info in files:
        country_code = file_info["name"].replace(".txt", "")
        url = file_info["download_url"]
        content = fetch_url(url)
        if content:
            ips = parse_ip_list(content)
            if ips:
                country_ips[country_code] = ips

    return country_ips


def write_ruleset(name: str, ruleset: Dict):
    """Write ruleset to YAML file."""
    output_path = RULESET_DIR / f"{name}.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write(f"# Source: {SOURCE_REPO}\n\n")
        f.write("payload:\n")
        for rule in ruleset["payload"]:
            f.write(f"  - {rule}\n")

    print(f"  Written: {output_path}")


def write_classic(name: str, content: str):
    """Write classic text format."""
    output_path = CLASSIC_DIR / f"{name}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Written: {output_path}")


def generate_index(rulesets: List[str], country_codes: List[str]) -> str:
    """Generate README index of available rulesets."""
    lines = [
        "# Available Rulesets",
        "",
        "## Domain Rulesets",
        "",
    ]

    for name in rulesets:
        lines.append(f"- [{name}](ruleset/{name}.yaml)")

    lines.extend(
        [
            "",
            "## Country IP Rulesets",
            "",
        ]
    )

    for code in sorted(country_codes):
        lines.append(f"- [{code}](ruleset/{code}.yaml)")

    return "\n".join(lines)


def main():
    """Main conversion process."""
    print("=" * 60)
    print("NetPatch to Clash Converter")
    print("=" * 60)
    print()

    # Create output directories
    RULESET_DIR.mkdir(parents=True, exist_ok=True)
    CLASSIC_DIR.mkdir(parents=True, exist_ok=True)

    all_rulesets = []
    all_country_codes = []

    # Convert domain files
    print("[1/2] Converting domain lists...")
    for filename in DOMAIN_FILES:
        print(f"\n  Processing: {filename}")
        domains, name = convert_domain_file(filename)
        if domains:
            print(f"    Found {len(domains)} domains")

            # Generate ruleset
            ruleset = generate_clash_ruleset(name, domains=domains)
            write_ruleset(name, ruleset)
            all_rulesets.append(name)

            # Generate classic format
            classic = generate_classic_text(name, domains=domains)
            write_classic(name, classic)

    # Convert country IPs
    print("\n[2/2] Converting country IP lists...")
    country_ips = convert_country_ips()

    for country_code, ips in sorted(country_ips.items()):
        print(f"\n  Processing: {country_code}")
        print(f"    Found {len(ips)} IP CIDRs")

        # Generate ruleset
        ruleset = generate_clash_ruleset(country_code, ips=ips)
        write_ruleset(country_code, ruleset)
        all_country_codes.append(country_code)

        # Generate classic format
        classic = generate_classic_text(country_code, ips=ips)
        write_classic(country_code, classic)

    # Generate index
    print("\n[3/3] Generating index...")
    index = generate_index(all_rulesets, all_country_codes)
    with open(OUTPUT_DIR / "INDEX.md", "w", encoding="utf-8") as f:
        f.write(index)
    print(f"  Written: {OUTPUT_DIR / 'INDEX.md'}")

    # Summary
    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print("=" * 60)
    print(f"  Domain rulesets: {len(all_rulesets)}")
    print(f"  Country IP rulesets: {len(all_country_codes)}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print()


if __name__ == "__main__":
    main()
