"""
audio_file_organizer.py
Helper script for organizing and validating audio annotation deliverables
(e.g. TELUS-style freetalk segment naming and CSV generation).
"""

import os
import re
import csv

# Expected filename pattern: YYMMDD_freetalk_secN_NNN_Speaker.wav
FILENAME_PATTERN = re.compile(
    r"^(\d{6})_freetalk_sec(\d+)_(\d{3})_(Tim|Lily)\.wav$"
)


def validate_filenames(folder_path):
    """Check all .wav files in a folder against the required naming convention."""
    valid_files = []
    invalid_files = []

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(".wav"):
            if FILENAME_PATTERN.match(filename):
                valid_files.append(filename)
            else:
                invalid_files.append(filename)

    print(f"Valid files: {len(valid_files)}")
    print(f"Invalid files: {len(invalid_files)}")
    if invalid_files:
        print("\nFiles that don't match the naming convention:")
        for f in invalid_files:
            print(f"  - {f}")

    return valid_files, invalid_files


def generate_csv_template(folder_path, output_csv):
    """Generate a CSV template (filename, start, end) for valid files, sorted naturally."""
    valid_files, _ = validate_filenames(folder_path)

    # Sort by section number, then sentence number, to match ABAB order
    def sort_key(fname):
        match = FILENAME_PATTERN.match(fname)
        date, sec, num, speaker = match.groups()
        return (int(sec), int(num))

    valid_files.sort(key=sort_key)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for filename in valid_files:
            # Placeholder times - fill these in manually or extend script to read audio length
            writer.writerow([filename, "0:00.000", "0:00.000"])

    print(f"\nCSV template created: {output_csv}")


if __name__ == "__main__":
    folder = input("Enter path to audio folder: ").strip()
    output_file = input("Enter output CSV filename (e.g. output.csv): ").strip()

    if os.path.isdir(folder):
        generate_csv_template(folder, output_file)
    else:
        print("Folder not found. Please check the path and try again.")
