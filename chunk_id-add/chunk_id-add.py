import json

# Load your existing JSON file
with open("/Users/yamrajkhadka/nepal-legal-rag/source-change/pdf-to-text_extraction.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Add meaningful chunk_id safely
for item in data:
    # Use .get() with defaults to avoid KeyError
    part_num = item.get("part", "0").replace("Part-", "").strip()
    chapter_num = item.get("chapter", "0").replace("Chapter-", "").strip()
    section_num = str(item.get("section", 0))
    
    # Handle subsection being None or missing
    sub_num = item.get("subsection")
    if sub_num:
        sub_num = sub_num.strip("()")
    else:
        sub_num = "0"
    
    # Create chunk_id
    item["chunk_id"] = f"npc2017_p{part_num}_c{chapter_num}_s{section_num}_sub{sub_num}"

# Save the updated JSON
with open("/Users/yamrajkhadka/nepal-legal-rag/source-change/jaibaba.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Meaningful chunk_ids added successfully!")
