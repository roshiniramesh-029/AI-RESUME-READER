import streamlit as st
import PyPDF2
import io
import subprocess

st.set_page_config(
    page_title="AI RESUME CRITIQUER",
    page_icon="📄",
    layout="wide"
)

st.title("AI RESUME CRITIQUER")
st.markdown("Upload your resume and get AI-powered feedback (runs locally using Ollama).")

uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text().encode("utf-8", errors="ignore").decode("utf-8") + "\n"

    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8", errors="ignore")



def analyze_with_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file has no readable content.")
            st.stop()
        file_content = file_content[:4000]

        prompt = f"""
You are an expert resume reviewer with years of HR and recruitment experience.

Analyze the following resume and provide constructive feedback focusing on:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Improvements for {job_role if job_role else 'general job applications'}

Resume:
{file_content}

Provide clear, structured feedback with bullet points.
"""

        with st.spinner("Analyzing resume locally using AI..."):
            feedback = analyze_with_ollama(prompt)

        st.markdown("### 📊 Analysis Results")
        st.write(feedback)

    except FileNotFoundError:
        st.error("Ollama is not installed or not found. Please install Ollama first.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
