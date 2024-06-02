import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from models import get_transcript_by_id
from fpdf import FPDF
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sendinblue_api_key = os.getenv("SENDINBLUE_API_KEY")

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = sendinblue_api_key

def generate_protocol(episode_id):
    try:
        logging.info(f"Generating protocol for episode_id: {episode_id}")
        transcript = get_transcript_by_id(episode_id)
        if not transcript:
            logging.error(f"No relevant transcript found for episode_id: {episode_id}")
            return "No relevant transcript found."

        summary = transcript['summary']  # Use the summary from the dictionary

        # Use the summary to generate a response
        prompt = f"The user wants an easy to use protocol from episode ID {episode_id}. Please provide a quick 1 sentence summary of this: {summary}. Based on this, please provide a Huberman protocol of daily practices they can implement it into their daily lives to improve their lives based on the context of the summary and divide them into helpful categories. Please include only ideas and helpful products from the summary and be extremely detailed."

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )

        logging.info(f"Protocol generated successfully for episode_id: {episode_id}")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating protocol for episode_id {episode_id}: {e}")
        return f"Error generating protocol: {e}"

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

def generate_pdf(protocol_text, user_email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, protocol_text)
    pdf_output = f"protocol_{user_email}.pdf"
    pdf.output(pdf_output)
    return pdf_output

def send_protocol_via_email(protocol_text, user_email):
    pdf_path = generate_pdf(protocol_text, user_email)
    return send_brevo_email(user_email, pdf_path)

def send_brevo_email(user_email, pdf_path):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"email": "your-email@example.com", "name": "Your Name"}
    to = [{"email": user_email, "name": ""}]
    subject = "Your Huberman Protocol"
    html_content = "Please find attached your personalized Huberman protocol."

    with open(pdf_path, "rb") as attachment:
        attachment_content = attachment.read()
    
    attachment_data = [
        {
            "content": attachment_content,
            "name": "protocol.pdf"
        }
    ]
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content,
        attachment=attachment_data
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return f"Email sent successfully: {api_response}"
    except ApiException as e:
        return f"Failed to send email: {e}"