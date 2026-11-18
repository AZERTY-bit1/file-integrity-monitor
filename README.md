# 🛡️ File Integrity Monitor

![tests](https://github.com/AZERTY-bit1/file-integrity-monitor/actions/workflows/tests.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

A simple **FIM** (like a mini Tripwire/AIDE): it takes a SHA-256 fingerprint of every file in a folder, then tells you what was **added, modified or deleted**.

## ✨ Features

- SHA-256 baseline of a whole folder
- `check` mode: one-time comparison (exit code 1 if changes)
- `watch` mode: live alerts every N seconds
- Pure Python, no dependencies

## 🚀 Usage

No installation needed - only Python 3.8+.

```bash
git clone https://github.com/AZERTY-bit1/file-integrity-monitor.git
cd file-integrity-monitor
python fim.py init  ./my_folder -b baseline.json
python fim.py check ./my_folder -b baseline.json
python fim.py watch ./my_folder -b baseline.json -i 5
```

## 📸 Example output

```
[+] ADDED    new_script.sh
[~] MODIFIED config.ini
[-] DELETED  notes.txt
[!] 3 change(s) detected.
```

## 🧪 Tests

```bash
python -m unittest discover -s tests -v
```

## ⚠️ Disclaimer

This is a **defensive / educational** tool. Only use it on systems and data you own or are allowed to check.

## 📄 License

MIT - see [LICENSE](LICENSE).
