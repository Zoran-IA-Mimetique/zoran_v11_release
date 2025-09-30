#!/usr/bin/env python3
# one_shot_validator.py
import sys, re, json, os

def load_text(path):
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    else:
        return sys.stdin.read()

def check_sections(text, required):
    found = {}
    for s in required:
        pattern = r"(?m)^\s*#*\s*"+re.escape(s)+r"\b"
        found[s] = bool(re.search(pattern, text, flags=re.IGNORECASE))
    return found

def check_valid_block(text):
    m = re.search(r"VALIDATION_CHECK.*Dossier\s*:\s*one_shot_exhaustif\s*—\s*FIN", text, flags=re.IGNORECASE|re.DOTALL)
    return bool(m)

def word_count(text):
    return len(re.findall(r"\w+", text))

def main():
    path = sys.argv[1] if len(sys.argv)>1 else None
    text = load_text(path) if path else sys.stdin.read()
    required_sections = ["Abstract","Introduction","Methods","Results","Discussion","Conclusion"]
    sec = check_sections(text, required_sections)
    wc = word_count(text)
    block_ok = check_valid_block(text)
    fin_ok = "Dossier: one_shot_exhaustif — FIN" in text
    passed = all(sec.values()) and (wc >= 900) and block_ok and fin_ok
    result = {
        "passed": passed,
        "word_count": wc,
        "sections_found": sec,
        "valid_block": block_ok,
        "fin_present": fin_ok
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
