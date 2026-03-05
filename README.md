# MetaShield

MetaShield detects, extracts, and strips sensitive EXIF metadata from images to prevent OSINT tracking.

## Features
* **Auto-Scanning:** Automatically processes all images placed in `data/raw/`.
* **GPS Decoding:** Decodes raw binary GPS tags into clickable Google Maps links.
* **Device Identification:** Reveals Camera Make, Model, and Software versions.
* **Batch Sanitization:** Strips all metadata and saves clean copies to `data/processed/`.

## Project Structure
```text
meta-shield/
├── main.py                # Scanner & sanitizer
├── data/
│   ├── raw/               # Place images to analyze here
│   └── processed/         # Cleaned images are saved here
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## Quick Start

1. Setup 

```bash
pip3 install -r requirements.txt
```

2. Usage

* Place your images in `data/raw/`

* Run the scanner:
```bash
python3 main.py 
```

* View extracted data in the console and find cleaned images in `data/processed/`

3. Sample Output

```text
--- Processing: area51.jpg ---
    > Make: Apple
    > Model: iPhone 15 Pro
    > Software: iOS 17.4.1
    [!] GPS DETECTED: 37.2431, -115.793
    [!] Map: https://www.google.com/maps?q=37.2431,-115.793
    [V] SANITIZED: Saved to data/processed/cleaned_area51.jpg
```
