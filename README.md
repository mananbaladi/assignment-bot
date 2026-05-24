# SZABIST Assignment Bot

## Setup (one time only)

1. Extract this ZIP to Desktop

2. Open VS Code in the folder, open terminal (Ctrl + ~)

3. Create virtual environment:
   ```
   C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe -m venv venv
   venv\Scripts\activate
   ```

4. Install packages:
   ```
   python -m pip install streamlit python-docx fpdf2 requests python-dotenv
   ```

5. Open `.env` file and paste your GitHub token:
   ```
   GITHUB_TOKEN=github_pat_your_token_here
   ```

6. Run the app:
   ```
   streamlit run app.py
   ```

## Features
- SZABIST formatted cover page (blue header, grey department bar)
- AI-generated academic content (no markdown symbols)
- Download as Word (.docx) or PDF
- Proper footer: Department | Batch | SZABIST
