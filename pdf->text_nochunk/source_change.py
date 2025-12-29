import json

# Load your existing JSON file
with open("naya_nepal_penal_code_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# New standardized source
new_source = "National Penal (Code) Act, 2017 (English translation) — https://bwcimplementation.org/sites/default/files/resource/NP_National%20Penal%20Code%20Act_EN.pdf"

# Replace the source in every entry
for entry in data:
    entry["source"] = new_source

# Save the updated JSON
with open("your_file_updated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("All sources updated successfully!")
