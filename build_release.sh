#!/usr/bin/env bash
set -euo pipefail

pyinstaller --onefile i3sm.py

zip -j dist/i3sm.zip dist/i3sm README.md LICENSE NOTICES