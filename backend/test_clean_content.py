import re

def clean_content(content):
    # Updated regex with better whitespace handling
    cleaned_content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}\s+', '', content)
    return cleaned_content.strip()

# Test the function
test_content = "00:00.000 --> 00:02.240 Welcome to the Huberman Lab Podcast,\n"
print("Original Content:", test_content)
print("Cleaned Content:", clean_content(test_content))

