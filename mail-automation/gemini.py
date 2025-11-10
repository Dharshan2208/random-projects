import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def classify_email(subject, body):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
            You are an email classification assistant.
            Classify the following email into one of the categories: Work, Personal, Finance, Spam, Promotions.

            Only respond with the single category name.

            ---
            Subject: {subject}
            Body: {body}
            """

    response = model.generate_content(prompt, generation_config={"temperature": 0.25})
    return response.text.strip()

#  Just for testing 
if __name__ == "__main__":
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    category = classify_email(subject, body)
    print(f"\n Gemini classified this email as: **{category}**")