import os
from openai import OpenAI
from dotenv import load_dotenv
from models import get_transcript_by_id
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_protocol(episode_id):
    transcript = get_transcript_by_id(episode_id)
    if not transcript:
        return "No relevant transcript found."

    summary = transcript[4]  # Use the summary from the selected episode

    # Use the summary to generate a response
    prompt = f"The user wants an easy to use protocol from: {episode_id}. please provide a quick 1 sentence summary of this: {summary}. Based on this, please provide a Huberman protocol that the user can implament into their daily lives to improve their lives based on the context of the summary. Please include only ideas and any helpful products from the summary."

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    
    return response.choices[0].message.content.strip()

def update_protocol(user_input, protocol_text):
    prompt = f"The current protocol is: {protocol_text}. The user wants to make the following changes: {user_input}. Update the protocol accordingly."

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
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
