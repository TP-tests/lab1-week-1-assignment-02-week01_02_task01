#!/usr/bin/env python3
import sys
import re
from pathlib import Path

ASSIGNMENT_FILE = Path("01_hardware_vs_software.md")

# Expected headings (exact match)
H1 = r"# Part 1 – Hardware vs Software"
H2_SECTIONS = [
    r"## Explain Hardware",
    r"## Explain Software",
    r"## How Do Hardware and Software Interact\?",
]

MIN_WORDS = 50

def fail(msg):
    print(f"::error::{msg}")
    print("RESULT: FAIL")
    sys.exit(1)

def pass_msg(msg):
    print(msg)

def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"File not found: {path}")

def count_words(text: str) -> int:
    # Basic word tokenizer: sequences of letters/digits/apostrophes/hyphens
    tokens = re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text)
    return len(tokens)

def extract_section_body(md: str, section_heading: str, next_headings: list) -> str:
    # Match the section heading line
    pattern = rf"(?m)^{section_heading}\s*\n(.+?)(?=^\#\# |\Z)"
    m = re.search(pattern, md, flags=re.DOTALL)
    if not m:
        return None
    body = m.group(1).strip()
    # Remove horizontal rules or markdown separators if any
    body = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", "", body).strip()
    return body

def main():
    md = load_file(ASSIGNMENT_FILE)

    # 1) Check H1 exists
    if not re.search(rf"(?m)^{H1}\s*$", md):
        fail("Missing exact H1 heading: '# Part 1 – Hardware vs Software'")

    # 2) Check each H2 exists and has >= MIN_WORDS body
    total_ok = True
    for h2 in H2_SECTIONS:
        if not re.search(rf"(?m)^{h2}\s*$", md):
            fail(f"Missing exact section heading: '{re.sub(r'\\', '', h2)}'")

        body = extract_section_body(md, h2, H2_SECTIONS)
        if body is None:
            fail(f"Could not extract content under section: '{re.sub(r'\\', '', h2)}'")

        words = count_words(body)
        if words < MIN_WORDS:
            fail(
                f"Section '{re.sub(r'\\', '', h2)}' has {words} words; "
                f"minimum required is {MIN_WORDS}."
            )
        else:
            pass_msg(
                f"Section '{re.sub(r'\\', '', h2)}' OK: {words} words (≥ {MIN_WORDS})."
            )

    print("All checks passed.")
    print("RESULT: PASS")

if __name__ == "__main__":
    main()