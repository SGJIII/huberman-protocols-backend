import openai
import os
from dotenv import load_dotenv
from models import get_all_transcripts

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv('OPEN_AI_API_KEY')

def generate_protocol(user_input):
    transcripts = get_all_transcripts()
    transcript_texts = [transcript[3] for transcript in transcripts]  # assuming content is in the fourth position
    
    # Combine all transcript texts into one large string
    combined_transcripts = ' '.join(transcript_texts)
    
    # Use the combined transcripts to generate a response
    prompt = f"The user wants to: {user_input}. Based on the following transcripts, provide a Huberman protocol: {combined_transcripts}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    return response.choices[0].text.strip()

