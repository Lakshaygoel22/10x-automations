import os
import json
import google.generativeai as genai

def analyze_profile_sync(profile):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key":
        return {"score": 50, "category": "Unknown", "outreach": "Hi " + profile['name'] + ", thanks for reacting to my post!"}
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = "You are an expert sales AI. Analyze this LinkedIn profile. Name: " + profile['name'] + ". Headline: " + profile['headline'] + ".\n"
    prompt += "Return ONLY a valid JSON object with these keys: 'score' (integer 0-100 based on their seniority/decision-making power from the headline), 'category' (string, e.g., 'Executive', 'Engineer', 'Student'), and 'outreach' (string, a highly personalized 2-sentence cold outreach message mentioning their headline)."
    try:
        response = model.generate_content(prompt)
        text = response.text
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception:
        return {"score": 0, "category": "Error", "outreach": "Could not generate AI insights."}
