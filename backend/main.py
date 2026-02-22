import os
import pdfplumber
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume to Email Generator API")

# Allow requests from the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text content from PDF bytes using pdfplumber."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def generate_email_with_groq(
    resume_text: str,
    company_name: str,
    job_role: str,
    recipient_email: str,
) -> str:
    """Use Groq API to generate a professional job application email."""
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not set. Please add it to your .env file.",
        )

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""You are an expert career coach and professional email writer.
Based on the following resume, write a concise, professional, and personalized job application email.

RESUME:
{resume_text}

TARGET COMPANY: {company_name}
JOB ROLE: {job_role}
RECIPIENT EMAIL: {recipient_email}

Write a compelling job application email that:
1. Has a professional subject line (prefix with "Subject: ")
2. Starts with a strong opening that mentions the company and the role
3. Highlights 2-3 most relevant skills/experiences from the resume
4. Shows genuine enthusiasm for the company
5. Ends with a clear call to action
6. Is concise (200-300 words max)

Output ONLY the email content, starting with "Subject: "
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=800,
    )

    return chat_completion.choices[0].message.content


@app.get("/")
def read_root():
    return {"message": "Resume to Email Generator API is running!"}


@app.post("/generate-email")
async def generate_email(
    resume: UploadFile = File(..., description="Resume PDF file"),
    company_name: str = Form(..., description="Target company name"),
    job_role: str = Form(..., description="Target job role"),
    recipient_email: str = Form(..., description="Recipient email address"),
):
    """
    Accepts a resume PDF and job details,
    extracts resume text, and generates a personalized email using AI.
    """
    # Validate file type
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read and extract text from the uploaded PDF
    file_bytes = await resume.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF. Please ensure it is a text-based PDF.",
        )

    # Generate the email using the AI model
    generated_email = generate_email_with_groq(
        resume_text=resume_text,
        company_name=company_name,
        job_role=job_role,
        recipient_email=recipient_email,
    )

    return {
        "success": True,
        "company_name": company_name,
        "job_role": job_role,
        "recipient_email": recipient_email,
        "generated_email": generated_email,
    }
