import google.generativeai as genai
import json, re, os
import streamlit as st

# Read API key from Streamlit secrets (cloud) or environment variable (local)
def _get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")

genai.configure(api_key=_get_api_key())

model = genai.GenerativeModel("gemini-2.5-flash")

def predict_guna_with_gemini(journal_text):
    """
    Analyze journal text using Triguna theory (Bhagavad Gita Ch. 14).
    Returns structured JSON with guna percentages, dominant guna,
    AI reasoning, emotion, energy level, and focus level.
    """
    prompt = f"""
You are an expert in Bhagavad Gita Chapter 14 (Triguna theory) and modern behavioral psychology.

Analyze the journal entry below and return a detailed psychological profile.

Triguna Framework:
- Sattva: clarity, wisdom, peace, compassion, creativity
- Rajas: passion, ambition, restlessness, anger, desire, action
- Tamas: inertia, laziness, confusion, depression, ignorance, dullness

Journal:
\"\"\"{journal_text}\"\"\"

Return ONLY valid JSON (no markdown, no explanation outside JSON):
{{
  "Sattva": <integer 0-100>,
  "Rajas": <integer 0-100>,
  "Tamas": <integer 0-100>,
  "DominantGuna": "Sattva" | "Rajas" | "Tamas",
  "Reason": "<2-3 sentence explanation of why this guna dominates, citing specific phrases from the journal>",
  "Emotion": "<primary emotion: e.g. hopeful, anxious, grateful, frustrated, calm, excited, melancholic, motivated>",
  "EnergyLevel": "low" | "medium" | "high",
  "FocusLevel": "low" | "medium" | "high",
  "KeyThemes": ["<theme1>", "<theme2>", "<theme3>"]
}}

RULES:
- Sattva + Rajas + Tamas MUST equal exactly 100
- DominantGuna must match the highest percentage
- Reason must reference actual content from the journal
- Emotion must be a single descriptive word or short phrase
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Extract JSON block (handle markdown code fences)
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in response")
        data = json.loads(match.group())

        # Validate percentages sum to 100
        total = data.get("Sattva", 0) + data.get("Rajas", 0) + data.get("Tamas", 0)
        if abs(total - 100) > 2:
            factor = 100 / total
            data["Sattva"] = round(data["Sattva"] * factor)
            data["Rajas"]  = round(data["Rajas"]  * factor)
            data["Tamas"]  = 100 - data["Sattva"] - data["Rajas"]

        return data

    except Exception as e:
        return {
            "Sattva": 33, "Rajas": 34, "Tamas": 33,
            "DominantGuna": "Rajas",
            "Reason": f"Analysis unavailable: {str(e)}",
            "Emotion": "neutral",
            "EnergyLevel": "medium",
            "FocusLevel": "medium",
            "KeyThemes": ["reflection"]
        }
