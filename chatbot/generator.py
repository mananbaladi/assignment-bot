import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_assignment(info):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not found in .env")
        return None

    prompt = f"""You are a professional academic writer for SZABIST university Pakistan.

Write a complete, detailed university assignment on the topic below.

Subject: {info['subject']}
Topic / Question: {info['topic']}
Target Length: approximately {info['pages']} pages

STRICT RULES — follow exactly:
1. Do NOT use any markdown symbols like **, ##, ###, --, *, #, or ---
2. Do NOT write cover page, student name, or any header info
3. Write ONLY the assignment body content
4. Section headings must be written in ALL CAPITALS on their own line with no symbols
5. Separate each section with a blank line
6. Write in formal academic English
7. Structure: INTRODUCTION, then 2-3 body sections with topic-based headings, ANALYSIS, CONCLUSION, REFERENCES
8. References section must have at least 3 proper academic references numbered like: 1. Author (Year). Title. Publisher.
9. Each section must be detailed and well-explained
10. No bullet points — write in full paragraphs only

Begin writing the assignment body now:"""

    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 3500,
                "temperature": 0.7
            },
            timeout=90
        )
        print(f"API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            # Clean markdown
            text = re.sub(r'\*{1,3}', '', text)
            text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
            # Clean special characters for PDF
            text = text.replace('\u201c', '"').replace('\u201d', '"')
            text = text.replace('\u2018', "'").replace('\u2019', "'")
            text = text.replace('\u2013', '-').replace('\u2014', '-')
            text = text.replace('\u2026', '...')
            return text.strip()
        else:
            print(f"API Error {response.status_code}: {response.text[:300]}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None