import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_assignment(info):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None

    prompt = f"""You are a professional academic writer for SZABIST university Pakistan.

Write a complete university assignment on the topic below.

Subject: {info['subject']}
Topic / Question: {info['topic']}
Target Length: approximately {info['pages']} pages

STRICT RULES:
1. Write EXACTLY what the question asks — nothing more, nothing less
2. If question asks for definition, give definition
3. If question asks for comparison, compare
4. If question asks for explanation, explain
5. Do NOT add extra sections not asked in the question
6. Do NOT use markdown symbols like **, ##, *, ---
7. Section headings in ALL CAPITALS on their own line
8. Write in full paragraphs, no bullet points
9. Do NOT write cover page or student info
10. End with REFERENCES section with 3 academic references

Begin writing now:"""

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
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            text = re.sub(r'\*{1,3}', '', text)
            text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
            text = text.replace('\u201c', '"').replace('\u201d', '"')
            text = text.replace('\u2018', "'").replace('\u2019', "'")
            text = text.replace('\u2013', '-').replace('\u2014', '-')
            text = text.replace('\u2026', '...')
            return text.strip()
        else:
            return None
    except Exception as e:
        return None