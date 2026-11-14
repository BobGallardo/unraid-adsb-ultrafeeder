#!/usr/bin/env python3
"""Validate the Unraid Community Apps ADS-B Ultrafeeder template.

Only standard-library XML and basic template checks; no hardware is touched.
Use --publish to reject placeholder publisher URLs before Community Apps submission.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "adsb-ultrafeeder.xml"
PROFILE = ROOT / "ca_profile.xml"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="reject placeholder publisher metadata")
    args = parser.parse_args()
    errors: list[str] = []

    try:
        root = ET.parse(TEMPLATE).getroot()
        profile = ET.parse(PROFILE).getroot()
    except (ET.ParseError, OSError) as exc:
        print(f"XML parse error: {exc}", file=sys.stderr)
        return 1

    if root.tag != "Container" or root.attrib.get("version") != "2":
        errors.append("Template must have <Container version='2'> root")
    if profile.tag != "CommunityApplications":
        errors.append("ca_profile.xml must have CommunityApplications root")
    if not (profile.findtext("Profile") or "").strip():
        errors.append("ca_profile.xml must have non-empty <Profile>")

    expected = {
        "Name", "Repository", "Overview", "Category", "Project", "Support",
        "WebUI", "TemplateURL", "Icon",
    }
    for name in sorted(expected):
        if not (root.findtext(name) or "").strip():
            errors.append(f"Missing or empty <{name}>")

    if (root.findtext("Repository") or "") != "ghcr.io/sdr-enthusiasts/docker-adsb-ultrafeeder:latest":
        errors.append("Unexpected Docker image repository")
    if (root.findtext("Network") or "") != "bridge":
        errors.append("Default network must be bridge so the container shares the Unraid server IP")
    if (root.findtext("Privileged") or "").lower() != "false":
        errors.append("Container must not require privileged mode")

    configs = root.findall("Config")
    targets = [x.attrib.get("Target", "") for x in configs]
    for name in ("READSB_LAT", "READSB_LON", "READSB_ALT", "TZ", "READSB_DEVICE_TYPE"):
        if name not in targets:
            errors.append(f"Missing mandatory environment setting: {name}")
    if len(targets) != len(set(targets)):
        errors.append("Duplicate Config Target entries")
    if not any(
        c.attrib.get("Target") == "80"
        and c.attrib.get("Type") == "Port"
        and c.attrib.get("Default") == "8080"
        and (c.text or "").strip() == "8080"
        for c in configs
    ):
        errors.append("Container web port 80 must default to host port 8080")
    if (root.findtext("WebUI") or "") != "http://[IP]:[PORT:80]/":
        errors.append("WebUI must reference container port 80 so Unraid resolves the selected network port")
    if "--device-cgroup-rule=" not in (root.findtext("ExtraParams") or ""):
        errors.append("Missing USB device cgroup permission")
    if not any(c.attrib.get("Target") == "/dev/bus/usb" and c.attrib.get("Type") == "Path" for c in configs):
        errors.append("Missing USB bus bind mount")
    if any(c.attrib.get("Target") == "ULTRAFEEDER_CONFIG" and (c.text or "").strip() for c in configs):
        errors.append("Default ULTRAFEEDER_CONFIG must not enable external feeds")

    if args.publish:
        for path in (TEMPLATE, PROFILE):
            if "YOUR_GITHUB_USERNAME" in path.read_text(encoding="utf-8"):
                errors.append(f"Replace GitHub placeholders in {path.relative_to(ROOT)}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1
    print(f"PASS: {TEMPLATE.relative_to(ROOT)} parsed and validated ({len(configs)} settings)")
    if not args.publish:
        print("NOTE: Run with --publish after setting GitHub ownership and support URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
