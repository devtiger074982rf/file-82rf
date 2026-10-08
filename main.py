"""Utility to detect duplicate files in a directory tree."""
import os
import hashlib
import argparse

def file_hash(path, block=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b''):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(root):
    hashes = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            fp = os.path.join(dirpath, name)
            try:
                key = file_hash(fp)
            except (OSError, PermissionError):
                continue
            hashes.setdefault(key, []).append(fp)
    return [v for v in hashes.values() if len(v) > 1]

def main():
    parser = argparse.ArgumentParser(description="Find duplicate files.")
    parser.add_argument("path", help="Directory to scan")
    args = parser.parse_args()
    duplicates = find_duplicates(args.path)
    if not duplicates:
        print("No duplicates found.")
        return
    print("Duplicate groups:")
    for group in duplicates:
        print("\n".join(group))
        print("-" * 40)

if __name__ == "__main__":
    main()