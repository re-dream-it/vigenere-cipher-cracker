# 🔐 Vigenère Cipher Cracker

A Python tool for cracking Vigenère cipher using frequency analysis and IC comparasion method.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-8A2BE2)

## ✨ Features
- **Automatic key length detection** using index of coincidence
- **Interactive cracking mode** with manual shift selection
- **Multi-language support** (Russian/English)
- **File input/output** support
- **Frequency analysis** visualization

## ᯓ★ Quick Start
```bash
# Run with interactive mode
❯ python vigenere_cracker.py encrypted.txt

# Decrypt with known key
❯ python vigenere_cracker.py encrypted.txt -k "secret"

# Semi-automatic mode with suggested shifts
❯ python vigenere_cracker.py encrypted.txt -s 5 12 8 3
```

## 🔧 How It Works
### 1. Frequency Analysis. 
Compares letter frequencies with language reference tables
### 2. Interactive Mode. Guides user through decryption with suggestions:
```
=== Part 3/5 ===
Top letters:
1. ш (24x) -> shift 5 (key 'е')
2. щ (18x) -> shift 6 (key 'ж')
3. ч (15x) -> shift 3 (key 'г')

Choose option (1-3) or enter custom shift:
```

## 📋 Usage Examples
### Basic Decryption
```bash
# Run interactive mode with saving results to .txt file
❯ python vigenere_cracker.py message.txt -o decrypted.txt
```

### Key Recovery
```bash
# Get estimated key length
❯ python vigenere_cracker.py ciphertext.txt --analyze

# Test specific key
❯ python vigenere_cracker.py ciphertext.txt -k "password"
```

### Help menu for other options
```bash
❯ python3 vigener_crack.py -h
usage: vigener_crack.py [-h] [-s SHIFTS [SHIFTS ...]] [-k KEY] [-o OUTPUT] file

Crack Vigenère cipher

positional arguments:
  file                  Input file with ciphertext

options:
  -h, --help            show this help message and exit
  -s SHIFTS [SHIFTS ...], --shifts SHIFTS [SHIFTS ...]
                        Manual shifts for each key letter
  -k KEY, --key KEY     Known key for direct decryption
  -o OUTPUT, --output OUTPUT
                        Output file for decrypted text
```

## 🧠 Theory
The tool uses:

- Index of Coincidence (IC) for key length detection
- Frequency distributions of Russian letters
