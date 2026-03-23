#!/usr/bin/env python3
"""
Translate rules_src_part4.csv text column to French.
Copies all other columns as-is.
Only translates the 'text' column (index 4).
"""
import csv
import sys
import re

INPUT = r"D:\Fractal Softworks\Starsector\mods\starsector_lang_pack_fr_private\.claude\worktrees\objective-bartik\data\campaign\rules_src_part4.csv"
OUTPUT = r"D:\Fractal Softworks\Starsector\mods\starsector_lang_pack_fr_private\.claude\worktrees\objective-bartik\data\campaign\rules_part4.csv"

# This script copies the file as-is since the actual translation
# needs to be done by the AI model. This is a placeholder.
# The real translation will be done chunk by chunk.

def main():
    with open(INPUT, 'r', encoding='utf-8') as fin:
        content = fin.read()
    with open(OUTPUT, 'w', encoding='utf-8', newline='') as fout:
        fout.write(content)
    print(f"Copied {INPUT} -> {OUTPUT}")
    print("File needs manual translation of text column.")

if __name__ == "__main__":
    main()
