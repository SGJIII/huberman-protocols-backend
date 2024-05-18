import os
from openai import OpenAI
from dotenv import load_dotenv
from models import search_transcripts
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_protocol(user_input):
    transcripts = search_transcripts(user_input)
    if not transcripts:
        return "No relevant transcripts found."

    # Extract excerpts from the found transcripts
    excerpts = []
    for transcript in transcripts:
        excerpts.append(transcript[3][:1000])  # Taking the first 1000 characters as an excerpt

    # Combine all excerpts into one large string
    combined_excerpts = ' '.join(excerpts)
    
    # Use the combined excerpts to generate a response
    prompt = f"The user wants to: {user_input}. Based on the following transcript excerpts, provide a Huberman protocol: {combined_excerpts}"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    
    return response.choices[0].message.content.strip()

def update_protocol(user_input, protocol_text):
    prompt = f"The current protocol is: {protocol_text}. The user wants to make the following changes: {user_input}. Update the protocol accordingly."

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    
    return response.choices[0].message.content.strip()

def send_protocol_via_email(protocol_text, user_email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, protocol_text)

    pdf_output = f"protocol_{user_email}.pdf"
    pdf.output(pdf_output)

    # Email configuration
    sender_email = "your-email@example.com"
    sender_password = "your-password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = "Your Huberman Protocol"

    body = "Please find attached your personalized Huberman protocol."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_output, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=pdf_output)
        part['Content-Disposition'] = f'attachment; filename="{pdf_output}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"