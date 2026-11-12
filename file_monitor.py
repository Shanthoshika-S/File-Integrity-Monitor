import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


MONITORED_FOLDER = Path("monitored_files")
BASELINE_FILE = Path("baseline.json")
REPORT_FOLDER = Path("reports")


def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with Path(file_path).open("rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except OSError as error:
        print(f"[ERROR] Unable to read file: {error}")
        return None


def create_baseline():
    """Save the current hashes as the original baseline."""

    baseline = {}

    for file_path in MONITORED_FOLDER.iterdir():
        if file_path.is_file():
            file_hash = calculate_file_hash(file_path)

            if file_hash:
                baseline[file_path.name] = file_hash

    with BASELINE_FILE.open("w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)

    if not MONITORED_FOLDER.exists() or not MONITORED_FOLDER.is_dir():
        print(f"[ERROR] Monitored folder not found: {MONITORED_FOLDER}")
        return

    print("\n[SUCCESS] Baseline created successfully!")
    print(f"Files recorded: {len(baseline)}")


def check_integrity():
    """Compare current files against the saved baseline."""

    if not MONITORED_FOLDER.exists() or not MONITORED_FOLDER.is_dir():
        print(f"[ERROR] Monitored folder not found: {MONITORED_FOLDER}")
        return

    if not BASELINE_FILE.exists():
        print("[ERROR] Baseline not found. Create a baseline first.")
        return

    try:
        with BASELINE_FILE.open("r", encoding="utf-8") as file:
            baseline = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"[ERROR] Unable to read baseline: {error}")
        return

    if not isinstance(baseline, dict):
        print("[ERROR] Invalid baseline format. Expected a JSON object.")
        return

    current_files = {}

    try:
        for file_path in MONITORED_FOLDER.iterdir():
            if file_path.is_file():
                file_hash = calculate_file_hash(file_path)

                if file_hash:
                    current_files[file_path.name] = file_hash

    except OSError as error:
        print(f"[ERROR] Unable to scan monitored folder: {error}")
        return

    changes = []

    for filename, original_hash in baseline.items():
        if filename not in current_files:
            changes.append(f"[DELETED] {filename}")

        elif current_files[filename] != original_hash:
            changes.append(f"[MODIFIED] {filename}")

    for filename in current_files:
        if filename not in baseline:
            changes.append(f"[NEW] {filename}")

    print("\n===== INTEGRITY CHECK RESULTS =====")

    if changes:
        for change in changes:
            print(change)
    else:
        print("[SAFE] No file changes detected.")

    generate_report(changes, len(current_files))


def generate_report(changes, files_checked):
    """Generate a Markdown report of the integrity check."""

    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if changes:
        status = "CHANGES DETECTED"
    else:
        status = "NO CHANGES DETECTED"

    report_content = f"""# File Integrity Monitoring Report

- **Date:** {timestamp}
- **Status:** {status}
- **Files checked:** {files_checked}
- **Changes detected:** {len(changes)}

## Detected Events

"""

    if changes:
        for change in changes:
            report_content += f"- {change}\n"
    else:
        report_content += "- No unexpected changes detected.\n"

    report_file = REPORT_FOLDER / "integrity_report.md"

    report_file.write_text(report_content, encoding="utf-8")

    print(f"\n[REPORT] Report saved to: {report_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Python File Integrity Monitoring System"
    )

    commands = parser.add_mutually_exclusive_group(required=True)

    commands.add_argument(
        "--create-baseline",
        action="store_true",
        help="Create a new baseline of monitored files"
    )

    commands.add_argument(
        "--check",
        action="store_true",
        help="Check monitored files against the saved baseline"
    )

    args = parser.parse_args()

    print("===== FILE INTEGRITY MONITOR =====")

    if args.create_baseline:
        create_baseline()

    elif args.check:
        check_integrity()


if __name__ == "__main__":
    main()
