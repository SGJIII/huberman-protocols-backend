import requests
from bs4 import BeautifulSoup
import json
import re
from models import save_transcript

def get_transcript_links(base_url):
    links = []
    try:
        response = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=100)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Collecting direct links
            direct_links = [link['href'] if 'http' in link['href'] else base_url.rstrip('/') + link['href']
                            for link in soup.find_all('a', href=True) if '/post/' in link['href']]
            links.extend(direct_links)

            # Finding idMapping and constructing additional links
            script_tag = soup.find('script', text=re.compile('idMapping'))
            if script_tag:
                data = json.loads(script_tag.string)
                id_mapping = data['props']['pageProps']['idMapping']
                mapped_links = [f"{base_url.rstrip('/')}/post/{post_id}" for post_id in id_mapping.values()]
                links.extend(mapped_links)

        else:
            print(f"Failed to fetch {base_url}: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to retrieve links: {e}")
    return links

def scrape_transcripts():
    base_url = "https://www.hubermantranscripts.com/"
    links = get_transcript_links(base_url)
    for url in links:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag:
                    data = json.loads(script_tag.string)
                    transcript_entries = data['props']['pageProps']['transcript']
                    title = data['props']['pageProps']['title'] if 'title' in data['props']['pageProps'] else 'No title'
                    
                    # Aggregate text, assuming values are plain text
                    full_transcript = " ".join(transcript_entries.values())
                    
                    print(f"Attempting to save transcript: {title}")
                    save_transcript(title, url, full_transcript)
                    print(f"Saved transcript: {title}")
                else:
                    print(f"No transcript found for {url}")
            else:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Failed to process {url}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed for {url}: {e}")

if __name__ == '__main__':
    scrape_transcripts()

