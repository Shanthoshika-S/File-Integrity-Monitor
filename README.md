# File Integrity Monitoring System (Python)

A beginner-friendly cybersecurity project that monitors files for unauthorized changes using SHA-256 cryptographic hashing.

## Overview

The File Integrity Monitoring (FIM) System is a Python-based security tool that establishes a baseline of monitored files and checks their integrity against that baseline.

It identifies:
- Modified files
- Deleted files
- Newly created files

The tool also generates a Markdown security report after each integrity check.

## Features

- SHA-256 file hashing using Python's `hashlib`
- JSON-based integrity baseline
- Detection of modified, deleted, and newly created files
- Automated Markdown security reports
- Command-line interface using `argparse`
- Input validation and error handling
- Automated unit tests using `unittest`

## Technologies

- Python 3
- hashlib
- pathlib
- JSON
- argparse
- unittest

No external Python packages are required.

## Project Structure

```text
File-Integrity-Monitor/
├── monitored_files/
│   ├── config.txt
│   ├── security.txt
│   └── users.txt
├── reports/
│   └── integrity_report.md
├── src/
│   └── file_monitor.py
├── tests/
│   └── test_file_monitor.py
├── baseline.json
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```

Python 3 is required.

## Usage

### 1. Create an integrity baseline

```bash
python3 src/file_monitor.py --create-baseline
```

This calculates SHA-256 hashes for the monitored files and saves them in `baseline.json`.

### 2. Check file integrity

```bash
python3 src/file_monitor.py --check
```

The tool compares the current hashes against the saved baseline.

### 3. View the generated report

```bash
cat reports/integrity_report.md
```

### 4. Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

## Example Detection Output

```text
===== INTEGRITY CHECK RESULTS =====

[MODIFIED] config.txt
[DELETED] users.txt
[NEW] backup.txt
```

## Security Considerations and Limitations

- SHA-256 detects content changes but does not identify who made them.
- The baseline must be protected from unauthorized modification.
- An attacker who can modify both monitored files and the baseline may be able to hide changes.
- The current version monitors files directly inside the configured folder, not nested subdirectories.
- This project is a learning and demonstration tool, not a replacement for an enterprise-grade FIM solution.

## Future Improvements

- Recursive directory monitoring
- Timestamped historical reports
- Email alerts for detected changes
- File permission monitoring
- Protected or remotely stored baselines
- HMAC-based baseline authentication

## Learning Outcomes

Through this project, I practised:

- Cryptographic hashing with SHA-256
- File handling and directory operations in Python
- Baseline-based integrity verification
- Security event detection
- JSON data storage
- Command-line application development
- Automated testing and error handling

## Disclaimer

This project is intended for educational and authorized defensive security monitoring.
