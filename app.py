import streamlit as st
import google.generativeai as genai

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

# Configure Gemini using Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

def generate_explanation(company, level, focus_list):
    focus_text = ", ".join(focus_list)
    prompt = f"""
Explain the company "{company}" in simple, educational language.
User stock knowledge level: {level}
Focus areas: {focus_text}

Guidelines:
- No investment advice.
- No price predictions.
- Use short paragraphs.
- Keep explanations general and beginner-friendly.
- Include a final reminder: "This is for learning only, not financial advice."
"""
    response = model.generate_content(prompt)
    return response.text


if st.button("✨ Explain"):
    if not company_name.strip():
        st.warning("Please enter a company name first.")
    else:
        with st.spinner("Generating explanation…"):
            result = generate_explanation(company_name, knowledge_level, focus_area)
        st.write(result)
        st.info("This explanation is for learning only — not financial advice.")
