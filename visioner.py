"""
Vigenère Cipher Cracker

This script implements a method to crack the Vigenère cipher using frequency analysis
and the Kasiski examination technique.
"""

from collections import defaultdict
import argparse
from pathlib import Path

# Russian alphabet
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALPHABET_LENGTH = len(ALPHABET)


def read_file(filename: str) -> str:
    """Read text from file with automatic encoding detection."""
    try:
        return Path(filename).read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return Path(filename).read_text(encoding='cp1251')
        except Exception as e:
            raise ValueError(f"Cannot read file {filename}: {str(e)}")

def clean_text(text: str) -> str:
    """Remove all non-alphabetic characters from the text."""
    return ''.join(c for c in text.lower() if c in ALPHABET)


def count_letter_frequencies(text: str) -> list[tuple[str, int]]:
    """Count frequency of each letter in text, return sorted list."""
    counts = defaultdict(int)
    for c in text:
        counts[c] += 1
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)


def calculate_index_of_coincidence(text: str) -> float:
    """Calculate the index of coincidence for the given text."""
    freq = count_letter_frequencies(text)
    L = len(text)
    if L < 2:
        return 0.0
    return sum(n * (n - 1) for _, n in freq) / (L * (L - 1))


def guess_key_length(ciphertext: str, max_len=15, lang='ru') -> int:
    """
    Estimates key length by IC
    """
    expected_ic = 0.056
    
    best_len = 1
    closest_ic_diff = float('inf')
    
    for possible_len in range(1, max_len + 1):
        parts = [ciphertext[i::possible_len] for i in range(possible_len)]
        avg_ic = sum(calculate_index_of_coincidence(part) for part in parts) / possible_len
        current_diff = abs(avg_ic - expected_ic)
        if current_diff < closest_ic_diff:
            closest_ic_diff = current_diff
            best_len = possible_len
    
    print(f"\nBest estimated key length: {best_len} (IC diff {closest_ic_diff:.4f})")
    return best_len


def shift_char(c: str, shift: int) -> str:
    """Shift a character by given amount in the alphabet."""
    idx = (ALPHABET.index(c) - shift) % ALPHABET_LENGTH
    return ALPHABET[idx]


def shift_text(text: str, shift: int) -> str:
    """Shift all characters in text by given amount."""
    return ''.join(shift_char(c, shift) for c in text)


def find_shift(part: str) -> int:
    """
    Find the most probable shift for a part of ciphertext.
    Assumes the most frequent letter should be 'о' (most frequent in Russian).
    """
    freq = count_letter_frequencies(part)
    top_letters = ''
    for i in freq[:5]:
        shift = str((ALPHABET.index(i[0][0]) - ALPHABET.index('о')) % ALPHABET_LENGTH)
        top_letters += f"{i[0]} [{shift}]: {i[1]} times | "
    print(top_letters)

    if not freq:
        return 0
    most_frequent = freq[0][0]
    return (ALPHABET.index(most_frequent) - ALPHABET.index('о')) % ALPHABET_LENGTH

def interactive_crack(ciphertext: str):
    """
    Interactive cracking mode where user can select shifts for each part.
    """
    ciphertext = clean_text(ciphertext)
    key_length = guess_key_length(ciphertext)
    print(f"\nEstimated key length: {key_length}")
    
    parts = [ciphertext[i::key_length] for i in range(key_length)]
    key_shifts = []
    
    for i, part in enumerate(parts):
        print(f"\n=== Part {i+1} ===")
        print(f"Length: {len(part)} chars")
        
        freq = count_letter_frequencies(part)[:5]
        print("\nTop letters and possible shifts:")
        i = 0
        for letter, count in freq:
            shift = (ALPHABET.index(letter) - ALPHABET.index('о')) % ALPHABET_LENGTH
            key_char = ALPHABET[shift]
            print(f"{i}. {letter} ({count}x) -> shift {shift} (key '{key_char}')")
            i+=1
        
        ic = calculate_index_of_coincidence(part)
        print(f"\nIndex of coincidence: {ic:.4f} (expected ~0.056)")
        
        while True:
            try:
                shift = int(input("Enter chosen shift: "))
                if 0 <= shift < ALPHABET_LENGTH:
                    break
                print(f"Shift must be between 0 and {ALPHABET_LENGTH-1}")
            except ValueError:
                print("Please enter a valid number")
        
        key_shifts.append(shift)
    
    key = ''.join(ALPHABET[shift] for shift in key_shifts)
    plaintext = decrypt_vigenere(ciphertext, key)
    
    print("\n=== Results ===")
    print(f"Key: {key}")
    print("\nDecrypted text (first 200 chars):")
    print(plaintext[:200] + "...")
    
    return plaintext, key


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using known key."""
    cleaned = clean_text(ciphertext)
    key_shifts = [ALPHABET.index(c) for c in key.lower() if c in ALPHABET]
    if not key_shifts:
        return ciphertext
    
    key_length = len(key_shifts)
    parts = [cleaned[i::key_length] for i in range(key_length)]
    
    plaintext_parts = [
        shift_text(part, shift)
        for part, shift in zip(parts, key_shifts)
    ]
    
    return ''.join(
        plaintext_parts[i % key_length][i // key_length]
        for i in range(len(cleaned)))

def crack_vigenere(ciphertext: str, shifts: list) -> tuple[str, str]:
    """
    Crack Vigenère cipher and return (plaintext, key).
    
    Steps:
    1. Clean the ciphertext
    2. Guess the key length
    3. Split text into key-length parts
    4. Find shift for each part
    5. Combine shifts to get key
    6. Decrypt the ciphertext
    """
    print('------- ANALYZING -------')

    ciphertext = clean_text(ciphertext)
    key_length = guess_key_length(ciphertext)
    print(f"Key length: {key_length}")
    
    parts = [ciphertext[i::key_length] for i in range(key_length)]
    
    print('Top of letters for each part:')
    likely_shifts = [find_shift(part) for part in parts]
    print(f"Most likely shifts: {likely_shifts}")


    print('\n------- SOLVING -------')

    print(f"Using shifts: {shifts}")
    key = ''.join(ALPHABET[shift] for shift in shifts)
    
    plaintext_parts = [
        shift_text(part, shift) 
        for part, shift in zip(parts, shifts)
    ]
    plaintext = ''.join(
        plaintext_parts[i % key_length][i // key_length] 
        for i in range(len(ciphertext)))
    
    return plaintext, key

def main():
    parser = argparse.ArgumentParser(description='Crack Vigenère cipher')
    parser.add_argument('file', help='Input file with ciphertext')
    parser.add_argument('-s', '--shifts', nargs='+', type=int,
                      help='Manual shifts for each key letter')
    parser.add_argument('-k', '--key', help='Known key for direct decryption')
    parser.add_argument('-o', '--output', help='Output file for decrypted text')
    
    args = parser.parse_args()

    # Reading text
    try:
        ciphertext = read_file(args.file)
        print(f"Read {len(ciphertext)} characters from {args.file}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Choosing mode
    if args.key:
        # Direct decrypt using key
        plaintext = decrypt_vigenere(ciphertext, args.key)
        print(f"\nUsing provided key: {args.key}")
    elif args.shifts:
        # Semi-auto mode with passing shifts
        plaintext, key = crack_vigenere(ciphertext, args.shifts)
        print(f"\nUsed key: {key}")
    else:
        # Interactive mode
        print("Starting interactive cracking mode...")
        plaintext, key = interactive_crack(ciphertext)
        print(f"\nFinal key: {key}")

    # Printing results
    print("\nDecrypted text preview:")
    print(plaintext[:200] + "...")

    # Saving to file
    if args.output:
        try:
            Path(args.output).write_text(plaintext, encoding='utf-8')
            print(f"\nFull decrypted text saved to {args.output}")
        except Exception as e:
            print(f"Error saving output file: {e}")

if __name__ == "__main__":
    main()