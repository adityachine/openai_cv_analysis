# Import necessary libraries
import streamlit as st  # Streamlit for web app interface
import fitz  # PyMuPDF – used to read and extract text from PDF files
from openai import OpenAI  # OpenAI client for accessing GPT models

# ⚠️ WARNING: Hardcoding API keys is insecure. Use environment variables instead for production.
api_key = "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"  # OpenAI API Key (should be kept secret and not exposed in source code)

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Function to extract text from uploaded PDF using PyMuPDF
def extract_text_from_pdf(uploaded_file):
    text = ""  # Initialize empty string to store extracted text
    try:
        # Open the PDF file stream with fitz (PyMuPDF)
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            # Iterate through each page and extract text
            for page in doc:
                text += page.get_text()
    except Exception as e:
        # Handle exceptions and return error message as text
        text = f"Error reading PDF: {e}"
    return text  # Return extracted or error text

# Function to analyze resume text vs job description using OpenAI
def analyze_resume(resume_text, jd_text):
    # Create the prompt with resume and job description inserted
    prompt = f"""
You are an HR AI assistant. Given the following RESUME and JOB DESCRIPTION, analyze how well they match.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Respond with:
- Match Percentage
- 3 key skills missing in resume
- 2 suggestions to improve resume
"""
    try:
        # Call the OpenAI Chat API with the crafted prompt
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o mini model
            messages=[{"role": "user", "content": prompt}],  # Provide user prompt
            temperature=0.3  # Lower temp = more deterministic output
        )
        # Extract and return the AI's response message
        return response.choices[0].message.content
    except Exception as e:
        # Return any error that occurred during the API call
        return f"❌ Error during AI analysis: {e}"

# Configure Streamlit app layout and title
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# Display the app title in a styled HTML heading
st.markdown("<h1 style='text-align: center; color: white;'>AI Resume Analyzer</h1>", unsafe_allow_html=True)
# Description below title
st.markdown("<p style='text-align: center;'>Upload your resume and job description to get AI-based feedback.</p>", unsafe_allow_html=True)

# Section header for file upload
st.markdown("### 📄 Upload Your Files")
# File uploader for resume PDF
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
# File uploader for job description PDF
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

# Submit button to start analysis
if st.button("🚀 Analyze Resume"):
    # Check both files are uploaded
    if resume_file and jd_file:
        st.info("🔄 Extracting content...")  # Show status to user

        # Extract text from uploaded resume and job description
        resume_text = extract_text_from_pdf(resume_file)
        jd_text = extract_text_from_pdf(jd_file)

        # Check if extraction was successful
        if "Error" in resume_text or "Error" in jd_text:
            st.error("❌ Failed to extract text from one or both PDFs.")  # Show error if extraction failed
        else:
            st.success("✅ Files read successfully!")  # Success message

            # Show a preview of resume text
            st.subheader("📑 Resume Preview")
            st.text(resume_text[:500])  # Show only first 500 characters

            # Show a preview of job description text
            st.subheader("📋 Job Description Preview")
            st.text(jd_text[:500])  # Show only first 500 characters

            # Analyze and display AI-generated analysis
            st.subheader("🤖 AI Resume Analysis")
            result = analyze_resume(resume_text, jd_text)  # Get AI response
            st.markdown(result)  # Display result
    else:
        # Warn user if one or both files are missing
        st.error("⚠️ Please upload both resume and job description.")
