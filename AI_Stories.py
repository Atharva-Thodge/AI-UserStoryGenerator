#!/usr/bin/env python3
# ai_user_story.py - call a local Ollama model and print a user story

import requests, re, sys

MODEL = "mistral:7b-instruct"

TEMPLATE = """Turn the sentence into a product user story with acceptance criteria.
Return plain text in this exact skeleton:

Title: <short title>
User story:
As a <persona>, I want <capability> so that <value>.

Acceptance criteria:
- <AC 1>
- <AC 2>
- <AC 3>

Sentence: "{line}"
"""

def ask_ollama(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}},
        timeout=180,
    )
    r.raise_for_status()
    return r.json().get("response", "").strip()

def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p for p in parts if p]

if __name__ == "__main__":
    print("Paste a sentence or short paragraph, then press Enter:")
    user_text = sys.stdin.readline().strip()
    if not user_text:
        sys.exit(0)

    lines = split_sentences(user_text)
    print("\n====== USER STORIES ======\n")
    for i, line in enumerate(lines, 1):
        prompt = TEMPLATE.format(line=line)
        print(f"[{i}] From: {line}\n")
        print(ask_ollama(prompt))
        print()
    print("==========================\n")