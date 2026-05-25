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