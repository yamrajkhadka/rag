from enum import STRICT
import fitz
import re
import json

PDF_PATH = "penal-english.pdf"
OUTPUT = "naya_nepal_penal_code_clean.json"

LAW = "National Penal Code 2017"

doc = fitz.open(PDF_PATH)

# Extract + pre-clean text
raw = []
for page in doc:
    t = page.get_text()
    t = re.sub(r'(\w)-\n(\w)', r'\1\2', t)   # fix hyphens
    t = re.sub(r'\n+', '\n', t)
    raw.append(t)

lines = [l.strip() for l in "\n".join(raw).split("\n")]

# remove pure page numbers
lines = [l for l in lines if not re.fullmatch(r'\d+', l)]

#2.Regrex(STRICT ORDER)
part_re = re.compile(r'^Part\s*[-–]?\s*(\d+)\s*(.*)', re.I)
chapter_re = re.compile(r'^Chapter\s*[-–]?\s*(\d+)', re.I)
section_re = re.compile(r'^(\d+)\.\s*(.+)')
subsection_re = re.compile(r'^\((\d+)\)')
clause_re = re.compile(r'^\(([a-z])\)')

#3.State
records = []

part = chapter = chapter_title = None
section = section_title = None
subsection = None
buffer = ""

def flush():
    global buffer
    if section and buffer.strip():
        records.append({
            "law": LAW,
            "part": part,
            "chapter": chapter,
            "chapter_title": chapter_title,
            "section": section,
            "section_title": section_title,
            "subsection": subsection,
            "text": buffer.strip(),
            "source": "penal-english.pdf"  #here replacewith ----"source": "National Penal (Code) Act, 2017 (English translation) — https://bwcimplementation.org/sites/default/files/resource/NP_National%20Penal%20Code%20Act_EN.pdf"

  
        })
    buffer = ""

i = 0
while i < len(lines):
    line = lines[i]
    i += 1
    if not line:
        continue

    # PART
    m = part_re.match(line)
    if m:
        flush()
        part = f"Part-{m.group(1)}"
        section = subsection = None
        continue

    # CHAPTER
    m = chapter_re.match(line)
    if m:
        flush()
        chapter = f"Chapter-{m.group(1)}"
        section = subsection = None

        # next non-empty = chapter title
        while i < len(lines) and not lines[i]:
            i += 1
        chapter_title = lines[i] if i < len(lines) else None
        i += 1
        continue

    # SECTION (HARD BOUNDARY)
    m = section_re.match(line)
    if m:
        flush()
        section = int(m.group(1))
        section_title = m.group(2).rstrip(":")
        subsection = None
        continue

    # SUBSECTION
    m = subsection_re.match(line)
    if m:
        flush()
        subsection = f"({m.group(1)})"
        continue

    # CLAUSE → keep inside subsection
    if clause_re.match(line):
        buffer += " " + line
        continue

    # CONTENT
    buffer += " " + line

flush()

#4. Output
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Clean legal dataset generated: {len(records)} records")
