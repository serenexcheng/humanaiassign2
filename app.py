import streamlit as st
import requests

st.set_page_config(page_title="Stock Market Explainer", page_icon="📈")

st.title("📈 Stock Market Explainer (Educational)")
st.write("""
This app gives simple, beginner-friendly explanations of what a company does,
how it makes money, and typical risks companies like it face.

⚠️ This is for **learning only**, not financial advice.
""")

company_name = st.text_input("🏢 Enter a company name:", placeholder="NVIDIA, AAPL, TSMC, etc.")

knowledge_level = st.selectbox(
    "Your familiarity with stocks:",
    ["Beginner", "Some experience", "Quite familiar"]
)

focus_area = st.multiselect(
    "What would you like explained?",
    [
        "What the company does",
        "How it makes money",
        "Who its customers are",
        "Typical risks",
        "Beginner analogy"
    ],
    default=["What the company does", "How it makes money", "Typical risks"]
)

DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]

API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_explanation(company, level, focus_points):
    focus_text = ", ".join(focus_points)

    prompt = f"""
Explain the company "{company}" in simple, beginner-friendly language.
User knowledge level: {level}
Focus areas: {focus_text}

Rules:
- No investment advice.
- No price predictions.
- Keep paragraphs short.
- Use everyday examples.
- Include a section called "General Risks".
- End with: "This explanation is for learning only, not financial advice."
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7  
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]


if st.button("✨ Explain"):
    if not company_name.strip():
        st.warning("Please enter a company name first.")
    else:
        with st.spinner("Generating explanation…"):
            explanation = generate_explanation(company_name, knowledge_level, focus_area)
        st.write(explanation)
        st.info("This explanation is for learning only — not financial advice.")
